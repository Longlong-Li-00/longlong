# Project Structure

This document explains the current structure of the Longlong Li academic website project and clarifies which files are edited manually versus generated automatically.

## Current architecture

The website is an Excel-driven static site. The main content flow is:

```text
data/website_content.xlsx
→ tools/generate_site_data.py
→ assets/data/*.json
→ scripts/data-renderer.js
→ English / Chinese HTML pages
```

## Main folders

- `./`
  English root HTML pages and shared static files
- `zh/`
  Chinese pages
- `assets/`
  Images, downloadable CV files, and generated JSON data
- `data/`
  Excel content source
- `scripts/`
  Frontend rendering scripts
- `tools/`
  Content generation and helper scripts
- `docs/`
  Maintenance and deployment documentation
- `.github/workflows/`
  GitHub Pages deployment workflow

## Manually maintained files

These files or folders are expected to be edited manually:

- `data/website_content.xlsx`
- `assets/Project/` project images
- gallery image folders such as `assets/albums/`
- `assets/CV/` CV and resume PDF files
- `README.md`
- files under `docs/`

The downloadable CV files are not edited manually in normal maintenance. They are generated into `assets/CV/` by `tools/generate_cv_docs.py` after `assets/data/*.json` has been refreshed.

## Automatically generated files

These files are generated outputs and should usually not be edited manually:

- `assets/data/profile.json`
- `assets/data/publications.json`
- `assets/data/patents.json`
- `assets/data/conferences.json`
- `assets/data/awards.json`
- `assets/data/projects.json`
- `assets/data/gallery.json`
- `assets/data/cv.json`
- `assets/data/links.json`

Regenerate them with:

```bash
python tools\generate_site_data.py
```

## Core scripts

- `tools/generate_site_data.py`
  Main Excel-to-JSON generator used by local maintenance and GitHub Pages deployment.
- `tools/extract_site_content_to_excel.py`
  Reverse extraction helper for rebuilding or auditing the Excel workbook from an existing website snapshot.
- `tools/check_content_update.py`
  Search helper for checking whether a keyword exists in the Excel source and generated JSON files.
- `tools/generate_cv_docs.py`
  Generates the active Academic CV and 2-page Resume DOCX/PDF files from `assets/data/*.json`. Run this after `tools/generate_site_data.py` when Excel changes should be reflected in downloadable CV files.
- `scripts/data-renderer.js`
  Frontend content renderer that reads `assets/data/*.json` and injects structured content into HTML pages.
- `scripts.js`
  Shared frontend initializer for avatar fallback, email hydration, analytics binding, and navigation highlighting.

## Page files

### English root pages

- `index.html`
- `publications.html`
- `patents.html`
- `conferences.html`
- `awards.html`
- `projects.html`
- `gallery.html`
- `cv.html`

### Chinese pages

- `zh/index.html`
- `zh/publications.html`
- `zh/patents.html`
- `zh/conferences.html`
- `zh/awards.html`
- `zh/projects.html`
- `zh/gallery.html`
- `zh/cv.html`

## Asset handling note

Do not move files under `assets/` casually.

If you move or rename images or downloadable files, you must verify and update every affected reference, which may include:

- `data/website_content.xlsx`
- generated JSON files under `assets/data/`
- HTML page references
- frontend JavaScript
- Python maintenance scripts
- deployment workflow assumptions

Until a full path normalization pass is completed, the safest rule is:

```text
Do not move assets unless you are intentionally performing a coordinated path update.
```
