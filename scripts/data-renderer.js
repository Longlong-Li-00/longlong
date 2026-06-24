(function () {
  function getLang() {
    return document.documentElement.lang === "zh" ? "zh" : "en";
  }

  function getSiteRoot() {
    return window.location.pathname.includes("/zh/") ? "../" : "";
  }

  async function loadJson(relativePath) {
    const response = await fetch(getSiteRoot() + relativePath, { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Failed to load ${relativePath}: ${response.status}`);
    }
    return response.json();
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  }

  function clearAndAppend(container, ...children) {
    if (container) container.replaceChildren(...children);
  }

  function getLocalized(record, baseKey, lang) {
    if (!record) return "";
    return record[`${baseKey}_${lang}`] || record[`${baseKey}_en`] || "";
  }

  function highlightLonglong(text) {
    const fragment = document.createDocumentFragment();
    const parts = String(text || "").split(/(Longlong Li|Li Longlong)/g);
    for (const part of parts) {
      if (!part) continue;
      if (part === "Longlong Li" || part === "Li Longlong") fragment.append(el("span", "name-highlight", part));
      else fragment.append(document.createTextNode(part));
    }
    return fragment;
  }

  function makeLinkChip(label, href) {
    if (!href) return null;
    const link = el("a", "", label);
    link.href = href;
    link.target = "_blank";
    link.rel = "noreferrer";
    return link;
  }

  function makeEmailLink(label, mode) {
    const link = el("a", "", label || "Email");
    link.href = "#";
    link.dataset.emailLink = "";
    link.dataset.emailUser = "lilonglong2000";
    link.dataset.emailDomainName = "jnu";
    link.dataset.emailDomainTld = "ac.kr";
    link.dataset.emailText = mode || label || "Email";
    return link;
  }

  function getProfileLink(links, id) {
    return links.find((item) => item.id === id && item.visible);
  }

  function formatPublicationMeta(item) {
    const parts = [];
    if (item.journal) parts.push(item.journal);
    const detail = [];
    if (item.year) detail.push(String(item.year));
    if (item.volume && item.issue) detail.push(`${item.volume}(${item.issue})`);
    else if (item.volume) detail.push(item.volume);
    else if (item.issue) detail.push(`(${item.issue})`);
    if (item.pages) detail.push(item.pages);
    if (detail.length) parts.push(detail.join(", "));
    return parts.join(", ");
  }

  function buildPublicationItem(item, index, lang) {
    const li = el("li", "pub-item");
    li.dataset.year = String(item.year || "");
    const pubIndex = el("span", "pub-index", `[${index}]`);
    const content = el("span", "pub-content");
    const title = el("span", "pub-title", getLocalized(item, "title", lang) || item.title_en);
    const authors = el("span", "pub-authors");
    authors.append(highlightLonglong(item.authors));
    const meta = el("span", "pub-meta", formatPublicationMeta(item));
    const linksWrap = el("div", "pub-links");
    const mainLink = makeLinkChip("Link", item.link);
    const doiLink = item.doi ? makeLinkChip("DOI", `https://doi.org/${item.doi}`) : null;
    if (mainLink) linksWrap.append(mainLink);
    if (doiLink && (!item.link || !item.link.includes(item.doi))) linksWrap.append(doiLink);
    content.append(title, authors, meta);
    if (linksWrap.childElementCount) content.append(linksWrap);
    if (item.bibtex) {
      const citation = document.createElement("details");
      citation.className = "citation-block";
      const summary = document.createElement("summary");
      summary.textContent = lang === "zh" ? "引用" : "BibTeX";
      const pre = document.createElement("pre");
      pre.textContent = item.bibtex;
      citation.append(summary, pre);
      content.append(citation);
    }
    li.append(pubIndex, content);
    return li;
  }

  function buildPublicationControls(container, items, lang) {
    const years = [...new Set(items.map((item) => String(item.year)).filter(Boolean))].sort((a, b) => b.localeCompare(a));
    const controls = el("div", "publication-controls");
    controls.append(el("span", "", lang === "zh" ? "筛选" : "Filter"));
    const addButton = (label, value) => {
      const button = el("button", value === "all" ? "is-active" : "", label);
      button.type = "button";
      button.dataset.filterValue = value;
      controls.append(button);
    };
    addButton(lang === "zh" ? "全部" : "All", "all");
    years.forEach((year) => addButton(year, year));
    controls.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      const value = button.dataset.filterValue || "all";
      controls.querySelectorAll("button").forEach((node) => node.classList.toggle("is-active", node === button));
      container.querySelectorAll(".pub-item").forEach((item) => {
        item.hidden = value !== "all" && item.dataset.year !== value;
      });
      updatePublicationYearHeadings(container);
    });
    return controls;
  }

  function updatePublicationYearHeadings(container) {
    container.querySelectorAll(".pub-year-heading").forEach((node) => node.remove());
    let lastYear = "";
    const visible = [...container.querySelectorAll(".pub-item")].filter((item) => !item.hidden);
    for (const item of visible) {
      const year = item.dataset.year || "Undated";
      if (year === lastYear) continue;
      const heading = el("li", "pub-year-heading", year);
      item.before(heading);
      lastYear = year;
    }
  }

  function showLoadError(container, lang) {
    if (!container) return;
    clearAndAppend(container, el("p", "section-intro", lang === "zh" ? "内容暂时无法加载。" : "Content could not be loaded."));
  }

  function splitCvBullets(value) {
    return String(value || "")
      .split("|")
      .map((item) => item.trim())
      .filter(Boolean);
  }

  function renderHome(profile, links, projects, publications, conferences, patents, awards, lang) {
    const heroHeader = document.querySelector("[data-home-identity]");
    if (heroHeader) {
      heroHeader.querySelector("h1").textContent = profile.name?.[lang] || profile.name?.en || "";
      heroHeader.querySelector(".hero-title").textContent = profile.position?.[lang] || profile.position?.en || "";
      heroHeader.querySelector(".hero-affiliation").textContent = profile.affiliation?.[lang] || profile.affiliation?.en || "";
      heroHeader.querySelector(".hero-location").textContent = profile.location?.[lang] || profile.location?.en || "";
    }
    const tagline = document.querySelector("[data-home-tagline]");
    if (tagline) tagline.textContent = profile.research_statement?.[lang] || profile.research_statement?.en || "";

    const profileLinks = document.querySelector("[data-home-profile-links]");
    if (profileLinks) {
      const nodes = [makeEmailLink("Email", "Email")];
      ["google_scholar", "orcid", "homepage", "mntl"].forEach((id) => {
        const item = getProfileLink(links, id);
        if (!item || !item.url) return;
        const anchor = makeLinkChip(item.label_en || item.label_zh || "", item.url);
        if (anchor) nodes.push(anchor);
      });
      clearAndAppend(profileLinks, ...nodes);
    }

    const interests = document.querySelector("[data-home-interests]");
    if (interests) {
      const values = (lang === "zh" ? profile.research_keywords?.zh_list : profile.research_keywords?.en_list) || [];
      clearAndAppend(interests, ...values.map((value) => el("li", "", value)));
    }

    const projectRoot = document.querySelector("[data-home-projects]");
    if (projectRoot) {
      clearAndAppend(
        projectRoot,
        ...projects
          .filter((item) => item.visible)
          .slice(0, 3)
          .map((item) => {
            const article = el("article", "project-card");
            const visual = el("div", "project-visual");
            if (item.image) {
              const image = document.createElement("img");
              image.src = getSiteRoot() + item.image;
              image.alt = `${getLocalized(item, "title", lang) || item.title_en} figure`;
              image.loading = "lazy";
              visual.append(image);
            }
            article.append(
              visual,
              el("div", "project-meta", [item.period, item.lab].filter(Boolean).join(" | ")),
              el("h3", "", getLocalized(item, "title", lang) || item.title_en),
              el("p", "", getLocalized(item, "background", lang) || item.background_en || "")
            );
            return article;
          })
      );
    }

    const publicationRoot = document.querySelector("[data-home-publications]");
    if (publicationRoot) {
      clearAndAppend(
        publicationRoot,
        ...publications.filter((item) => item.selected).slice(0, 4).map((item, index) => buildPublicationItem(item, index + 1, lang))
      );
    }

    const highlightRoot = document.querySelector("[data-home-highlights]");
    if (highlightRoot) {
      const cards = [
        [getSiteRoot() + "publications.html", String(publications.length), lang === "zh" ? "论文发表" : "Publications"],
        [getSiteRoot() + "conferences.html", String(conferences.length), lang === "zh" ? "学术会议" : "Conferences"],
        [getSiteRoot() + "patents.html", String(patents.length), lang === "zh" ? "专利" : "Patents"],
        [getSiteRoot() + "awards.html", String(awards.length), lang === "zh" ? "奖励荣誉" : "Awards"]
      ].map(([href, value, label]) => {
        const card = el("a", "highlight-card");
        card.href = href;
        card.append(el("span", "highlight-value", value), el("span", "highlight-label", label));
        return card;
      });
      clearAndAppend(highlightRoot, ...cards);
    }

    const contactRoot = document.querySelector("[data-home-contact]");
    if (contactRoot) {
      const emailItem = el("div", "contact-item");
      emailItem.append(el("div", "contact-label", lang === "zh" ? "邮箱" : "Email"), makeEmailLink("", "address"));
      const locationItem = el("div", "contact-item");
      locationItem.append(
        el("div", "contact-label", lang === "zh" ? "所在地" : "Location"),
        el("span", "", profile.location?.[lang] || profile.location?.en || "")
      );
      clearAndAppend(contactRoot, emailItem, locationItem);
    }

    const contactLinks = document.querySelector("[data-home-contact-links]");
    if (contactLinks) {
      const nodes = ["google_scholar", "orcid", "homepage", "mntl"]
        .map((id) => getProfileLink(links, id))
        .filter((item) => item && item.url)
        .map((item) => {
          const anchor = el("a", "", item.label_en || item.label_zh || "");
          anchor.href = item.url;
          anchor.target = "_blank";
          anchor.rel = "noreferrer";
          return anchor;
        });
      clearAndAppend(contactLinks, ...nodes);
    }
  }

  function renderPublications(publications, lang) {
    const root = document.querySelector("[data-publications-list]");
    if (!root) return;
    const records = publications.filter((item) => item.type !== "conference" && item.type !== "conference_paper");
    const journalItems = records.filter((item) => item.type !== "manuscript");
    const manuscriptItems = records.filter((item) => item.type === "manuscript");
    const controlsRoot = document.querySelector("[data-publications-controls]");
    if (controlsRoot) clearAndAppend(controlsRoot, buildPublicationControls(root, journalItems, lang));
    clearAndAppend(root, ...journalItems.map((item, index) => buildPublicationItem(item, index + 1, lang)));
    updatePublicationYearHeadings(root);
    const manuscriptsRoot = document.querySelector("[data-manuscripts-root]");
    if (!manuscriptsRoot) return;
    if (!manuscriptItems.length) {
      clearAndAppend(
        manuscriptsRoot,
        el("p", "section-intro", lang === "zh" ? "当前公开网站内容中暂无额外列出的在投或准备中稿件。" : "No additional manuscripts are listed in the current public website content.")
      );
      return;
    }
    clearAndAppend(manuscriptsRoot, ...manuscriptItems.map((item, index) => buildPublicationItem(item, index + 1, lang)));
  }

  function buildPatentItem(item, lang) {
    const node = el("div", "section-item");
    const body = el("div", "item-body");
    const subtitle = el("div", "item-subtitle");
    subtitle.append(
      highlightLonglong(
        `${lang === "zh" ? "发明人" : "Inventors"}: ${item.inventors}. ${lang === "zh" ? "申请人" : "Applicant"}: ${item.applicant}.`
      )
    );
    const metaParts = [];
    const numbers = [item.patent_number, item.application_number].filter(Boolean).join(" / ");
    if (numbers) metaParts.push(`${lang === "zh" ? "专利号 / 申请号" : "Patent / Application No."}: ${numbers}`);
    if (item.status) metaParts.push(`${lang === "zh" ? "状态" : "Status"}: ${item.status}`);
    if (item.application_date_display) metaParts.push(`${lang === "zh" ? "申请日" : "Application date"}: ${item.application_date_display}`);
    if (item.grant_or_publication_date_display) metaParts.push(`${lang === "zh" ? "授权/公开日" : "Grant / publication date"}: ${item.grant_or_publication_date_display}`);
    body.append(
      el("div", "item-title", getLocalized(item, "title", lang) || item.title_en),
      subtitle,
      el("div", "item-description", metaParts.join(". ") + (metaParts.length ? "." : ""))
    );
    node.append(el("div", "item-period", item.date_display || ""), body);
    return node;
  }

  function renderPatents(patents, lang) {
    const root = document.querySelector("[data-patents-root]");
    if (!root) return;
    const groups = [
      {
        title: lang === "zh" ? "发明专利" : "Invention Patents",
        items: patents.filter((item) => item.patent_type === "granted_invention" || item.patent_type === "published_invention_application")
      },
      {
        title: lang === "zh" ? "实用新型专利" : "Utility Model Patents",
        items: patents.filter((item) => item.patent_type === "utility_model")
      }
    ];
    clearAndAppend(
      root,
      ...groups.map((group) => {
        const section = el("div", "subsection");
        const list = el("div", "section-list");
        group.items.forEach((item) => list.append(buildPatentItem(item, lang)));
        section.append(el("h3", "subsection-title", group.title), list);
        return section;
      })
    );
  }

  function buildConferenceItem(item, lang) {
    const node = el("div", "section-item");
    const body = el("div", "item-body");
    const authors = el("div", "conference-authors");
    authors.append(highlightLonglong(item.authors));
    body.append(
      el("div", "item-title", getLocalized(item, "title", lang) || item.title_en),
      authors,
      el("div", "conference-meta", [item.conference, item.location].filter(Boolean).join(", "))
    );
    if (item.link) {
      const desc = el("div", "item-description");
      const link = makeLinkChip("Link", item.link);
      if (link) desc.append(link);
      body.append(desc);
    }
    node.append(el("div", "item-period", String(item.year)), body);
    return node;
  }

  function renderConferences(conferences, lang) {
    const root = document.querySelector("[data-conferences-root]");
    if (!root) return;
    const groups = [
      [lang === "zh" ? "口头报告" : "Oral Presentations", conferences.filter((item) => item.presentation_type === "oral")],
      [lang === "zh" ? "海报展示" : "Poster Presentations", conferences.filter((item) => item.presentation_type === "poster")]
    ];
    clearAndAppend(
      root,
      ...groups.map(([title, items]) => {
        const section = el("div", "subsection");
        const list = el("div", "section-list");
        items.forEach((item) => list.append(buildConferenceItem(item, lang)));
        section.append(el("h3", "subsection-title", title), list);
        return section;
      })
    );
  }

  function renderAwards(awards, lang) {
    const root = document.querySelector("[data-awards-root]");
    if (!root) return;
    const groups = [
      ["scholarship", lang === "zh" ? "奖学金与资助" : "Scholarships & Fellowships", false],
      ["academic_honor", lang === "zh" ? "学术荣誉" : "Academic Honors", false],
      ["competition", lang === "zh" ? "竞赛与其他奖励" : "Competitions & Other Awards", true]
    ];
    clearAndAppend(
      root,
      ...groups
        .map(([key, title, optional]) => ({
          title,
          optional,
          items: awards.filter((item) => item.category === key || (key === "competition" && item.category === "other"))
        }))
        .filter((group) => !group.optional || group.items.length)
        .map((group) => {
          const section = el("div", "subsection");
          const list = el("div", "section-list awards-list");
          group.items.forEach((item) => {
            const node = el("div", "section-item");
            const body = el("div", "item-body");
            body.append(
              el("div", "item-title", getLocalized(item, "name", lang) || item.name_en),
              el("div", "item-subtitle", getLocalized(item, "description", lang) || item.level || item.organization || "")
            );
            node.append(el("div", "item-period", String(item.year)), body);
            list.append(node);
          });
          section.append(el("h3", "subsection-title", group.title), list);
          return section;
        })
    );
  }

  function renderProjects(projects, lang) {
    const root = document.querySelector("[data-projects-root]");
    if (!root) return;
    clearAndAppend(
      root,
      ...projects.filter((item) => item.visible).map((item) => {
        const article = el("article", "project-detail-card");
        if (item.image) {
          const img = document.createElement("img");
          img.className = "project-detail-image";
          img.src = getSiteRoot() + item.image;
          img.alt = `${getLocalized(item, "title", lang) || item.title_en} diagram`;
          img.loading = "lazy";
          article.append(img);
        }
        const content = el("div", "project-detail-content");
        content.append(
          el("div", "project-detail-meta", [item.period, item.lab].filter(Boolean).join(" | ")),
          el("h3", "", getLocalized(item, "title", lang) || item.title_en),
          el("p", "", `${lang === "zh" ? "背景" : "Background"}: ${getLocalized(item, "background", lang) || ""}`),
          el("p", "", `${lang === "zh" ? "技术路线" : "Technical route"}: ${getLocalized(item, "methods", lang) || ""}`),
          el("p", "", `${lang === "zh" ? "我的贡献" : "My contribution"}: ${getLocalized(item, "contribution", lang) || ""}`),
          el("p", "", `${lang === "zh" ? "代表性结果" : "Representative results"}: ${getLocalized(item, "result", lang) || ""}`)
        );
        article.append(content);
        return article;
      })
    );
  }

  function renderGallery(gallery, lang) {
    const root = document.querySelector("[data-gallery-root]");
    if (!root) return;
    clearAndAppend(
      root,
      ...gallery.map((item) => {
        const article = el("article", "gallery-entry");
        const image = document.createElement("img");
        image.className = "gallery-photo";
        image.src = getSiteRoot() + item.image;
        image.alt = getLocalized(item, "title", lang) || item.source_filename || "Gallery image";
        image.loading = "lazy";
        image.addEventListener("error", () => article.remove());
        article.append(
          el("div", "gallery-date", item.date_display || ""),
          image,
          el("div", "gallery-note", getLocalized(item, "title", lang) || item.source_filename || "")
        );
        return article;
      })
    );
  }

  function renderCv(profile, links, cv, publications, conferences, patents, lang) {
    const identity = document.querySelector("[data-cv-identity]");
    if (identity) {
      identity.querySelector("h2").textContent = profile.name?.[lang] || profile.name?.en || "";
      identity.querySelector(".cv-role").textContent = profile.position?.[lang] || profile.position?.en || "";
      identity.querySelector(".cv-affiliation").textContent = profile.affiliation?.[lang] || profile.affiliation?.en || "";
      identity.querySelector(".cv-location").textContent = profile.location?.[lang] || profile.location?.en || "";
    }

    const headerLinks = document.querySelector("[data-cv-header-links]");
    if (headerLinks) {
      const nodes = [makeEmailLink(lang === "zh" ? "邮箱" : "Email", lang === "zh" ? "邮箱" : "Email")];
      ["homepage", "google_scholar", "orcid", "mntl"].forEach((id) => {
        const item = getProfileLink(links, id);
        if (!item || !item.url) return;
        const anchor = makeLinkChip(item.label_en || item.label_zh || "", item.url);
        if (anchor) nodes.push(anchor);
      });
      clearAndAppend(headerLinks, ...nodes);
    }

    const actionsRoot = document.querySelector("[data-cv-actions]");
    if (actionsRoot) {
      const suffix = lang === "zh" ? "_ZH." : "_EN.";
      const academic = links.find((item) => item.type === "cv_download" && item.url && item.url.includes("Academic_CV") && item.url.includes(suffix));
      const resume = links.find((item) => item.type === "cv_download" && item.url && item.url.includes("Resume") && item.url.includes(suffix));
      const actions = [];
      if (academic) {
        const link = el("a", "button outline", lang === "zh" ? "下载完整学术简历" : "Download Full Academic CV");
        link.href = getSiteRoot() + academic.url;
        link.download = academic.url.split("/").pop() || "";
        actions.push(link);
      }
      if (resume) {
        const link = el("a", "button outline", lang === "zh" ? "下载 2 页简历" : "Download 2-page Resume");
        link.href = getSiteRoot() + resume.url;
        link.download = resume.url.split("/").pop() || "";
        actions.push(link);
      }
      clearAndAppend(actionsRoot, ...actions);
    }

    const profileRoot = document.querySelector("[data-cv-profile]");
    if (profileRoot && cv.profile && cv.profile[0]) {
      profileRoot.textContent = lang === "zh" ? cv.profile[0].description_zh || "" : cv.profile[0].description_en || "";
    }

    const educationRoot = document.querySelector("[data-cv-education]");
    if (educationRoot) {
      clearAndAppend(
        educationRoot,
        ...(cv.education || []).map((item) => el("li", "", `${item.year_or_period || ""} | ${lang === "zh" ? item.title_zh || item.title_en : item.title_en || item.title_zh}`))
      );
    }

    const researchRoot = document.querySelector("[data-cv-research-experience]");
    if (researchRoot) {
      clearAndAppend(
        researchRoot,
        ...(cv.research_experience || []).map((item) => el("li", "", lang === "zh" ? item.description_zh || "" : item.description_en || ""))
      );
    }

    const skillsRoot = document.querySelector("[data-cv-skills]");
    if (skillsRoot) {
      clearAndAppend(
        skillsRoot,
        ...(cv.technical_skills || []).map((item) => {
          const article = el("article", "skill-card");
          article.append(
            el("h4", "", lang === "zh" ? item.title_zh || item.title_en : item.title_en || item.title_zh),
            el("p", "", lang === "zh" ? item.description_zh || "" : item.description_en || "")
          );
          return article;
        })
      );
    }

    const projectRoot = document.querySelector("[data-cv-projects]");
    if (projectRoot) {
      clearAndAppend(
        projectRoot,
        ...(cv.selected_projects || []).map((item) => {
          const article = el("article", "project-detail-card");
          const content = el("div", "project-detail-content");
          content.append(
            el("div", "project-detail-meta", [item.year_or_period, item.organization].filter(Boolean).join(" | ")),
            el("h4", "", lang === "zh" ? item.title_zh || item.title_en : item.title_en || item.title_zh)
          );
          const list = el("ul", "cv-compact-list");
          splitCvBullets(lang === "zh" ? item.description_zh : item.description_en).forEach((bullet) => list.append(el("li", "", bullet)));
          content.append(list);
          article.append(content);
          return article;
        })
      );
    }

    const publicationRoot = document.querySelector("[data-cv-publications]");
    if (publicationRoot) {
      const mapped = (cv.selected_publications || [])
        .map((row) => publications.find((item) => item.title_en === row.title_en))
        .filter(Boolean);
      clearAndAppend(publicationRoot, ...mapped.map((item, index) => buildPublicationItem(item, index + 1, lang)));
    }

    const conferenceRoot = document.querySelector("[data-cv-conferences]");
    if (conferenceRoot) {
      const mapped = (cv.selected_conferences || [])
        .map((row) => conferences.find((item) => item.title_en === row.title_en))
        .filter(Boolean);
      clearAndAppend(conferenceRoot, ...mapped.map((item) => buildConferenceItem(item, lang)));
    }

    const patentRoot = document.querySelector("[data-cv-patents]");
    if (patentRoot) {
      const total = patents.length;
      const invention = patents.filter((item) => item.patent_type === "granted_invention" || item.patent_type === "published_invention_application").length;
      const granted = patents.filter((item) => item.patent_type === "granted_invention").length;
      const utility = patents.filter((item) => item.patent_type === "utility_model").length;
      const stats = el("div", "highlights-grid cv-highlights");
      [
        [String(total), lang === "zh" ? "总专利数" : "Total Patents"],
        [String(invention), lang === "zh" ? "发明专利" : "Invention Patents"],
        [String(granted), lang === "zh" ? "已授权发明" : "Granted Inventions"],
        [String(utility), lang === "zh" ? "实用新型" : "Utility Models"]
      ].forEach(([value, label]) => {
        const card = el("div", "highlight-card");
        card.append(el("span", "highlight-value", value), el("span", "highlight-label", label));
        stats.append(card);
      });
      const list = el("ul", "cv-compact-list");
      patents.slice(0, 4).forEach((item) => {
        const li = document.createElement("li");
        const strong = document.createElement("strong");
        strong.textContent = lang === "zh" ? item.title_zh || item.title_en : item.title_en || item.title_zh;
        li.append(strong, document.createElement("br"));
        li.append(`${item.status || ""}, ${item.patent_number || item.application_number || ""}, ${item.date_display || ""}.`);
        list.append(li);
      });
      const link = el("a", "section-link", lang === "zh" ? "查看完整专利档案" : "View full patent archive");
      link.href = getSiteRoot() + "patents.html";
      clearAndAppend(
        patentRoot,
        el("h3", "subsection-title", lang === "zh" ? "专利概览" : "Patent Summary"),
        stats,
        list,
        link
      );
    }

    const awardsRoot = document.querySelector("[data-cv-awards]");
    if (awardsRoot) {
      const timeline = el("div", "timeline");
      (cv.awards || []).slice(0, 4).forEach((item) => {
        const row = el("div", "timeline-item");
        const content = el("div", "timeline-content");
        row.append(el("div", "timeline-marker"), content);
        content.append(
          el("div", "timeline-period", item.year_or_period || ""),
          el("div", "timeline-title", lang === "zh" ? item.title_zh || item.title_en : item.title_en || item.title_zh),
          el("div", "timeline-subtitle", lang === "zh" ? item.description_zh || "" : item.description_en || "")
        );
        timeline.append(row);
      });
      clearAndAppend(
        awardsRoot,
        el("h3", "subsection-title", lang === "zh" ? "奖励荣誉" : "Awards"),
        timeline
      );
    }
  }

  async function init() {
    const lang = getLang();
    const page = document.body.dataset.page;
    try {
      if (page === "home-en" || page === "home-zh") {
        const [profile, links, projects, publications, conferences, patents, awards] = await Promise.all([
          loadJson("assets/data/profile.json"),
          loadJson("assets/data/links.json"),
          loadJson("assets/data/projects.json"),
          loadJson("assets/data/publications.json"),
          loadJson("assets/data/conferences.json"),
          loadJson("assets/data/patents.json"),
          loadJson("assets/data/awards.json")
        ]);
        renderHome(profile, links, projects, publications, conferences, patents, awards, lang);
        return;
      }
      if (page === "publications") {
        renderPublications(await loadJson("assets/data/publications.json"), lang);
        return;
      }
      if (page === "patents") {
        renderPatents(await loadJson("assets/data/patents.json"), lang);
        return;
      }
      if (page === "conferences") {
        renderConferences(await loadJson("assets/data/conferences.json"), lang);
        return;
      }
      if (page === "awards") {
        renderAwards(await loadJson("assets/data/awards.json"), lang);
        return;
      }
      if (page === "projects") {
        renderProjects(await loadJson("assets/data/projects.json"), lang);
        return;
      }
      if (page === "gallery") {
        renderGallery(await loadJson("assets/data/gallery.json"), lang);
        return;
      }
      if (page === "cv") {
        const [profile, links, cv, publications, conferences, patents] = await Promise.all([
          loadJson("assets/data/profile.json"),
          loadJson("assets/data/links.json"),
          loadJson("assets/data/cv.json"),
          loadJson("assets/data/publications.json"),
          loadJson("assets/data/conferences.json"),
          loadJson("assets/data/patents.json")
        ]);
        renderCv(profile, links, cv, publications, conferences, patents, lang);
      }
    } catch (error) {
      console.error(error);
      const selectors = {
        "home-en": "[data-home-root]",
        "home-zh": "[data-home-root]",
        publications: "[data-publications-list]",
        patents: "[data-patents-root]",
        conferences: "[data-conferences-root]",
        awards: "[data-awards-root]",
        projects: "[data-projects-root]",
        gallery: "[data-gallery-root]",
        cv: "[data-cv-root]"
      };
      showLoadError(document.querySelector(selectors[page] || ""), lang);
    }
  }

  window.SiteDataRenderer = { init };
})();
