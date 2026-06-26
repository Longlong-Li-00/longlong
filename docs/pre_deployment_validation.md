# Pre-deployment Validation

Validation date: 2026-06-26

## Branch and commits

- Branch: `project-structure-cleanup`
- Latest validated commit before this report: `ef7f14a fix: align conference presentation types across data and CV`
- Required cleanup commits are present in the current branch history:
  - `77e0166 docs: add website maintenance and preview workflow`
  - `0a926a7 chore: document cleanup review and remove temporary files`
  - `5d58f42 docs: audit website assets and references`
  - `6127e31 chore: unify gallery data source`
  - `39718c5 docs: audit CV files and references`
  - `8e0acba chore: archive unused legacy CV files`
  - `2a52509 feat: sync generated CV documents with website data`
  - `ef7f14a fix: align conference presentation types across data and CV`

## Data generation results

Commands run:

```bash
python tools\generate_site_data.py
python tools\check_content_update.py "KMEMS"
python tools\generate_cv_docs.py
node --check scripts.js
node --check scripts/data-renderer.js
```

Results:

- `assets/data/*.json` regenerated successfully.
- `KMEMS` was found in the Excel source and generated JSON.
- CV documents regenerated successfully.
- JavaScript syntax checks passed.
- `generate_site_data.py` reported 51 validation warnings, all tied to optional blank fields such as publication DOI/pages/issue fields and gallery category fields.

## JSON record counts

| Dataset | Count |
|---|---:|
| Publications | 9 |
| Patents | 15 |
| Conferences | 12 |
| Awards | 12 |
| Projects | 3 |
| Gallery | 36 |
| Links | 25 |

## CV generation results

Generated active CV files:

- `assets/CV/Longlong_Li_Academic_CV_EN.docx`
- `assets/CV/Longlong_Li_Academic_CV_EN.pdf`
- `assets/CV/Longlong_Li_Academic_CV_ZH.docx`
- `assets/CV/Longlong_Li_Academic_CV_ZH.pdf`
- `assets/CV/Longlong_Li_Resume_EN.docx`
- `assets/CV/Longlong_Li_Resume_EN.pdf`
- `assets/CV/Longlong_Li_Resume_ZH.docx`
- `assets/CV/Longlong_Li_Resume_ZH.pdf`

PDF checks:

- English Academic CV: 4 pages, includes `KMEMS`, no `H. Sun`.
- Chinese Academic CV: 4 pages, includes `KMEMS`, no `H. Sun`.
- English Resume: 2 pages, no `H. Sun`.
- Chinese Resume: 2 pages, no `H. Sun`.

The four website download PDF targets exist under `assets/CV/`.

## Page availability checks

All checked pages returned HTTP 200 from a local static HTTP server:

- `index.html`
- `publications.html`
- `patents.html`
- `conferences.html`
- `awards.html`
- `projects.html`
- `gallery.html`
- `cv.html`
- `zh/index.html`
- `zh/publications.html`
- `zh/patents.html`
- `zh/conferences.html`
- `zh/awards.html`
- `zh/projects.html`
- `zh/gallery.html`
- `zh/cv.html`

All checked JSON resources returned HTTP 200:

- `assets/data/profile.json`
- `assets/data/publications.json`
- `assets/data/patents.json`
- `assets/data/conferences.json`
- `assets/data/awards.json`
- `assets/data/projects.json`
- `assets/data/gallery.json`
- `assets/data/cv.json`
- `assets/data/links.json`

Representative browser checks were also run on English and Chinese homepage, conferences, gallery, and CV pages. No console errors, broken images, or visible data-load fallback messages were observed on those representative pages.

## Content consistency checks

- Homepage highlights now show 9 publications, 12 conferences, 15 patents, and 12 awards.
- No `7+` patent count remains in checked HTML pages.
- `Yang Yang` appears only as a legitimate patent inventor name, not as profile identity text.
- Publications data contains 9 records.
- Publications UI no longer exposes topic/status filters or conference-paper sections.
- Projects data contains 3 records.
- Removed project-specific links are not rendered on the projects pages.
- Awards data contains 12 records.
- `Outstanding Paper Award, KMEMS 2025` is present in awards data.

## Gallery data source check

- Official gallery data source: `assets/data/gallery.json`.
- Gallery record count: 36.
- `scripts/data-renderer.js` loads `assets/data/gallery.json`.
- `gallery.html` and `zh/gallery.html` no longer depend on `assets/gallery-data.json`.
- `assets/gallery-data.json` remains only as a legacy recovery artifact documented in cleanup notes.
- Local asset reference check found 77 unique local asset references and 0 missing files.

## Conference classification check

- Conference total: 12.
- Oral presentations: 4.
- Poster presentations: 8.
- Conference pages use section headings for Oral/Poster classification and do not repeat presentation-type labels inside each item.
- `H. Sun` does not appear in generated conference JSON or active CV PDFs.

## CV download check

Active PDF download targets exist:

- `assets/CV/Longlong_Li_Academic_CV_EN.pdf`
- `assets/CV/Longlong_Li_Academic_CV_ZH.pdf`
- `assets/CV/Longlong_Li_Resume_EN.pdf`
- `assets/CV/Longlong_Li_Resume_ZH.pdf`

The active PDF files can be parsed and have the expected page counts.

## GitHub Pages workflow check

Workflow checked: `.github/workflows/deploy-pages.yml`

- Installs Python dependencies via `pip install -r requirements.txt`.
- Runs `python tools/optimize_images.py`.
- Runs `python tools/generate_site_data.py`.
- Does not run legacy `tools/generate_gallery_data.py`.
- Uploads the repository root as the GitHub Pages artifact.
- Does not separately run `python tools/generate_cv_docs.py`; current generated CV files are committed and included in the uploaded repository root.
- `CNAME` is present and points to `longlongli.com`.
- `sitemap.xml` and `robots.txt` exist.
- No workflow rule was found that excludes `assets/data/*.json`, `assets/CV/*.pdf`, `assets/Project/*`, or gallery image folders from the Pages artifact.

## Known limitations

- Full page-by-page visual QA of generated PDFs was not performed. PDF parsing, page counts, and key text checks were performed instead.
- Browser console checks were performed on representative pages rather than every single page. HTTP availability was checked for all listed pages and JSON resources.
- The search term `TODO` still appears in inactive profile-link notes for ResearchGate/GitHub placeholders and in the historical extraction utility. These are not currently rendered as visible website content.
- `Content could not be loaded` remains in `scripts/data-renderer.js` as an expected fallback message and in troubleshooting documentation.
- `assets/gallery-data.json` remains documented as a legacy data artifact, but current pages and deployment no longer rely on it.

## Final recommendation

The current `project-structure-cleanup` branch is suitable for merge into the deployment branch after reviewing this validation report and the small deployment fixes made during validation:

- Added root `CNAME` for `longlongli.com`.
- Updated homepage academic-highlight counts to match current data.
- Updated stale audit documentation that still referenced older CV record counts and missing CNAME status.

No blocking issue remains in the validated static website data flow, Gallery source, CV generation, local page availability, or GitHub Pages workflow.

## Post-deployment maintenance note

After deployment integration, the canonical deployment branch is `main`.

Normal future maintenance should follow:

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

Important notes:

- Do not continue using `master` for new content updates.
- Do not push to `master`.
- Do not force push.
- Do not manually edit `assets/data/*.json`; edit `data/website_content.xlsx` and regenerate JSON.
- If CV content changes, regenerate CV documents before commit.
- GitHub Actions deploys from `main`.
