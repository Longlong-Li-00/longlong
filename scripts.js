const avatar = document.querySelector("[data-avatar]");
if (avatar) {
  const img = avatar.querySelector("img");
  if (img) {
    img.addEventListener("error", () => {
      img.classList.add("is-hidden");
      avatar.classList.add("no-image");
    });
  }
}

function hydrateEmailLinks() {
  const emailLinks = document.querySelectorAll("[data-email-link]");
  if (!emailLinks.length) return;

  for (const link of emailLinks) {
    const user = link.dataset.emailUser || "";
    const domainName = link.dataset.emailDomainName || "";
    const domainTld = link.dataset.emailDomainTld || "";

    if (!user || !domainName || !domainTld) continue;

    const address = `${user}@${domainName}.${domainTld}`;
    link.href = `mailto:${address}`;

    if (link.dataset.emailText === "address") {
      link.textContent = address;
    } else {
      link.textContent = link.dataset.emailText || "Email";
    }
  }
}

function bindAnalyticsEvents() {
  const links = document.querySelectorAll("[data-analytics-event]");
  if (!links.length) return;

  for (const link of links) {
    link.addEventListener("click", () => {
      // Cloudflare Web Analytics handles page-level traffic automatically.
      // These hooks are kept for optional GA4/custom event tracking if enabled later.
      if (typeof window.gtag === "function") {
        window.gtag("event", link.dataset.analyticsEvent || "link_click", {
          event_category: link.dataset.analyticsCategory || "engagement",
          event_label: link.dataset.analyticsLabel || link.textContent?.trim() || "link",
          transport_type: "beacon"
        });
      }
    });
  }
}

function textOf(element) {
  return element?.textContent?.replace(/\s+/g, " ").trim() || "";
}

function classifyPublicationTopic(title, venue) {
  const source = `${title} ${venue}`.toLowerCase();
  if (source.includes("machine learning")) {
    return "Machine Learning";
  }
  if (source.includes("graphene") || source.includes("cardiomyocyte") || source.includes("cardiac")) {
    return "Cardiac Tissue";
  }
  if (source.includes("sensor") || source.includes("sensing") || source.includes("field potential") || source.includes("acetone") || source.includes("e-nose")) {
    return "Biosensing";
  }
  if (source.includes("su-8") || source.includes("micromechanics") || source.includes("mems") || source.includes("micro")) {
    return "BioMEMS";
  }
  if (source.includes("hydrogel") || source.includes("bioink") || source.includes("curcumin") || source.includes("scaffold")) {
    return "Biomaterials";
  }
  return "BioMEMS";
}

function makeBibtexKey(title, year) {
  const firstWord = title
    .replace(/[^a-zA-Z0-9\s-]/g, "")
    .trim()
    .split(/\s+/)[0] || "publication";
  return `li${year || "year"}${firstWord}`;
}

function makeBibtex({ title, authors, venue, year }) {
  const cleanYear = (year.match(/\b(20\d{2})\b/) || [])[1] || "YEAR";
  const cleanVenue = venue.replace(/,$/, "") || "JOURNAL";
  const key = makeBibtexKey(title, cleanYear);
  return [
    `@article{${key},`,
    `  title = {${title || "TITLE"}},`,
    `  author = {${authors || "AUTHORS"}},`,
    `  journal = {${cleanVenue}},`,
    `  year = {${cleanYear}},`,
    `  note = {Please verify volume, issue, pages, and DOI before reuse.}`,
    `}`
  ].join("\n");
}

async function loadGalleryItems(source) {
  const response = await fetch(source, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Failed to load gallery data: ${response.status}`);
  }

  const items = await response.json();
  return Array.isArray(items) ? items : [];
}

async function renderGallery() {
  const container = document.querySelector("[data-gallery-root]");
  if (!container) return;

  const source = container.dataset.gallerySource || "assets/gallery-data.json";
  const prefix = container.dataset.galleryPrefix || "";
  const fragment = document.createDocumentFragment();
  let items = [];

  try {
    items = await loadGalleryItems(source);
  } catch (error) {
    console.error(error);
    container.replaceChildren();
    return;
  }

  for (const item of items) {
    const article = document.createElement("article");
    article.className = "gallery-entry";

    const date = document.createElement("div");
    date.className = "gallery-date";
    date.textContent = item.date || "Undated";

    const image = document.createElement("img");
    image.className = "gallery-photo";
    image.src = prefix + item.src;
    image.alt = item.title || item.filename || "Gallery image";
    image.loading = "lazy";
    image.addEventListener("error", () => {
      article.remove();
    });

    const note = document.createElement("div");
    note.className = "gallery-note";
    note.textContent = item.title || item.filename || "Untitled image";

    article.append(date, image, note);
    fragment.append(article);
  }

  container.replaceChildren(fragment);
}

function formatPublicationItems() {
  const items = document.querySelectorAll(".pub-item");
  if (!items.length) return;
  const isPublicationArchive = document.body.dataset.page === "publications";

  for (const item of items) {
    const content = item.querySelector(".pub-content");
    if (!content || content.dataset.formatted === "true") continue;

    const title = content.querySelector(".pub-title");
    const authors = content.querySelector(".pub-authors");
    const venue = content.querySelector(".pub-venue");
    const year = content.querySelector(".pub-year");
    const links = [...content.querySelectorAll(":scope > a")];

    if (!title || !authors) continue;

    const titleText = textOf(title);
    const authorsText = textOf(authors).replace(/\.$/, "");
    const venueText = textOf(venue);
    const yearText = textOf(year);
    const yearValue = (yearText.match(/\b(20\d{2})\b/) || [])[1] || "";
    const topic = item.dataset.topic || classifyPublicationTopic(titleText, venueText);
    const selected = authorsText.startsWith("Longlong Li") || titleText.toLowerCase().includes("graphene su-8");

    if (isPublicationArchive) {
      item.dataset.year = item.dataset.year || yearValue;
      item.dataset.topic = topic;
      item.dataset.selected = selected ? "true" : "false";
    }

    const meta = document.createElement("div");
    meta.className = "pub-meta";
    meta.textContent = [venueText, yearText].filter(Boolean).join(" ");

    const tags = document.createElement("div");
    tags.className = "pub-tags";
    if (isPublicationArchive) {
      for (const value of [yearValue, topic, selected ? "Selected" : ""]) {
        if (!value) continue;
        const tag = document.createElement("span");
        tag.textContent = value;
        tags.append(tag);
      }
    }

    const linksWrap = document.createElement("div");
    linksWrap.className = "pub-links";
    for (const link of links) {
      link.textContent = "Link";
      linksWrap.append(link);
    }

    const nextChildren = [title, authors];
    if (meta.textContent) nextChildren.push(meta);
    if (tags.childElementCount) nextChildren.push(tags);
    if (linksWrap.childElementCount) nextChildren.push(linksWrap);
    if (isPublicationArchive) {
      const citation = document.createElement("details");
      citation.className = "citation-block";
      const summary = document.createElement("summary");
      summary.textContent = "BibTeX";
      const pre = document.createElement("pre");
      pre.textContent = makeBibtex({
        title: titleText,
        authors: authorsText,
        venue: venueText,
        year: yearText
      });
      citation.append(summary, pre);
      nextChildren.push(citation);
    }

    content.replaceChildren(...nextChildren);
    content.dataset.formatted = "true";
  }
}

function setupPublicationControls() {
  if (document.body.dataset.page !== "publications") return;
  const list = document.querySelector(".pub-list");
  if (!list || document.querySelector(".publication-controls")) return;

  const isZh = document.documentElement.lang === "zh";
  const items = [...list.querySelectorAll(".pub-item")];
  const years = [...new Set(items.map((item) => item.dataset.year).filter(Boolean))].sort((a, b) => b.localeCompare(a));
  const controls = document.createElement("div");
  controls.className = "publication-controls";
  controls.innerHTML = `<span>${isZh ? "筛选" : "Filter"}</span>`;

  const addButton = (label, type, value) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.dataset.filterType = type;
    button.dataset.filterValue = value;
    if (value === "all") button.classList.add("is-active");
    controls.append(button);
  };

  addButton(isZh ? "全部" : "All", "all", "all");
  for (const year of years) addButton(year, "year", year);

  list.before(controls);

  const applyFilter = (type, value) => {
    controls.querySelectorAll("button").forEach((button) => {
      button.classList.toggle("is-active", button.dataset.filterType === type && button.dataset.filterValue === value);
    });

    for (const item of items) {
      const show = value === "all" || item.dataset[type] === value;
      item.hidden = !show;
    }

    updatePublicationYearHeadings(list);
  };

  controls.addEventListener("click", (event) => {
    const button = event.target.closest("button");
    if (!button) return;
    applyFilter(button.dataset.filterType, button.dataset.filterValue);
  });

  updatePublicationYearHeadings(list);
}

function updatePublicationYearHeadings(list) {
  list.querySelectorAll(".pub-year-heading").forEach((heading) => heading.remove());

  let lastYear = "";
  const items = [...list.querySelectorAll(".pub-item")].filter((item) => !item.hidden);
  for (const item of items) {
    const year = item.dataset.year || "Undated";
    if (year === lastYear) continue;
    const heading = document.createElement("li");
    heading.className = "pub-year-heading";
    heading.textContent = year;
    item.before(heading);
    lastYear = year;
  }
}

function formatConferenceItems() {
  const roots = document.querySelectorAll("[data-conference-root]");
  if (!roots.length) return;

  for (const root of roots) {
    const items = root.querySelectorAll(".section-item .item-body");
    for (const body of items) {
      const subtitle = body.querySelector(".item-subtitle");
      if (!subtitle || body.querySelector(".conference-authors")) continue;

      const parts = subtitle.innerHTML.split(/\s*\|\s*/);
      if (parts.length < 2) continue;

      const meta = document.createElement("div");
      meta.className = "conference-meta";
      meta.innerHTML = parts[0].trim();

      const authors = document.createElement("div");
      authors.className = "conference-authors";
      authors.innerHTML = parts.slice(1).join(" | ").trim();

      const link = body.querySelector(".item-description a");
      if (link) {
        link.textContent = "Link";
      }

      subtitle.replaceWith(authors, meta);
    }
  }
}

function setActiveNavigation() {
  const links = [...document.querySelectorAll("[data-nav-key]")];
  if (!links.length) return;

  const pageKey = document.body.dataset.page || "about";
  let activeKey = pageKey;

  if ((pageKey === "home-en" || pageKey === "home-zh") && window.location.hash) {
    activeKey = window.location.hash.slice(1);
  }

  if (pageKey === "home-en" || pageKey === "home-zh") {
    const sectionKeys = ["about", "research", "projects", "contact"];
    const sections = sectionKeys
      .map((key) => document.getElementById(key))
      .filter(Boolean);

    if (!window.location.hash && sections.length) {
      activeKey = "about";
    }

    if ("IntersectionObserver" in window && sections.length) {
      const observer = new IntersectionObserver(
        (entries) => {
          const visible = entries
            .filter((entry) => entry.isIntersecting)
            .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

          if (!visible) return;
          const key = visible.target.id;
          links.forEach((link) => link.classList.toggle("is-active", link.dataset.navKey === key));
        },
        {
          rootMargin: "-25% 0px -55% 0px",
          threshold: [0.2, 0.4, 0.6]
        }
      );

      sections.forEach((section) => observer.observe(section));
    }
  }

  links.forEach((link) => link.classList.toggle("is-active", link.dataset.navKey === activeKey));
}

hydrateEmailLinks();
bindAnalyticsEvents();
renderGallery();
formatPublicationItems();
setupPublicationControls();
formatConferenceItems();
setActiveNavigation();
