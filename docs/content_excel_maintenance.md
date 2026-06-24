# Website Content Excel Maintenance

`data/website_content.xlsx` is now the primary structured content source for the personal academic website. The public pages remain static HTML, but the repeated content areas are generated from JSON files created from this workbook.

## Workbook sheets

| Sheet | Purpose |
| --- | --- |
| `profile` | Personal identity, affiliation, contact details, biography, and research keywords |
| `publications` | Complete journal publication list and citation metadata |
| `patents` | Invention patents, published applications, and utility model patents |
| `conferences` | Oral and poster presentation records |
| `awards` | Scholarships, academic honors, competitions, and other awards |
| `projects` | The three projects currently visible on the Projects page |
| `gallery` | Date, title, image path, and source filename generated from album images |
| `cv` | Structured sections used by the web CV and downloadable CV |
| `links` | Profile, download, publication, and conference URLs |

Each sheet uses one record per row. The first row is frozen and filterable. Do not merge cells or insert additional header rows.

## Adding content

### Publication

Add one row to `publications`.

Required fields: `id`, `year`, `title_en`, `authors`, `journal`, `type`, and `selected`.

Recommended `type` values: `journal`, `review`, `manuscript`, `other`.

Use `TRUE` in `selected` only when the publication should appear in a selected-publications view. Leave unknown DOI, volume, issue, pages, or Chinese title fields blank rather than guessing.

### Patent

Add one row to `patents`.

Required fields: `id`, at least one title, and either `patent_number` or `application_number`.

Recommended `patent_type` values:

- `granted_invention`
- `published_invention_application`
- `utility_model`
- `other`

Keep legal metadata concise. Do not add technical summaries or abstracts to this table.

### Conference

Add one row to `conferences`.

Required fields: `id`, `year`, `title_en`, and `presentation_type`.

Allowed `presentation_type` values: `oral`, `poster`.

Keep the conference name and location in separate columns. Add a URL only when a valid external record exists.

### Award

Add one row to `awards`.

Required fields: `id`, `year`, `name_en`, and `category`.

Recommended `category` values: `scholarship`, `academic_honor`, `competition`, `other`.

National, provincial, institute, and conference levels belong in the `level` column rather than in separate top-level categories.

### Project

Add one row to `projects`.

Required fields: `id`, English or Chinese title, `visible`, and `order`.

Use `TRUE` or `FALSE` in `visible`. Use a unique integer in `order`. Keep image paths relative to the website root, for example `assets/Project/example.webp`.

## Gallery maintenance

The Gallery currently remains filename-driven. Add or rename source images in `assets/albums/` using the existing date-and-title convention, then run the image and gallery generation scripts before regenerating this workbook. The `gallery` sheet records the generated path and source filename; it does not replace the current Gallery build process.

## How the Excel-driven website works

1. Edit `data/website_content.xlsx`.
2. Run `python tools/generate_site_data.py`.
3. Review the generated JSON files under `assets/data/`.
4. Preview the website locally.
5. Commit the workbook, generated JSON, and page updates together.
6. GitHub Actions reruns the JSON generation step before deploying GitHub Pages.

The publish chain is:

`data/website_content.xlsx` -> `tools/generate_site_data.py` -> `assets/data/*.json` -> static HTML + `scripts/data-renderer.js`

## Required and controlled fields

### Publications

Required: `id`, `year`, `title_en`, `authors`, `journal`, `type`, `selected`

Allowed `type` values:

- `journal`
- `review`
- `manuscript`
- `other`

Only year filters are rendered on the Publications page. Topic tags may stay in notes or future fields, but they are not exposed in the current UI.

Use `TRUE` in `selected` when a publication should appear in homepage or CV selected-publication views.

### Patents

Required: `id`, `title_en`, `title_zh`, `inventors`, `applicant`, `patent_type`

At least one of `patent_number` or `application_number` must be present.

Allowed `patent_type` values:

- `granted_invention`
- `published_invention_application`
- `utility_model`
- `other`

Patent descriptions are intentionally not rendered on the Patents page.

### Conferences

Required: `id`, `year`, `title_en`, `authors`, `conference`, `presentation_type`

Allowed `presentation_type` values:

- `oral`
- `poster`

The Conferences page groups records by `presentation_type`, so oral/poster classification should be maintained in Excel.

### Awards

Required: `id`, `year`, `name_en`, `category`

Recommended `category` values:

- `scholarship`
- `academic_honor`
- `competition`
- `other`

The Awards page groups categories as:

- `scholarship` -> Scholarships & Fellowships
- `academic_honor` -> Academic Honors
- `competition` and `other` -> Competitions & Other Awards

Award level information such as national or provincial status belongs in `level` or `description_*`, not as a separate page section.

### Projects

Required: `id`, `title_en`, `title_zh`, `visible`, `order`

Use `TRUE` or `FALSE` in `visible`.

- `visible = TRUE`: project is rendered on `projects.html` / `zh/projects.html`
- `visible = FALSE`: project stays in Excel but is hidden from the Projects page

Homepage featured projects currently use the first visible rows after sorting by `order`.

### Gallery

Required: `id`, `image`

Recommended fields: `date`, `title_en`, `title_zh`, `source_filename`

The website reads `assets/data/gallery.json`, which is generated from the workbook. The existing image optimization and filename-driven helper scripts remain available, but the published page now uses the workbook-derived JSON.

### CV

Required: `section`, `item_id`, `order`

Keep section names stable because the CV renderer groups by these keys:

- `profile`
- `education`
- `research_experience`
- `technical_skills`
- `selected_projects`
- `selected_publications`
- `selected_conferences`
- `patent_overview`
- `awards`

## Regenerating the workbook

Run:

```powershell
python tools/extract_site_content_to_excel.py
```

The extraction script parses the current HTML and Gallery JSON, validates critical fields, and invokes the workbook builder. It prints record counts and warnings for optional missing fields.

Use the extraction script only when you need to rebuild the workbook from the currently published site snapshot. For normal maintenance after this refactor, edit the workbook directly and regenerate JSON with:

```powershell
python tools/generate_site_data.py
```
