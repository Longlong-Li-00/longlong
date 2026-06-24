# Website Content Excel Maintenance

`data/website_content.xlsx` is a structured snapshot of the content currently published on the personal academic website. It is intended to become the central editing table for a later data-driven website refactor. The current HTML pages do not read from this workbook yet.

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

## Regenerating the workbook

Run:

```powershell
python tools/extract_site_content_to_excel.py
```

The extraction script parses the current HTML and Gallery JSON, validates critical fields, and invokes the workbook builder. It prints record counts and warnings for optional missing fields.

The workbook is currently an extraction and maintenance artifact only. A future refactor can generate HTML or JSON from it after field names, validation rules, and bilingual content have been reviewed. Until that refactor is implemented, update both the public HTML and this workbook when changing published content.
