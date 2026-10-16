(function () {
  "use strict";

  window.CONNECT_PROFILE = Object.freeze({
    identity: Object.freeze({
      name: "Longlong Li",
      title: "PhD Researcher",
      institution: "Chonnam National University",
      profileImage: "/assets/profile-connect.webp",
      profileImageAlt: "Longlong Li at IEEE SENSORS 2025",
    }),
    contact: Object.freeze({
      email: "lilonglong2209@gmail.com",
      website: "https://longlongli.com",
      linkedin: "https://www.linkedin.com/in/longlong-li-11a7123a2/",
      scholar: "https://scholar.google.com/citations?user=eehgHYgAAAAJ&hl=en",
      orcid: "https://orcid.org/0009-0008-4062-5191",
    }),
    research: Object.freeze({
      areas: Object.freeze([
        "Engineered Heart Tissue",
        "Cardiac Organ-on-Chip",
        "Electromechanical Biosensing",
      ]),
      statement:
        "Developing engineered cardiac tissue platforms for simultaneous mechanical and electrophysiological monitoring, with applications in cardiac disease modeling, drug screening, and cardiotoxicity assessment.",
      interests: Object.freeze([
        "EHT",
        "Organ-on-Chip",
        "Biosensing",
        "Cardiotoxicity",
        "Drug Screening",
        "Disease Modeling",
      ]),
    }),
    conference: Object.freeze({
      name: "MicroTAS 2026",
      type: "Poster",
      posterTitle:
        "A Flexible Electromechanical Sensing Platform for In Vitro Hypoxic Cardiac Tissue Models",
      posterUrl: "/assets/conference/microtas2026/uTAS_poster_longlong_261015.pdf",
      posterThumbnail: "/assets/conference/microtas2026/poster-thumb.webp",
      posterThumbnailAlt:
        "MicroTAS 2026 poster showing a flexible electromechanical sensing platform for hypoxic cardiac tissue models",
    }),
    footerMessage: "Open to research discussions and collaborations.",
    vcardFilename: "Longlong_Li.vcf",
  });
})();
