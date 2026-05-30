# Longlong Li Academic Website

This repository is a bilingual personal academic website for Longlong Li, built with plain HTML, CSS, and a small JavaScript helper.

## Pages

- `index.html`: default English homepage
- `en/index.html`: English homepage copy
- `zh/index.html`: Chinese homepage
- `gallery.html`: English gallery page
- `zh/gallery.html`: Chinese gallery page
- `cv.html`: English CV page
- `zh/cv.html`: Chinese CV page

## Customization

- Update homepage content in `index.html` and `zh/index.html`
- Add your real profile links where the placeholder social buttons are currently shown
- Replace the portrait by updating `assets/Longlong.jpg`
- Add future gallery images to `assets/albums` using the naming format `YYYY-MM-DD_Title.jpg` or `YYYYMMDD_标题.jpg`
- Run `python tools/generate_gallery_data.py` locally if you want to preview new gallery items before pushing

## Deployment

This site is deployed as a static GitHub Pages site.

- The gallery data file `assets/gallery-data.json` is generated automatically during deployment
- The included GitHub Actions workflow regenerates the gallery list from `assets/albums` on every push to `main` or `master`

If you want to use a custom domain later, create a new `CNAME` file with your own domain before deploying.
