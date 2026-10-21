# SaltyFork artwork

- `icon-chef-salty.svg`: current navy-outline icon on navy, with a subtle silver
  fork, white hat, red scarf, half-lidded eyes, and a hat over two prongs.
- `icon-chef-salty-black-transparent.svg`: the same vector geometry with black
  outlines and no background.
- `icon-chef-salty-black-blue.svg`: black outlines on the original navy `#0C2340`.
- The three `*-preview.png` files are 512-pixel renders of these SVGs.
- `tools/build-icon-vectors.py` rebuilds genuine paths from the approved outline
  reference with Python 3.12, Pillow and vtracer 0.6.15, then applies shared colors,
  silver shading and backgrounds. The SVGs contain 16 paths and no raster images.
- `icon-chef-salty-master.png`: approved raster reference before vectorization,
  with half-lidded salty eyes and a broad hat covering the two rightmost prongs.
- `icon-chef-salty-black-transparent-master.png` and
  `icon-chef-salty-black-blue-master.png`: generated outline reference masters.
- `icon-chef-salty.png`: 192 × 192 PNG fallback rendered from the current SVG.
  `favicon-salty.ico` contains the same silver icon at 16, 32, 48, 64, 128, and
  256 pixels. The landing uses the SVG for header/footer and modern favicons.
- `icon-chef-v2-master.png`: new simplified icon concept, generated with the
  built-in imagegen tool. Retained as the earlier wide-eyed attempt.
- `icon-chef-v2.png`: earlier 192 × 192 PNG icon.
  `favicon-v2.ico` contains the earlier icon at 16, 32, 48, 64, 128, and 256 pixels.
- `saltyfork-full-body.png`: full-resolution transparent full-body mascot master.
- `saltyfork-full-body.svg`: saved automatic vector trace for reference; the owner
  selected the PNG for the landing hero to retain the illustration's appearance.
- `logo-icon-navy.svg` / `.png`: the `logo-mark-square-tight.svg` crop on the
  original navy `#0C2340` background. Retained as the previous icon version.
- `favicon.ico`: the same navy square icon at 16, 32, 48, 64, 128, and 256 pixels.
  Retained as the previous icon version.
- `web/landing/public/assets/mascot-full-body.png` (relative to the repository root):
  web-sized hero derivative. Crop the PNG master at x=190, y=13, width=688,
  height=1521, then resize to 1000 pixels tall and losslessly encode as PNG.

The original supplied illustration is `saltyfork-draft.jpg`. The transparent PNG
master was produced with the built-in imagegen tool, then saved here. The SVG
trace contains real paths and no embedded raster; it simplifies the raster's
shading and is retained separately from the selected web artwork.

## Background-extraction prompt

Use case: background-extraction. Edit target: the supplied original SaltyFork
full-body chef fork illustration. Remove only the beige/cream background and
the small cast shadow beneath the handle, including all beige spaces between
the arms, apron, spoon and fork. Output a clean genuinely transparent-background
PNG cutout. Preserve exactly the existing original mascot's full body, facial
expression, silvery fork, chef hat, red neckerchief, white apron, both arms and
gloves, and wooden spoon, with the same pose, proportions, colors, outlines, and
fine details. Do not redesign, stylize, add objects, or change expression. Crop
only empty surrounding space to a snug portrait bounding box with a little
transparent padding; do not crop any part of the hat, tines, hands, spoon, or
bottom handle. Asset intended for a landing page hero and subsequent SVG vector
tracing. No text or watermark.

## Simplified icon prompt (built-in imagegen)

Use case: logo-brand. Create a fresh, polished app icon for SaltyFork, a recipe-sharing app. Square composition, solid deep navy #0C2340 background extending to every edge, with a centered bold ivory-white anthropomorphic four-tined fork chef head. The fork has a small white chef hat perched to the right, playful confident dark navy eyes and a subtle friendly smirk, plus one simple bright coral-red neckerchief at the bottom. Make the character read immediately as a fork, not a spoon: clearly separated long fork tines visible above the face. Design the silhouette and large shapes for a 32px favicon. Contemporary flat vector illustration aesthetic with beautifully controlled smooth shapes, thick clean outlines and very few interior lines; predominantly warm white, navy and coral red. Keep the entire chef hat and whole fork-head silhouette inside the square with balanced generous breathing room; no awkward cropped hat. Face should be inviting and a little mischievous, not sleepy or sinister. Strong contrast, crisp edges, no tiny details, no gradients, no metallic gray shading, no texture, no photorealism, no 3D, no border, no mockup, no text, no letters, no watermark, no icon grids or multiple alternatives. One finished icon only.
