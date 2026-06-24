# Deployment and Preview Guide

This document explains how to preview the website locally, regenerate JSON data after Excel updates, and troubleshoot common maintenance problems.

## Local preview

Run the following commands from the project root:

```bash
cd "D:\Documents\0_Longlong material\longlongWeb\yangcv"
python tools\generate_site_data.py
python -m http.server 8020
```

Then open:

```text
http://127.0.0.1:8020/index.html
```

Do not close the terminal window while previewing.

Do not preview by double-clicking HTML files, because the website loads JSON files through `fetch()` and needs a local server.

## Update the site after editing Excel

After changing `data/website_content.xlsx`:

1. Save and close `data/website_content.xlsx`
2. Run:

```bash
python tools\generate_site_data.py
```

3. Check the updated files under `assets/data/`
4. Start a local HTTP server
5. Reload the page with `Ctrl + F5` to bypass browser cache

## Check whether new content reached the generated data

Use:

```bash
python tools\check_content_update.py "keyword"
```

This helper checks:

- whether the keyword exists in `data/website_content.xlsx`
- which sheet and row contain it
- whether the keyword exists in generated JSON files
- which JSON file contains it

## GitHub Pages deployment

The website is deployed by GitHub Actions after pushing committed changes.

The deployment workflow should:

1. Install Python dependencies
2. Run `python tools/generate_site_data.py`
3. Upload the static site as the Pages artifact

The current deployment file is:

- `.github/workflows/deploy-pages.yml`

## Common problems

### `ModuleNotFoundError: No module named 'openpyxl'`

Cause:

- Python dependencies are not installed in the current environment.

Fix:

```bash
pip install -r requirements.txt
```

### Directly opening HTML shows `Content could not be loaded`

Cause:

- The site was opened with `file://...` instead of through a local HTTP server.

Fix:

```bash
python tools\generate_site_data.py
python -m http.server 8020
```

Then open:

```text
http://127.0.0.1:8020/index.html
```

### Excel changed but JSON did not update

Cause:

- `generate_site_data.py` was not rerun, or Excel was still open and not saved.

Fix:

1. Save and close the workbook
2. Run:

```bash
python tools\generate_site_data.py
```

3. Confirm file timestamps in `assets/data/`

### JSON updated but webpage still does not show the change

Cause:

- Browser cache, stale local server state, or the updated field is not rendered on the target page.

Fix:

1. Press `Ctrl + F5`
2. Confirm the value exists in the correct JSON file
3. Use:

```bash
python tools\check_content_update.py "keyword"
```

4. Verify the target page actually renders that field

### Browser cache problem

Fix:

- Use `Ctrl + F5`
- Restart the local server if needed
- Reopen the page after regenerating JSON

### Image path returns 404

Cause:

- Image file was moved, renamed, or referenced with the wrong relative path.

Fix:

1. Confirm the file exists in `assets/`
2. Check whether the path in Excel is correct
3. Regenerate JSON
4. Recheck the page reference and local preview URL
