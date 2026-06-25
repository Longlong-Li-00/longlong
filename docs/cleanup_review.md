# Cleanup Review

## Safe temporary files removed

The following low-risk Python cache files were removed in this phase:

- `tools/__pycache__/generate_gallery_data.cpython-312.pyc`
- `tools/__pycache__/optimize_images.cpython-312.pyc`
- `tools/__pycache__/update_seo_metadata.cpython-312.pyc`
- `tools/__pycache__/` directory

No removable `.log`, `.DS_Store`, `Thumbs.db`, or `Desktop.ini` files were found in the current working tree.

## Files kept intentionally

The following files or folders were intentionally kept in place during this phase:

- `en/index.html`
- `assets/gallery-data.json`
- `temp/`
- `tmp/`

These items may be obsolete or partially duplicated, but they are still referenced by tracked files or may still reflect local intermediate workflow state. They are not safe to delete without a later coordinated cleanup step.

## Files requiring manual review

| Path | Reason | Recommendation | Risk |
|---|---|---|---|
| `en/index.html` | Appears to duplicate the root English homepage route, but is still referenced by `sitemap.xml` and `tools/update_seo_metadata.py`. | Keep for now. Review whether `/en/` is still a supported public route before archiving or removing. | Medium |
| `assets/gallery-data.json` | Legacy gallery data file retained for historical recovery and the old HTML-to-Excel extraction utility. Current pages and deployment no longer depend on it. | Keep for now. Consider archive or removal only after the extraction workflow is retired or updated. | Medium |
| `temp/cv_render_en` | Empty local intermediate render directory from earlier CV export or render workflow. | Keep for now. If no tool depends on it, move to archive later or remove in a dedicated local-artifact cleanup phase. | Low |
| `temp/cv_render_zh` | Empty local intermediate render directory from earlier CV export or render workflow. | Keep for now. If no tool depends on it, move to archive later or remove in a dedicated local-artifact cleanup phase. | Low |
| `tmp/render_resume_en` | Empty local intermediate render directory from an earlier resume rendering workflow. | Keep for now. If no tool depends on it, move to archive later or remove in a dedicated local-artifact cleanup phase. | Low |

## Potential duplicate data flows

The repository retains two Gallery JSON files, but only one is now part of the formal runtime flow:

- `assets/data/gallery.json`
- `assets/gallery-data.json`

Current state:

- `assets/data/gallery.json` is generated from `data/website_content.xlsx`
- `scripts/data-renderer.js` renders both Gallery pages from `assets/data/gallery.json`
- `gallery.html` and `zh/gallery.html` no longer reference `assets/gallery-data.json`
- the deployment workflow no longer runs `tools/generate_gallery_data.py`
- `tools/generate_gallery_data.py` and `assets/gallery-data.json` remain as legacy recovery resources
- `tools/extract_site_content_to_excel.py` still reads the legacy file during the old HTML-to-Excel bootstrap workflow

The runtime and deployment data flow is unified. The remaining legacy references are offline maintenance references, not page dependencies.

## Future cleanup candidates

Potential later cleanup or archive candidates, not acted on in this phase:

- `en/index.html`
- `assets/gallery-data.json`
- `temp/`
- `tmp/`
- legacy Gallery helper flow around `tools/generate_gallery_data.py` and `tools/extract_site_content_to_excel.py`
- legacy or standalone SEO helper flow around `tools/update_seo_metadata.py`
