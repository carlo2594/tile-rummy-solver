# Tile Rummy Solver

A free web tool that finds the best move in Rummikub-style tile rummy games: enter the tiles on the table and in your rack, and it shows the move that plays the most tiles.

**Live site:** https://tilerummysolver.com · by Carlo J

## What's in this repository

```
site/   The finished website. This is the folder that gets published.
src/    The source the site is built from.
  template.html   The solver page (layout, styles and app code)
  solver.js       The solver (also runs as a background Web Worker)
  build.py        Builds every page into site/ (guides, FAQ, sitemap, etc.)
  puzzles.js      Checks the practice puzzles with the solver -> puzzles.json
```

The site is plain static files: no server, no database, no API keys.

## Deploy (Cloudflare Pages)

1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git**, and pick this repository.
2. Build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `site`
3. Add the custom domain `tilerummysolver.com` under **Custom domains**.

Every push to `main` then redeploys the site automatically.

## Making changes

- **Small text fix:** edit the file in `site/` directly and push.
- **Bigger change:** edit the files in `src/`, then rebuild:
  ```
  node src/puzzles.js      # only if you changed the puzzles
  python3 src/build.py     # rebuilds everything in site/
  ```
  Note that `build.py` overwrites `site/`, so changes made directly in `site/` are lost when you rebuild. Make lasting changes in `src/`.

## Settings to fill in

- `site/site.js`: your Ko-fi link (the tip button stays hidden until it's set).
- `site/ads.txt`: your AdSense publisher line, once AdSense approves the site.

## How the solver works

Dynamic programming over the numbers 1–13 (after van Rijn, Takes & Vis, *The Complexity of Rummikub Problems*): it tracks the open runs per color and the jokers used, and keeps the best arrangement for each state. That means the answer is the true best move, not a guess.

## Trademark

Rummikub® is a registered trademark of its owner. This project is independent and not affiliated with or endorsed by the trademark owner.

© 2026 Carlo J. All rights reserved.
