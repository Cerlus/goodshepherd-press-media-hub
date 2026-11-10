# Good Shepherd Press & Media Hub

Public press kit for *Good Shepherd* by ArchiusDev: a cozy shepherd sim by day and a narrated dungeon-crawler deckbuilder by night. Target: Steam Sheep Fest, Feb 4–8 2027.

Live: https://cerlus.github.io/goodshepherd-press-media-hub/

## Setup
Settings → Pages → Source: **GitHub Actions**. The workflow deploys every push to `main` and builds `assets/press-kit/goodshepherd-press-kit.zip`.

## Brand assets
`python3 tools/brand.py` (needs `playwright` and `pillow`) redraws the logo (stacked, one-line), the emblem and app icon, and recomposes every Steam capsule and social banner from the logo-free key art in `assets/branding/steam/library-hero-3840x1240.png`. Outputs land in `assets/branding` (logos and SVG sources in `assets/branding/logo`) and `assets/previews`. The original illustration and the marketing plan live with the game's marketing files.

`assets/screenshots` holds work-in-progress captures from the development build; replace them with final screenshots when the Steam page goes up.

## Look
The page background follows the day: the `data-bg` attribute on `<html>` picks the palette (`dusk` = Day to Night; also `night`, `meadow`, `wool`, `paper`).

Press contact: needle-blares.0m@icloud.com · https://linktr.ee/archiusdev
