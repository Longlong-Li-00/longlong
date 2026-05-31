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

  for (const item of items) {
    const content = item.querySelector(".pub-content");
    if (!content || content.dataset.formatted === "true") continue;

    const title = content.querySelector(".pub-title");
    const authors = content.querySelector(".pub-authors");
    const venue = content.querySelector(".pub-venue");
    const year = content.querySelector(".pub-year");
    const links = [...content.querySelectorAll(":scope > a")];

    if (!title || !authors) continue;

    const meta = document.createElement("div");
    meta.className = "pub-meta";
    meta.textContent = [venue?.textContent?.trim(), year?.textContent?.trim()].filter(Boolean).join(" ");

    const linksWrap = document.createElement("div");
    linksWrap.className = "pub-links";
    for (const link of links) {
      link.textContent = "Link";
      linksWrap.append(link);
    }

    const nextChildren = [title, authors];
    if (meta.textContent) nextChildren.push(meta);
    if (linksWrap.childElementCount) nextChildren.push(linksWrap);

    content.replaceChildren(...nextChildren);
    content.dataset.formatted = "true";
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
formatConferenceItems();
setActiveNavigation();
