# Longlong Li Academic Website

This repository contains the bilingual personal academic website of Longlong Li. The site is a static GitHub Pages website with an Excel-driven content workflow for structured academic records.

## Project overview

The website is maintained as a static site:

- English pages are in the project root.
- Chinese pages are in `zh/`.
- Shared rendering logic is handled by JavaScript.
- Structured content is maintained in Excel and converted into generated JSON files.

## Content maintenance workflow

The current content pipeline is:

```text
data/website_content.xlsx
→ tools/generate_site_data.py
→ assets/data/*.json
→ scripts/data-renderer.js
→ HTML pages
```

For normal updates, edit the Excel workbook first and then regenerate the JSON files.

## Local preview

Run the following commands from the project root:

```bash
python tools\generate_site_data.py
python -m http.server 8020
```

Then open:

```text
http://127.0.0.1:8020/index.html
```

You can also use:

```bash
preview-local.cmd
```

## Common maintenance notes

- Do not preview the site by double-clicking HTML files. The website loads JSON with `fetch()`, so it requires a local HTTP server.
- After editing `data/website_content.xlsx`, you must rerun `python tools\generate_site_data.py`.
- Do not manually edit `assets/data/*.json`. These files are generated outputs.
- If a webpage does not reflect your update, first check whether the corresponding JSON file in `assets/data/` was regenerated.
- If a keyword exists in Excel but you are not sure whether it reached the generated data, run:

```bash
python tools\check_content_update.py "keyword"
```

## Deployment

The website is deployed with GitHub Pages.

The canonical deployment branch is now `main`.

The GitHub Actions workflow will:

1. Install Python dependencies from `requirements.txt`
2. Run the site data generation workflow
3. Upload the static site as the GitHub Pages artifact

GitHub Actions deploys from `main`.

The site remains a static website. There is no backend or CMS.

## Normal update workflow

For future content maintenance, use `main` as the only normal update branch:

```bash
git checkout main
git pull origin main

# edit data/website_content.xlsx

python tools\generate_site_data.py
python tools\generate_cv_docs.py

python -m http.server 8020

git status
git add .
git commit -m "content: update website data"
git push origin main
```

Important:

- Do not continue using `master` for new content updates.
- Do not push to `master`.
- Do not force push.
- Do not manually edit `assets/data/*.json`; edit `data/website_content.xlsx` and regenerate JSON.
- If CV content changes, regenerate CV documents before commit.

## High-level folder overview

- `data/`: Excel content source
- `assets/data/`: generated JSON payloads
- `assets/Project/`: project images
- `assets/CV/`: downloadable CV and resume files
- `assets/albums/` and `assets/albums-optimized/`: gallery images
- `scripts/`: frontend rendering logic
- `tools/`: content generation and maintenance tools
- `docs/`: maintenance and deployment documentation

## Important restriction

Do not move or rename assets casually. If image or document paths change, the related Excel rows, generated JSON, HTML references, JavaScript logic, and deployment workflow may all need to be updated together.
