from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = "https://longlongli.com/assets/Project/High-throughput%20screening%20platform.jpg"

PAGES = {
    "index.html": (
        "Longlong Li | BioMEMS & Engineered Cardiac Tissue Sensing",
        "Personal academic website of Longlong Li, PhD student working on BioMEMS, multimodal biosensing, engineered cardiac tissue monitoring, and drug cardiotoxicity evaluation.",
        "https://longlongli.com/",
    ),
    "en/index.html": (
        "Longlong Li | BioMEMS & Engineered Cardiac Tissue Sensing",
        "Personal academic website of Longlong Li, PhD student working on BioMEMS, multimodal biosensing, engineered cardiac tissue monitoring, and drug cardiotoxicity evaluation.",
        "https://longlongli.com/en/",
    ),
    "zh/index.html": (
        "李龙龙 | BioMEMS 与工程化心脏组织传感",
        "李龙龙，机械工程博士研究生，研究方向聚焦于 BioMEMS 多模态传感平台、工程化心脏组织机电监测和药物心脏毒性评价。",
        "https://longlongli.com/zh/",
    ),
    "projects.html": (
        "Longlong Li | Research Projects",
        "Research and engineering projects by Longlong Li in BioMEMS, engineered cardiac tissue monitoring, biosensing platforms, and biomedical device systems.",
        "https://longlongli.com/projects.html",
    ),
    "zh/projects.html": (
        "李龙龙 | 研究项目",
        "李龙龙的研究与工程项目，涵盖 BioMEMS、工程化心脏组织监测、生物传感平台和多模态生物信号分析。",
        "https://longlongli.com/zh/projects.html",
    ),
    "publications.html": (
        "Longlong Li | Publications",
        "Journal publications by Longlong Li in BioMEMS, cardiac tissue engineering, biosensing, biomaterials, and related biomedical engineering topics.",
        "https://longlongli.com/publications.html",
    ),
    "zh/publications.html": (
        "李龙龙 | 论文发表",
        "李龙龙的期刊论文记录，涵盖 BioMEMS、心脏组织工程、生物传感、生物材料和相关生物医学工程方向。",
        "https://longlongli.com/zh/publications.html",
    ),
    "conferences.html": (
        "Longlong Li | Conferences",
        "Conference presentations by Longlong Li, including MicroTAS, IEEE NANOMED, IEEE MEMS, and IEEE SENSORS records.",
        "https://longlongli.com/conferences.html",
    ),
    "zh/conferences.html": (
        "李龙龙 | 学术会议",
        "李龙龙的学术会议和报告记录，包括 MicroTAS、IEEE NANOMED、IEEE MEMS 和 IEEE SENSORS 等会议。",
        "https://longlongli.com/zh/conferences.html",
    ),
    "patents.html": (
        "Longlong Li | Patents",
        "Patent records by Longlong Li, including invention patents and utility model patents from engineering and device-development projects.",
        "https://longlongli.com/patents.html",
    ),
    "zh/patents.html": (
        "李龙龙 | 专利",
        "李龙龙的专利记录，包括授权发明专利、发明专利申请和实用新型专利。",
        "https://longlongli.com/zh/patents.html",
    ),
    "awards.html": (
        "Longlong Li | Awards",
        "Awards, scholarships, and academic honors received by Longlong Li.",
        "https://longlongli.com/awards.html",
    ),
    "zh/awards.html": (
        "李龙龙 | 奖励荣誉",
        "李龙龙获得的奖学金、竞赛奖项和学术荣誉记录。",
        "https://longlongli.com/zh/awards.html",
    ),
    "gallery.html": (
        "Longlong Li | Gallery",
        "Chronological gallery of academic, research, conference, and personal milestones for Longlong Li.",
        "https://longlongli.com/gallery.html",
    ),
    "zh/gallery.html": (
        "李龙龙 | 图集",
        "李龙龙学习、科研、会议和阶段性经历的时间线图集。",
        "https://longlongli.com/zh/gallery.html",
    ),
    "cv.html": (
        "Longlong Li | CV",
        "Professional academic CV and resume overview for Longlong Li, focused on BioMEMS, biosensors, and engineered cardiac tissue monitoring.",
        "https://longlongli.com/cv.html",
    ),
    "zh/cv.html": (
        "李龙龙 | 简历",
        "李龙龙的学术简历与求职简历概览，聚焦 BioMEMS、生物传感器和工程化心脏组织监测。",
        "https://longlongli.com/zh/cv.html",
    ),
}


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def metadata_block(title: str, description: str, url: str) -> str:
    title_escaped = html_escape(title)
    description_escaped = html_escape(description)
    return f"""    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{title_escaped}" />
    <meta property="og:description" content="{description_escaped}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{DEFAULT_IMAGE}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title_escaped}" />
    <meta name="twitter:description" content="{description_escaped}" />
    <meta name="twitter:image" content="{DEFAULT_IMAGE}" />"""


def update_page(path: Path, title: str, description: str, url: str) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"<title>.*?</title>", f"<title>{html_escape(title)}</title>", html, count=1, flags=re.S)
    html = re.sub(
        r'<meta\s+name="description"\s+content=".*?"\s*/>',
        f'<meta name="description" content="{html_escape(description)}" />',
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(r"\n\s*<link rel=\"canonical\".*?/>", "", html)
    html = re.sub(r"\n\s*<meta property=\"og:.*?/>", "", html)
    html = re.sub(r"\n\s*<meta name=\"twitter:.*?/>", "", html)
    block = metadata_block(title, description, url)
    html = re.sub(
        r'(<meta\s+name="description"\s+content=".*?"\s*/>)',
        r"\1\n" + block,
        html,
        count=1,
        flags=re.S,
    )
    path.write_text(html, encoding="utf-8")


def main() -> None:
    for relative, metadata in PAGES.items():
        update_page(ROOT / relative, *metadata)


if __name__ == "__main__":
    main()
