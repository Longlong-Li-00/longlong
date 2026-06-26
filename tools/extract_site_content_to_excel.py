#!/usr/bin/env python3
"""Extract structured website content and build data/website_content.xlsx.

The script deliberately leaves the public HTML rendering unchanged. It parses the
current static pages into a temporary JSON payload, validates critical fields, and
delegates workbook authoring to build_website_content_workbook.mjs.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]


class Node:
    def __init__(self, tag: str, attrs: dict[str, str], parent: "Node | None" = None):
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children: list[Node | str] = []

    @property
    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())

    def text(self, separator: str = " ") -> str:
        parts: list[str] = []

        def walk(node: Node | str) -> None:
            if isinstance(node, str):
                parts.append(node)
                return
            if node.tag == "br":
                parts.append(separator)
            for child in node.children:
                walk(child)

        walk(self)
        return re.sub(r"\s+", " ", html.unescape("".join(parts))).strip()

    def find_all(
        self,
        tag: str | None = None,
        class_name: str | None = None,
        attr: str | None = None,
        attr_value: str | None = None,
    ) -> list["Node"]:
        matches: list[Node] = []

        def walk(node: Node) -> None:
            for child in node.children:
                if not isinstance(child, Node):
                    continue
                ok = tag is None or child.tag == tag
                ok = ok and (class_name is None or class_name in child.classes)
                ok = ok and (attr is None or attr in child.attrs)
                ok = ok and (attr_value is None or child.attrs.get(attr or "") == attr_value)
                if ok:
                    matches.append(child)
                walk(child)

        walk(self)
        return matches

    def first(
        self,
        tag: str | None = None,
        class_name: str | None = None,
        attr: str | None = None,
        attr_value: str | None = None,
    ) -> "Node | None":
        matches = self.find_all(tag, class_name, attr, attr_value)
        return matches[0] if matches else None


class DOMParser(HTMLParser):
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("document", {})
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag, {key: value or "" for key, value in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag == tag and tag not in self.VOID_TAGS:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


def parse_html(path: Path) -> Node:
    parser = DOMParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.root


def node_text(node: Node | None) -> str:
    return node.text() if node else ""


def direct_children(node: Node, tag: str | None = None, class_name: str | None = None) -> list[Node]:
    result = []
    for child in node.children:
        if not isinstance(child, Node):
            continue
        if tag and child.tag != tag:
            continue
        if class_name and class_name not in child.classes:
            continue
        result.append(child)
    return result


def find_heading(root: Node, text: str) -> Node:
    for node in root.find_all(class_name="subsection-title"):
        if node.text() == text:
            return node
    raise ValueError(f"Heading not found: {text}")


def enclosing(node: Node, class_name: str) -> Node:
    current = node.parent
    while current:
        if class_name in current.classes:
            return current
        current = current.parent
    raise ValueError(f"No enclosing .{class_name} for {node.text()}")


def extract_doi(url: str) -> str:
    if not url:
        return ""
    decoded = unquote(url)
    parsed = urlparse(decoded)
    if parsed.netloc == "doi.org":
        return parsed.path.lstrip("/")
    for marker in ("/doi/", "/article/"):
        if marker in parsed.path:
            candidate = parsed.path.split(marker, 1)[1]
            candidate = re.sub(r"/(?:meta|full)$", "", candidate)
            if candidate.startswith("10."):
                return candidate
    return ""


def slug_key(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title.lower())
    return "".join(words[:4]) or "publication"


def publication_metadata(year_text: str) -> tuple[int | str, str, str, str, str]:
    cleaned = year_text.strip().rstrip(".")
    match = re.match(r"(?P<year>20\d{2})(?:,\s*(?P<rest>.*))?$", cleaned)
    if not match:
        return "", "", "", "", "Unparsed publication metadata"
    year = int(match.group("year"))
    rest = (match.group("rest") or "").strip()
    volume = issue = pages = notes = ""
    if not rest:
        return year, volume, issue, pages, notes
    full = re.fullmatch(r"(\d+)\(([^)]+)\):\s*(.+)", rest)
    volume_issue = re.fullmatch(r"(\d+)\(([^)]+)\)", rest)
    volume_pages = re.fullmatch(r"(\d+):\s*(.+)", rest)
    article_number = re.fullmatch(r"(\d{5,})", rest)
    if full:
        volume, issue, pages = full.groups()
    elif volume_issue:
        volume, issue = volume_issue.groups()
    elif volume_pages:
        volume, pages = volume_pages.groups()
    elif article_number:
        pages = article_number.group(1)
        notes = "Article number as displayed on the website"
    else:
        notes = f"Unparsed journal metadata: {rest}"
    return year, volume, issue, pages, notes


def make_bibtex(record: dict) -> str:
    key = f"li{record['year']}{slug_key(record['title_en'])}"
    authors = re.sub(r"\.\s*$", "", record["authors"]).replace(", ", " and ")
    fields = [
        ("title", record["title_en"]),
        ("author", authors),
        ("journal", record["journal"]),
        ("year", str(record["year"])),
        ("volume", record["volume"]),
        ("number", record["issue"]),
        ("pages", record["pages"]),
        ("doi", record["doi"]),
        ("url", record["link"]),
    ]
    body = ",\n".join(f"  {name} = {{{value}}}" for name, value in fields if value)
    return f"@article{{{key},\n{body}\n}}"


def parse_publications(en: Node, zh: Node, home: Node, cv: Node) -> list[dict]:
    en_items = en.find_all(tag="li", class_name="pub-item")
    zh_items = zh.find_all(tag="li", class_name="pub-item")
    selected_titles = {
        node.text()
        for source in (home, cv)
        for node in source.find_all(class_name="pub-title")
    }
    records = []
    for index, item in enumerate(en_items, 1):
        title = node_text(item.first(class_name="pub-title"))
        authors = node_text(item.first(class_name="pub-authors")).rstrip(".")
        journal = node_text(item.first(class_name="pub-venue")).rstrip(",")
        year_text = node_text(item.first(class_name="pub-year"))
        link_node = item.first(tag="a")
        link = link_node.attrs.get("href", "") if link_node else ""
        year, volume, issue, pages, notes = publication_metadata(year_text)
        zh_title = ""
        if index <= len(zh_items):
            zh_title = node_text(zh_items[index - 1].first(class_name="pub-title"))
        record = {
            "id": f"pub_{index:03d}",
            "year": year,
            "title_en": title,
            "title_zh": zh_title,
            "authors": authors,
            "journal": journal,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": extract_doi(link),
            "link": link,
            "type": "journal",
            "selected": title in selected_titles,
            "bibtex": "",
            "notes": notes,
        }
        record["bibtex"] = make_bibtex(record)
        records.append(record)
    return records


def parse_labeled_text(text: str, label: str, next_labels: list[str]) -> str:
    end_pattern = "|".join(re.escape(value) for value in next_labels)
    pattern = rf"{re.escape(label)}\s*(.*?)(?=\.\s*(?:{end_pattern})|$)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def patent_type_for_subsection(subsection: Node) -> str:
    heading = node_text(subsection.first(class_name="subsection-title"))
    if "Granted" in heading:
        return "granted_invention"
    if "Application" in heading:
        return "published_invention_application"
    if "Utility" in heading:
        return "utility_model"
    return "other"


def parse_patents(en: Node, zh: Node) -> list[dict]:
    en_groups = en.find_all(class_name="subsection")
    zh_groups = zh.find_all(class_name="subsection")
    records = []
    index = 0
    labels = [
        "Patentee:",
        "Applicant:",
        "Patent / Application No.:",
        "Status:",
        "Application date:",
        "Grant date:",
        "Publication date:",
    ]
    for group_index, en_group in enumerate(en_groups):
        if not en_group.first(class_name="section-item"):
            continue
        zh_group = zh_groups[group_index]
        patent_type = patent_type_for_subsection(en_group)
        en_items = en_group.find_all(class_name="section-item")
        zh_items = zh_group.find_all(class_name="section-item")
        for item_index, en_item in enumerate(en_items):
            index += 1
            zh_item = zh_items[item_index]
            subtitle = node_text(en_item.first(class_name="item-subtitle"))
            number_match = re.search(
                r"Patent / Application No\.:\s*(.*?)\s*/\s*(.*?)\.\s*Status:",
                subtitle,
            )
            patent_number = number_match.group(1).strip() if number_match else ""
            application_number = number_match.group(2).strip() if number_match else ""
            applicant = parse_labeled_text(subtitle, "Patentee:", labels[2:])
            if not applicant:
                applicant = parse_labeled_text(subtitle, "Applicant:", labels[2:])
            records.append(
                {
                    "id": f"pat_{index:03d}",
                    "date": node_text(en_item.first(class_name="item-period")),
                    "title_zh": node_text(zh_item.first(class_name="item-title")),
                    "title_en": node_text(en_item.first(class_name="item-title")),
                    "inventors": parse_labeled_text(subtitle, "Inventors:", labels),
                    "applicant": applicant,
                    "patent_type": patent_type,
                    "patent_number": patent_number,
                    "application_number": application_number,
                    "status": parse_labeled_text(subtitle, "Status:", labels[4:]),
                    "application_date": parse_labeled_text(subtitle, "Application date:", labels[5:]),
                    "grant_or_publication_date": (
                        parse_labeled_text(subtitle, "Grant date:", [])
                        or parse_labeled_text(subtitle, "Publication date:", [])
                    ),
                    "notes": "",
                }
            )
    return records


def split_conference_location(value: str) -> tuple[str, str]:
    match = re.match(r"^(.*?\b20\d{2}),\s*(.+)$", value)
    return (match.group(1), match.group(2)) if match else (value, "")


def parse_conferences(en: Node, zh: Node) -> list[dict]:
    en_groups = en.find_all(attr="data-conference-root")
    zh_groups = zh.find_all(attr="data-conference-root")
    records = []
    index = 0
    for group_index, en_group in enumerate(en_groups):
        heading = node_text(en_group.first(class_name="subsection-title")).lower()
        presentation_type = "oral" if "oral" in heading else "poster"
        en_items = en_group.find_all(class_name="section-item")
        zh_items = zh_groups[group_index].find_all(class_name="section-item")
        for item_index, en_item in enumerate(en_items):
            index += 1
            subtitle = node_text(en_item.first(class_name="item-subtitle"))
            venue, authors = (subtitle.split(" | ", 1) + [""])[:2]
            conference, location = split_conference_location(venue)
            authors = authors.replace("H. Sun", "Haolan Sun")
            link_node = en_item.first(tag="a")
            records.append(
                {
                    "id": f"conf_{index:03d}",
                    "year": int(node_text(en_item.first(class_name="item-period"))),
                    "title_en": node_text(en_item.first(class_name="item-title")),
                    "title_zh": node_text(zh_items[item_index].first(class_name="item-title")),
                    "authors": authors,
                    "conference": conference,
                    "location": location,
                    "presentation_type": presentation_type,
                    "link": link_node.attrs.get("href", "") if link_node else "",
                    "notes": "",
                }
            )
    return records


def award_category(heading: str) -> str:
    if "Scholarships" in heading:
        return "scholarship"
    if "Academic Honors" in heading:
        return "academic_honor"
    if "Competitions" in heading:
        return "competition"
    return "other"


def award_level(name: str, description: str, category: str) -> str:
    if name == "China National Scholarship":
        return "National-level scholarship"
    if name == "Zhejiang Provincial Government Scholarship":
        return "Provincial-level scholarship"
    if "KMEMS" in name:
        return "Conference paper award"
    if name == "RLRC Outstanding Graduate Student":
        return "Institute-level honor"
    if category == "competition":
        return description.split(",", 1)[0]
    return ""


def award_organization(name: str) -> str:
    if name.startswith("BK21"):
        return "BK21"
    if name.startswith("RLRC"):
        return "RLRC"
    if "KMEMS" in name:
        return "KMEMS 2025"
    if name == "China National Scholarship":
        return "China"
    if name == "Zhejiang Provincial Government Scholarship":
        return "Zhejiang Provincial Government"
    return ""


def parse_awards(en: Node, zh: Node) -> list[dict]:
    en_groups = en.find_all(class_name="subsection")
    zh_groups = zh.find_all(class_name="subsection")
    records = []
    index = 0
    for group_index, en_group in enumerate(en_groups):
        heading = node_text(en_group.first(class_name="subsection-title"))
        category = award_category(heading)
        en_items = en_group.find_all(class_name="section-item")
        zh_items = zh_groups[group_index].find_all(class_name="section-item")
        for item_index, en_item in enumerate(en_items):
            index += 1
            name_en = node_text(en_item.first(class_name="item-title"))
            description_en = node_text(en_item.first(class_name="item-subtitle"))
            records.append(
                {
                    "id": f"award_{index:03d}",
                    "year": int(node_text(en_item.first(class_name="item-period"))),
                    "name_en": name_en,
                    "name_zh": node_text(zh_items[item_index].first(class_name="item-title")),
                    "category": category,
                    "level": award_level(name_en, description_en, category),
                    "organization": award_organization(name_en),
                    "description_en": description_en,
                    "description_zh": node_text(zh_items[item_index].first(class_name="item-subtitle")),
                    "notes": "",
                }
            )
    return records


def labeled_paragraphs(card: Node) -> dict[str, str]:
    values = {}
    for paragraph in card.find_all(tag="p"):
        strong = paragraph.first(tag="strong")
        if not strong:
            continue
        label = strong.text().rstrip(":：").lower()
        full_text = paragraph.text()
        values[label] = full_text[len(strong.text()) :].strip()
    return values


def project_home_notes(home: Node, cv: Node, index: int) -> str:
    home_cards = home.find_all(tag="article", class_name="project-card")
    cv_heading = find_heading(cv, "Selected Projects")
    cv_block = enclosing(cv_heading, "cv-block")
    cv_cards = cv_block.find_all(tag="article", class_name="project-detail-card")
    pieces = []
    if index < len(home_cards):
        card = home_cards[index]
        pieces.append(f"Homepage title: {node_text(card.first(tag='h3'))}")
        paragraphs = card.find_all(tag="p")
        if paragraphs:
            pieces.append(f"Homepage summary: {paragraphs[-1].text()}")
    if index < len(cv_cards):
        card = cv_cards[index]
        pieces.append(f"CV title: {node_text(card.first(tag='h4'))}")
        pieces.append(f"CV metadata: {node_text(card.first(class_name='project-detail-meta'))}")
        bullets = [item.text() for item in card.find_all(tag="li")]
        if bullets:
            pieces.append("CV details: " + " | ".join(bullets))
    return " || ".join(pieces)


def parse_projects(en: Node, zh: Node, home: Node, cv: Node) -> list[dict]:
    en_cards = en.find_all(tag="article", class_name="project-detail-card")
    zh_cards = zh.find_all(tag="article", class_name="project-detail-card")
    records = []
    for index, en_card in enumerate(en_cards):
        zh_card = zh_cards[index]
        meta = node_text(en_card.first(class_name="project-detail-meta"))
        meta_parts = [part.strip() for part in meta.split("|")]
        en_values = labeled_paragraphs(en_card)
        zh_values = labeled_paragraphs(zh_card)
        image_node = en_card.first(tag="img")
        records.append(
            {
                "id": f"project_{index + 1:03d}",
                "title_en": node_text(en_card.first(tag="h3")),
                "title_zh": node_text(zh_card.first(tag="h3")),
                "period": meta_parts[0] if meta_parts else "",
                "lab": meta_parts[1] if len(meta_parts) > 1 else "",
                "background_en": en_values.get("background", ""),
                "background_zh": zh_values.get("背景", ""),
                "methods_en": en_values.get("technical route", ""),
                "methods_zh": zh_values.get("技术路线", ""),
                "contribution_en": en_values.get("my contribution", ""),
                "contribution_zh": zh_values.get("我的贡献", ""),
                "result_en": en_values.get("representative results", ""),
                "result_zh": zh_values.get("代表性结果", ""),
                "image": image_node.attrs.get("src", "") if image_node else "",
                "visible": True,
                "order": index + 1,
                "notes": project_home_notes(home, cv, index),
            }
        )
    return records


def parse_gallery() -> list[dict]:
    source = json.loads((ROOT / "assets" / "gallery-data.json").read_text(encoding="utf-8"))
    return [
        {
            "id": f"gallery_{index:03d}",
            "date": item.get("date", "").replace(".", "-"),
            "title_en": item.get("title", ""),
            "title_zh": item.get("title", ""),
            "image": item.get("src", ""),
            "category": "",
            "description_en": "",
            "description_zh": "",
            "source_filename": item.get("filename", ""),
            "notes": "",
        }
        for index, item in enumerate(source, 1)
    ]


def parse_profile(home_en: Node, home_zh: Node, cv_en: Node, cv_zh: Node) -> list[dict]:
    email_node = home_en.first(attr="data-email-link")
    email = ""
    if email_node:
        email = (
            f"{email_node.attrs.get('data-email-user', '')}@"
            f"{email_node.attrs.get('data-email-domain-name', '')}."
            f"{email_node.attrs.get('data-email-domain-tld', '')}"
        )
    en_keywords = [item.text() for item in enclosing(home_en.first(class_name="hero-interests"), "hero-content").find_all(tag="li")]
    zh_keywords = [item.text() for item in enclosing(home_zh.first(class_name="hero-interests"), "hero-content").find_all(tag="li")]
    en_profile = node_text(cv_en.first(class_name="cv-profile"))
    zh_profile = node_text(cv_zh.first(class_name="cv-profile"))
    values = [
        ("name", node_text(home_en.first(tag="h1")), node_text(home_zh.first(tag="h1")), ""),
        ("position", node_text(home_en.first(class_name="hero-title")), node_text(home_zh.first(class_name="hero-title")), ""),
        ("affiliation", node_text(home_en.first(class_name="hero-affiliation")), node_text(home_zh.first(class_name="hero-affiliation")), ""),
        ("location", node_text(home_en.first(class_name="hero-location")), node_text(home_zh.first(class_name="hero-location")), ""),
        ("email", email, email, "Displayed on the website through JavaScript assembly"),
        ("homepage", "https://longlongli.com", "https://longlongli.com", ""),
        ("research_statement", node_text(home_en.first(class_name="hero-tagline")), node_text(home_zh.first(class_name="hero-tagline")), ""),
        ("research_keywords", "; ".join(en_keywords), "; ".join(zh_keywords), ""),
        ("short_bio", en_profile.split(". ")[0].rstrip(".") + ".", zh_profile.split("。")[0] + "。", ""),
        ("long_bio", en_profile, zh_profile, "Source: CV profile section"),
    ]
    return [{"field": field, "value_en": en_value, "value_zh": zh_value, "notes": notes} for field, en_value, zh_value, notes in values]


def cv_block(root: Node, heading: str) -> Node:
    return enclosing(find_heading(root, heading), "cv-block")


def extract_year_prefix(text: str) -> tuple[str, str]:
    if "|" in text:
        period, rest = text.split("|", 1)
        return period.strip(), rest.strip()
    return "", text


def parse_cv(en: Node, zh: Node) -> list[dict]:
    rows: list[dict] = []

    def add(section: str, item_id: str, period: str, title_en: str, title_zh: str, organization: str, desc_en: str, desc_zh: str, order: int, notes: str = "") -> None:
        rows.append(
            {
                "section": section,
                "item_id": item_id,
                "year_or_period": period,
                "title_en": title_en,
                "title_zh": title_zh,
                "organization": organization,
                "description_en": desc_en,
                "description_zh": desc_zh,
                "order": order,
                "notes": notes,
            }
        )

    add("profile", "cv_profile_001", "", "Profile", "个人简介", "", node_text(en.first(class_name="cv-profile")), node_text(zh.first(class_name="cv-profile")), 1)

    for index, (en_item, zh_item) in enumerate(
        zip(cv_block(en, "Education").find_all(tag="li"), cv_block(zh, "教育经历").find_all(tag="li")),
        1,
    ):
        period_en, title_en = extract_year_prefix(en_item.text())
        period_zh, title_zh = extract_year_prefix(zh_item.text())
        add("education", f"cv_education_{index:03d}", period_en or period_zh, title_en, title_zh, "", "", "", index)

    for index, (en_item, zh_item) in enumerate(
        zip(cv_block(en, "Research Experience").find_all(tag="li"), cv_block(zh, "科研经历").find_all(tag="li")),
        1,
    ):
        add("research_experience", f"cv_research_{index:03d}", "", f"Research experience {index}", f"科研经历 {index}", "", en_item.text(), zh_item.text(), index)

    en_skills = cv_block(en, "Technical Skills").find_all(tag="article", class_name="skill-card")
    zh_skills = cv_block(zh, "技术技能").find_all(tag="article", class_name="skill-card")
    for index, (en_card, zh_card) in enumerate(zip(en_skills, zh_skills), 1):
        add(
            "technical_skills",
            f"cv_skill_{index:03d}",
            "",
            node_text(en_card.first(tag="h4")),
            node_text(zh_card.first(tag="h4")),
            "",
            node_text(en_card.first(tag="p")),
            node_text(zh_card.first(tag="p")),
            index,
        )

    en_projects = cv_block(en, "Selected Projects").find_all(tag="article", class_name="project-detail-card")
    zh_projects = cv_block(zh, "代表项目").find_all(tag="article", class_name="project-detail-card")
    for index, (en_card, zh_card) in enumerate(zip(en_projects, zh_projects), 1):
        en_meta = node_text(en_card.first(class_name="project-detail-meta"))
        zh_meta = node_text(zh_card.first(class_name="project-detail-meta"))
        add(
            "selected_projects",
            f"cv_project_{index:03d}",
            en_meta.split("|", 1)[0].strip(),
            node_text(en_card.first(tag="h4")),
            node_text(zh_card.first(tag="h4")),
            "MNTL",
            " | ".join(item.text() for item in en_card.find_all(tag="li")),
            " | ".join(item.text() for item in zh_card.find_all(tag="li")),
            index,
            f"EN metadata: {en_meta}; ZH metadata: {zh_meta}",
        )

    en_pubs = cv_block(en, "Selected Publications").find_all(tag="li", class_name="pub-item")
    zh_pubs = cv_block(zh, "代表论文").find_all(tag="li", class_name="pub-item")
    for index, (en_item, zh_item) in enumerate(zip(en_pubs, zh_pubs), 1):
        year_text = node_text(en_item.first(class_name="pub-year"))
        year_match = re.search(r"20\d{2}", year_text)
        add(
            "selected_publications",
            f"cv_publication_{index:03d}",
            year_match.group(0) if year_match else "",
            node_text(en_item.first(class_name="pub-title")),
            node_text(zh_item.first(class_name="pub-title")),
            node_text(en_item.first(class_name="pub-venue")).rstrip(","),
            f"{node_text(en_item.first(class_name='pub-authors'))} {year_text}".strip(),
            f"{node_text(zh_item.first(class_name='pub-authors'))} {node_text(zh_item.first(class_name='pub-year'))}".strip(),
            index,
        )

    en_confs = cv_block(en, "Selected Conferences").find_all(class_name="section-item")
    zh_confs = cv_block(zh, "代表会议").find_all(class_name="section-item")
    for index, (en_item, zh_item) in enumerate(zip(en_confs, zh_confs), 1):
        add(
            "selected_conferences",
            f"cv_conference_{index:03d}",
            node_text(en_item.first(class_name="item-period")),
            node_text(en_item.first(class_name="item-title")),
            node_text(zh_item.first(class_name="item-title")),
            node_text(en_item.first(class_name="item-subtitle")).split("|", 1)[0].strip(),
            node_text(en_item.first(class_name="item-subtitle")),
            node_text(zh_item.first(class_name="item-subtitle")),
            index,
        )

    en_patent_block = cv_block(en, "Patent Summary")
    zh_patent_block = cv_block(zh, "专利概览")
    en_stats = [node.text() for node in en_patent_block.find_all(class_name="highlight-card")]
    zh_stats = [node.text() for node in zh_patent_block.find_all(class_name="highlight-card")]
    add("patent_overview", "cv_patent_summary", "", "Patent Summary", "专利概览", "", " | ".join(en_stats), " | ".join(zh_stats), 1)
    for index, (en_item, zh_item) in enumerate(
        zip(en_patent_block.find_all(tag="li"), zh_patent_block.find_all(tag="li")),
        2,
    ):
        add("patent_overview", f"cv_patent_{index - 1:03d}", "", node_text(en_item.first(tag="strong")), node_text(zh_item.first(tag="strong")), "", en_item.text(), zh_item.text(), index)

    en_awards = cv_block(en, "Awards").find_all(class_name="timeline-item")
    zh_awards = cv_block(zh, "奖励荣誉").find_all(class_name="timeline-item")
    for index, (en_item, zh_item) in enumerate(zip(en_awards, zh_awards), 1):
        add(
            "awards",
            f"cv_award_{index:03d}",
            node_text(en_item.first(class_name="timeline-period")),
            node_text(en_item.first(class_name="timeline-title")),
            node_text(zh_item.first(class_name="timeline-title")),
            "",
            node_text(en_item.first(class_name="timeline-subtitle")),
            node_text(zh_item.first(class_name="timeline-subtitle")),
            index,
        )
    return rows


def parse_links(home: Node, cv: Node, cv_zh: Node, publications: list[dict], conferences: list[dict]) -> list[dict]:
    links = [
        {"id": "email", "label_en": "Email", "label_zh": "邮箱", "url": "mailto:lilonglong2000@jnu.ac.kr", "type": "email", "visible": True, "notes": "Website display is assembled with JavaScript"},
        {"id": "homepage", "label_en": "Homepage", "label_zh": "主页", "url": "https://longlongli.com", "type": "profile", "visible": True, "notes": ""},
        {"id": "google_scholar", "label_en": "Google Scholar", "label_zh": "Google Scholar", "url": "https://scholar.google.com/citations?user=eehgHYgAAAAJ&hl=zh-CN", "type": "profile", "visible": True, "notes": ""},
        {"id": "orcid", "label_en": "ORCID", "label_zh": "ORCID", "url": "https://orcid.org/0009-0008-4062-5191", "type": "profile", "visible": True, "notes": ""},
        {"id": "mntl", "label_en": "MNTL", "label_zh": "MNTL 实验室", "url": "https://sites.google.com/view/mntljnu", "type": "lab", "visible": True, "notes": ""},
        {"id": "researchgate", "label_en": "ResearchGate", "label_zh": "ResearchGate", "url": "", "type": "profile", "visible": False, "notes": "TODO: no URL currently available on the website"},
        {"id": "github", "label_en": "GitHub", "label_zh": "GitHub", "url": "", "type": "profile", "visible": False, "notes": "TODO: no URL currently available on the website"},
    ]
    download_index = 0
    for language, source in (("en", cv), ("zh", cv_zh)):
        for link in source.find_all(tag="a"):
            href = link.attrs.get("href", "")
            if "assets/CV/" not in href:
                continue
            download_index += 1
            normalized_href = href[3:] if href.startswith("../") else href
            links.append(
                {
                    "id": f"cv_download_{download_index:02d}",
                    "label_en": link.text() if language == "en" else "",
                    "label_zh": link.text() if language == "zh" else "",
                    "url": normalized_href,
                    "type": "cv_download",
                    "visible": True,
                    "notes": f"{language.upper()} download",
                }
            )
    for record in publications:
        links.append(
            {
                "id": f"{record['id']}_link",
                "label_en": record["title_en"],
                "label_zh": record["title_zh"],
                "url": record["link"],
                "type": "publication",
                "visible": True,
                "notes": "",
            }
        )
    for record in conferences:
        if not record["link"]:
            continue
        links.append(
            {
                "id": f"{record['id']}_link",
                "label_en": record["title_en"],
                "label_zh": record["title_zh"],
                "url": record["link"],
                "type": "conference",
                "visible": True,
                "notes": "",
            }
        )
    return links


HEADERS = {
    "profile": ["field", "value_en", "value_zh", "notes"],
    "publications": ["id", "year", "title_en", "title_zh", "authors", "journal", "volume", "issue", "pages", "doi", "link", "type", "selected", "bibtex", "notes"],
    "patents": ["id", "date", "title_zh", "title_en", "inventors", "applicant", "patent_type", "patent_number", "application_number", "status", "application_date", "grant_or_publication_date", "notes"],
    "conferences": ["id", "year", "title_en", "title_zh", "authors", "conference", "location", "presentation_type", "link", "notes"],
    "awards": ["id", "year", "name_en", "name_zh", "category", "level", "organization", "description_en", "description_zh", "notes"],
    "projects": ["id", "title_en", "title_zh", "period", "lab", "background_en", "background_zh", "methods_en", "methods_zh", "contribution_en", "contribution_zh", "result_en", "result_zh", "image", "visible", "order", "notes"],
    "gallery": ["id", "date", "title_en", "title_zh", "image", "category", "description_en", "description_zh", "source_filename", "notes"],
    "cv": ["section", "item_id", "year_or_period", "title_en", "title_zh", "organization", "description_en", "description_zh", "order", "notes"],
    "links": ["id", "label_en", "label_zh", "url", "type", "visible", "notes"],
}


def extract_content() -> dict[str, list[dict]]:
    documents = {
        "home_en": parse_html(ROOT / "index.html"),
        "home_zh": parse_html(ROOT / "zh" / "index.html"),
        "publications_en": parse_html(ROOT / "publications.html"),
        "publications_zh": parse_html(ROOT / "zh" / "publications.html"),
        "patents_en": parse_html(ROOT / "patents.html"),
        "patents_zh": parse_html(ROOT / "zh" / "patents.html"),
        "conferences_en": parse_html(ROOT / "conferences.html"),
        "conferences_zh": parse_html(ROOT / "zh" / "conferences.html"),
        "awards_en": parse_html(ROOT / "awards.html"),
        "awards_zh": parse_html(ROOT / "zh" / "awards.html"),
        "projects_en": parse_html(ROOT / "projects.html"),
        "projects_zh": parse_html(ROOT / "zh" / "projects.html"),
        "cv_en": parse_html(ROOT / "cv.html"),
        "cv_zh": parse_html(ROOT / "zh" / "cv.html"),
    }
    publications = parse_publications(
        documents["publications_en"],
        documents["publications_zh"],
        documents["home_en"],
        documents["cv_en"],
    )
    patents = parse_patents(documents["patents_en"], documents["patents_zh"])
    conferences = parse_conferences(documents["conferences_en"], documents["conferences_zh"])
    awards = parse_awards(documents["awards_en"], documents["awards_zh"])
    projects = parse_projects(
        documents["projects_en"],
        documents["projects_zh"],
        documents["home_en"],
        documents["cv_en"],
    )
    return {
        "profile": parse_profile(documents["home_en"], documents["home_zh"], documents["cv_en"], documents["cv_zh"]),
        "publications": publications,
        "patents": patents,
        "conferences": conferences,
        "awards": awards,
        "projects": projects,
        "gallery": parse_gallery(),
        "cv": parse_cv(documents["cv_en"], documents["cv_zh"]),
        "links": parse_links(documents["home_en"], documents["cv_en"], documents["cv_zh"], publications, conferences),
    }


def validate(content: dict[str, list[dict]]) -> list[str]:
    warnings: list[str] = []
    for sheet, headers in HEADERS.items():
        if sheet not in content:
            raise ValueError(f"Missing sheet payload: {sheet}")
        for row_index, row in enumerate(content[sheet], 2):
            missing_columns = [column for column in headers if column not in row]
            if missing_columns:
                raise ValueError(f"{sheet} row {row_index} missing columns: {missing_columns}")

    for row in content["publications"]:
        if not row["title_en"] or not row["year"]:
            raise ValueError(f"Critical publication fields missing: {row['id']}")
        for field in ("title_zh", "doi", "volume", "issue", "pages"):
            if not row[field]:
                warnings.append(f"{row['id']}: optional publication field '{field}' is blank")

    for row in content["patents"]:
        if not row["title_en"] or not (row["patent_number"] or row["application_number"]):
            raise ValueError(f"Critical patent fields missing: {row['id']}")

    for row in content["conferences"]:
        if not row["title_en"] or not row["year"] or row["presentation_type"] not in {"oral", "poster"}:
            raise ValueError(f"Critical conference fields missing: {row['id']}")

    for row in content["awards"]:
        if not row["year"] or not row["name_en"]:
            raise ValueError(f"Critical award fields missing: {row['id']}")

    for row in content["projects"]:
        if not row["title_en"] or not isinstance(row["visible"], bool):
            raise ValueError(f"Critical project fields missing: {row['id']}")
        image_path = ROOT / unquote(row["image"])
        if row["image"] and not image_path.exists():
            warnings.append(f"{row['id']}: project image not found: {row['image']}")

    for row in content["gallery"]:
        image_path = ROOT / unquote(row["image"])
        if row["image"] and not image_path.exists():
            warnings.append(f"{row['id']}: gallery image not found: {row['image']}")
        if not row["category"]:
            warnings.append(f"{row['id']}: optional gallery category is blank")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT / "data" / "website_content.xlsx"))
    parser.add_argument("--json-output", default=str(ROOT / "data" / "website_content_extracted.json"))
    parser.add_argument("--node", default=shutil.which("node") or "node")
    parser.add_argument("--skip-workbook", action="store_true")
    args = parser.parse_args()

    content = extract_content()
    warnings = validate(content)
    payload = {
        "headers": HEADERS,
        "sheets": content,
        "warnings": warnings,
    }
    json_path = Path(args.json_output)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Extraction summary:")
    for sheet in HEADERS:
        print(f"  {sheet}: {len(content[sheet])} rows")
    print(f"  warnings: {len(warnings)}")
    for warning in warnings:
        print(f"  WARNING: {warning}")

    if not args.skip_workbook:
        builder = ROOT / "tools" / "build_website_content_workbook.mjs"
        result = subprocess.run(
            [args.node, str(builder), str(json_path), str(Path(args.output))],
            cwd=ROOT,
            check=False,
        )
        output_path = Path(args.output)
        if result.returncode != 0:
            if output_path.exists() and zipfile.is_zipfile(output_path):
                print(
                    "WARNING: workbook builder exited abnormally after producing "
                    "a valid XLSX file; continuing with the exported workbook."
                )
            else:
                raise subprocess.CalledProcessError(
                    result.returncode,
                    [args.node, str(builder), str(json_path), str(output_path)],
                )
    return 0


if __name__ == "__main__":
    sys.exit(main())
