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
    }
  }
}

const GALLERY_ITEMS = [
  { date: "2022.09.01", title: "抵达韩国", src: "assets/Albums/20220901_%E6%8A%B5%E8%BE%BE%E9%9F%A9%E5%9B%BD.jpg" },
  { date: "2022.11.19", title: "光州无等山", src: "assets/Albums/20221119_%E5%85%89%E5%B7%9E%E6%97%A0%E7%AD%89%E5%B1%B1.jpg" },
  { date: "2023.01.21", title: "过年", src: "assets/Albums/20230121_%E8%BF%87%E5%B9%B4.jpg" },
  { date: "2023.05.13", title: "Dongsu婚礼", src: "assets/Albums/20230513_Dongsu%E5%A9%9A%E7%A4%BC.jpg" },
  { date: "2023.07.30", title: "济州牛岛", src: "assets/Albums/20230730_%E6%B5%8E%E5%B7%9E%E7%89%9B%E5%B2%9B.jpg" },
  { date: "2023.08.23", title: "釜山广安里", src: "assets/Albums/20230823_%E9%87%9C%E5%B1%B1%E5%B9%BF%E5%AE%89%E9%87%8C.jpg" },
  { date: "2023.10.19", title: "波兰卡托维兹μTAS", src: "assets/Albums/20231019_%E6%B3%A2%E5%85%B0%E5%8D%A1%E6%89%98%E7%BB%B4%E5%85%B9%CE%BCTAS.jpg" },
  { date: "2023.12.16", title: "我和雪人", src: "assets/Albums/20231216_%E6%88%91%E5%92%8C%E9%9B%AA%E4%BA%BA.jpg" },
  { date: "2024.01.24", title: "茂朱滑雪", src: "assets/Albums/20240124_%E8%8C%82%E6%9C%B1%E6%BB%91%E9%9B%AA.jpg" },
  { date: "2024.03.16", title: "济州汉拿山", src: "assets/Albums/20240316_%E6%B5%8E%E5%B7%9E%E6%B1%89%E6%8B%BF%E5%B1%B1.jpg" },
  { date: "2024.04.10", title: "动物园", src: "assets/Albums/20240410_%E5%8A%A8%E7%89%A9%E5%9B%AD.jpg" },
  { date: "2024.08.03", title: "釜山海云台", src: "assets/Albums/20240803_%E9%87%9C%E5%B1%B1%E6%B5%B7%E4%BA%91%E5%8F%B0.jpg" },
  { date: "2024.11.16", title: "五等山顶", src: "assets/Albums/20241116_%E4%BA%94%E7%AD%89%E5%B1%B1%E9%A1%B6.jpg" },
  { date: "2024.11.22", title: "釜山海上烟花", src: "assets/Albums/20241122_%E9%87%9C%E5%B1%B1%E6%B5%B7%E4%B8%8A%E7%83%9F%E8%8A%B1.jpg" },
  { date: "2024.12.25", title: "圣诞节+汉拿山", src: "assets/Albums/20241225_%E5%9C%A3%E8%AF%9E%E8%8A%82%2B%E6%B1%89%E6%8B%BF%E5%B1%B1.jpg" },
  { date: "2025.01.29", title: "杭州径山", src: "assets/Albums/20250129_%E6%9D%AD%E5%B7%9E%E5%BE%84%E5%B1%B1.jpg" },
  { date: "2025.02.02", title: "大变财神", src: "assets/Albums/20250202_%E5%A4%A7%E5%8F%98%E8%B4%A2%E7%A5%9E.jpg" },
  { date: "2025.02.04", title: "福州添福", src: "assets/Albums/20250204_%E7%A6%8F%E5%B7%9E%E6%B7%BB%E7%A6%8F.jpg" },
  { date: "2025.02.27", title: "RLRC最佳研究生", src: "assets/Albums/20250227_RLRC%E6%9C%80%E4%BD%B3%E7%A0%94%E7%A9%B6%E7%94%9F.jpg" },
  { date: "2025.03.09", title: "羽毛球比赛", src: "assets/Albums/20250309_%E7%BE%BD%E6%AF%9B%E7%90%83%E6%AF%94%E8%B5%9B.jpg" },
  { date: "2025.03.28", title: "济州枪击", src: "assets/Albums/20250328_%E6%B5%8E%E5%B7%9E%E6%9E%AA%E5%87%BB.jpg" },
  { date: "2025.05.04", title: "浦项SpaceWalk", src: "assets/Albums/20250504_%E6%B5%A6%E9%A1%B9SpaceWalk.jpg" },
  { date: "2025.05.24", title: "Dr.Nomin", src: "assets/Albums/20250524_Dr.Nomin.jpg" },
  { date: "2025.08.26", title: "BK FellowShip 奖学金", src: "assets/Albums/20250826_BK%20FellowShip%20%E5%A5%96%E5%AD%A6%E9%87%91.jpg" },
  { date: "2025.08.28", title: "MNTL谭阳", src: "assets/Albums/20250828_MNTL%E8%B0%AD%E9%98%B3.jpg" },
  { date: "2025.10.02", title: "楠哥婚礼", src: "assets/Albums/20251002_%E6%A5%A0%E5%93%A5%E5%A9%9A%E7%A4%BC.jpg" },
  { date: "2025.10.07", title: "米菲70周年", src: "assets/Albums/20251007_%E7%B1%B3%E8%8F%B270%E5%91%A8%E5%B9%B4.jpg" },
  { date: "2025.10.27", title: "温哥华SENSORS", src: "assets/Albums/20251027_%E6%B8%A9%E5%93%A5%E5%8D%8ESENSORS.jpg" },
  { date: "2025.11.15", title: "釜山烟花节", src: "assets/Albums/20251115_%E9%87%9C%E5%B1%B1%E7%83%9F%E8%8A%B1%E8%8A%82.jpg" },
  { date: "2025.11.26", title: "大变圣诞老人", src: "assets/Albums/20251126_%E5%A4%A7%E5%8F%98%E5%9C%A3%E8%AF%9E%E8%80%81%E4%BA%BA.jpg" },
  { date: "2026.01.06", title: "BK+统营", src: "assets/Albums/20260106_BK%2B%E7%BB%9F%E8%90%A5.jpg" },
  { date: "2026.02.01", title: "智异山", src: "assets/Albums/20260201_%E6%99%BA%E5%BC%82%E5%B1%B1.jpg" },
  { date: "2026.02.23", title: "马头人滑雪", src: "assets/Albums/20260223_%E9%A9%AC%E5%A4%B4%E4%BA%BA%E6%BB%91%E9%9B%AA.jpg" },
  { date: "2026.03.28", title: "济州卡丁车", src: "assets/Albums/20260328_%E6%B5%8E%E5%B7%9E%E5%8D%A1%E4%B8%81%E8%BD%A6.jpg" },
  { date: "2026.03.29", title: "蛋糕人", src: "assets/Albums/20260329_%E8%9B%8B%E7%B3%95%E4%BA%BA.jpg" }
];

function renderGallery() {
  const container = document.querySelector("[data-gallery-root]");
  if (!container) return;

  const prefix = container.dataset.galleryPrefix || "";
  const fragment = document.createDocumentFragment();

  for (const item of GALLERY_ITEMS) {
    const article = document.createElement("article");
    article.className = "gallery-entry";

    const date = document.createElement("div");
    date.className = "gallery-date";
    date.textContent = item.date;

    const image = document.createElement("img");
    image.className = "gallery-photo";
    image.src = prefix + item.src;
    image.alt = item.title;
    image.loading = "lazy";

    const note = document.createElement("div");
    note.className = "gallery-note";
    note.textContent = item.title;

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
renderGallery();
formatPublicationItems();
formatConferenceItems();
setActiveNavigation();
