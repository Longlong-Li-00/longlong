(function () {
  "use strict";

  const profile = window.CONNECT_PROFILE;
  if (!profile) {
    document.documentElement.classList.add("profile-load-error");
    return;
  }

  const one = (selector) => document.querySelector(selector);
  const all = (selector) => [...document.querySelectorAll(selector)];
  const setText = (selector, value) => {
    const element = one(selector);
    if (element) element.textContent = value;
  };

  function setExternalLink(element, url, label) {
    element.href = url;
    element.target = "_blank";
    element.rel = "noopener noreferrer";
    element.setAttribute("aria-label", `${label} (opens in a new tab)`);
  }

  function escapeVcard(value) {
    return String(value)
      .replace(/\\/g, "\\\\")
      .replace(/\n/g, "\\n")
      .replace(/;/g, "\\;")
      .replace(/,/g, "\\,");
  }

  function buildVcard() {
    const { identity, contact, research, conference } = profile;
    const note = `${research.areas.join("; ")}. ${conference.name} poster: ${conference.posterTitle}.`;
    return [
      "BEGIN:VCARD",
      "VERSION:3.0",
      "N:Li;Longlong;;;",
      `FN:${escapeVcard(identity.name)}`,
      `TITLE:${escapeVcard(identity.title)}`,
      `ORG:${escapeVcard(identity.institution)}`,
      `EMAIL;TYPE=INTERNET:${contact.email}`,
      `URL:${contact.website}`,
      `URL:${contact.linkedin}`,
      `URL:${contact.scholar}`,
      `URL:${contact.orcid}`,
      `NOTE:${escapeVcard(note)}`,
      "END:VCARD",
      "",
    ].join("\r\n");
  }

  function downloadVcard() {
    const status = one("[data-action-status]");
    const blob = new Blob([buildVcard()], { type: "text/vcard;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = profile.vcardFilename;
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1500);
    if (status) {
      status.textContent = "Contact file ready — open it to add Longlong Li to your address book.";
      window.setTimeout(() => {
        status.textContent = "";
      }, 6000);
    }
  }

  function render() {
    const { identity, contact, research, conference } = profile;

    setText("[data-name]", identity.name);
    setText("[data-title]", identity.title);
    setText("[data-institution]", identity.institution);
    setText("[data-research-areas]", research.areas.join(" · "));
    setText("[data-research-statement]", research.statement);
    setText("[data-conference-name]", conference.name);
    setText("[data-conference-type]", conference.type);
    setText("[data-poster-title]", conference.posterTitle);
    setText("[data-footer-message]", profile.footerMessage);

    const portrait = one("[data-profile-image]");
    portrait.src = identity.profileImage;
    portrait.alt = identity.profileImageAlt;
    portrait.addEventListener("error", () => {
      one("[data-portrait-wrap]")?.classList.add("image-unavailable");
    });

    const thumbnail = one("[data-poster-thumbnail]");
    thumbnail.src = conference.posterThumbnail;
    thumbnail.alt = conference.posterThumbnailAlt;
    thumbnail.addEventListener("error", () => {
      one("[data-poster-visual]")?.classList.add("image-unavailable");
    });

    all("[data-link]").forEach((element) => {
      const type = element.dataset.link;
      if (type === "email") {
        element.href = `mailto:${contact.email}`;
        element.setAttribute("aria-label", `Email ${identity.name}`);
        return;
      }
      const labels = {
        website: "Open Longlong Li's website",
        linkedin: "Open Longlong Li's LinkedIn profile",
        scholar: "Open Longlong Li's Google Scholar profile",
        orcid: "Open Longlong Li's ORCID profile",
      };
      setExternalLink(element, contact[type], labels[type]);
    });

    const posterLink = one("[data-poster-link]");
    if (conference.posterUrl) {
      setExternalLink(posterLink, conference.posterUrl, `View ${conference.name} poster`);
    } else {
      posterLink.removeAttribute("href");
      posterLink.classList.add("is-disabled");
      posterLink.setAttribute("aria-disabled", "true");
      posterLink.querySelector("span").textContent = "Poster coming soon";
    }

    const tags = one("[data-interest-tags]");
    research.interests.forEach((interest) => {
      const item = document.createElement("li");
      item.textContent = interest;
      tags.append(item);
    });

    const structuredData = document.createElement("script");
    structuredData.type = "application/ld+json";
    structuredData.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Person",
      name: identity.name,
      jobTitle: identity.title,
      affiliation: { "@type": "CollegeOrUniversity", name: identity.institution },
      email: `mailto:${contact.email}`,
      url: contact.website,
      sameAs: [contact.linkedin, contact.scholar, contact.orcid],
      knowsAbout: research.areas,
    });
    document.head.append(structuredData);

    one("[data-save-contact]").addEventListener("click", downloadVcard);
    document.documentElement.classList.add("profile-loaded");
  }

  render();
})();
