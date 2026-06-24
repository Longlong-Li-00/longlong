function initAvatarFallback() {
  const avatar = document.querySelector("[data-avatar]");
  if (!avatar) return;
  const img = avatar.querySelector("img");
  if (!img) return;
  img.addEventListener("error", () => {
    img.classList.add("is-hidden");
    avatar.classList.add("no-image");
  });
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

(async () => {
  if (window.SiteDataRenderer && typeof window.SiteDataRenderer.init === "function") {
    await window.SiteDataRenderer.init();
  }
  initAvatarFallback();
  hydrateEmailLinks();
  bindAnalyticsEvents();
  setActiveNavigation();
})();
