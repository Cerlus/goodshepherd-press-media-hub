# Good Shepherd Press & Media Hub

Public press kit for *Good Shepherd* by ArchiusDev: a cozy shepherd sim by day and a narrated dungeon-crawler deckbuilder by night. Target: Steam Sheep Fest, Feb 4–8 2027.

Live: https://cerlus.github.io/goodshepherd-press-media-hub/

## Setup
Settings → Pages → Source: **GitHub Actions**. The workflow deploys every push to `main` and builds `assets/press-kit/goodshepherd-press-kit.zip`.

## Brand assets
`python3 tools/brand.py` (needs `playwright` and `pillow`) draws the key illustration (`tools/scene.py`: layered cut paper in SVG, one logo-free 3840 x 2160 master saved to `assets/branding/source`), the logo (stacked, one-line), the emblem and app icon, and cuts every Steam capsule, the library hero and the social banners from that master. Outputs land in `assets/branding` (logos and SVG sources in `assets/branding/logo`) and `assets/previews`. The marketing plan lives with the game's marketing files.

`assets/screenshots` holds 1920 x 1080 captures from the development build (`tests/press_shots.gd` in the game repo makes most of them; `thumbs/` are the page's small copies). `assets/video` holds the work-in-progress trailer, the opening storybook and the staffs clip; their music is a stand-in under CC BY 4.0 (credited on the page).

## Look
The page background follows the day: the `data-bg` attribute on `<html>` picks the palette (`dusk` = Day to Night; also `night`, `meadow`, `wool`, `paper`).

Press contact: needle-blares.0m@icloud.com · https://linktr.ee/archiusdev
