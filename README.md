# Pavan Kalyan — portfolio

A static site with no framework, served as-is by GitHub Pages. EN / 中文 toggle built in.

## Edit the content
1. Change text in `content.py`. Each text is a pair: `T("English", "中文")`. Lines marked `TODO` still need your details.
2. Run `python build.py` to regenerate every page.
3. Preview it with `python -m http.server 8000`, then open http://localhost:8000

## Add your files
- Portrait: a cut-out photo with a transparent background (webp) in `assets/img/`, then set `SITE["portrait"]`.
- Résumé: the PDF in `assets/`, then set `SITE["resume"]`.
- Project images: replace `assets/img/projects/<slug>/cover.svg` / `detail.svg` (or change `cover()` / `detail()` in build.py to point at .webp files).
- Link preview image: `assets/img/og.png` (1200×630), made from `tools/og.html`.
- Illustrations: regenerate them with `python tools/make_art.py`.

## Publish
Push to GitHub, then go to Settings → Pages → Deploy from branch → `main` / root.
If the repo isn't named `portfolio`, update `SITE["url"]` in content.py and rebuild.
