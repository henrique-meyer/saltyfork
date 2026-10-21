# SaltyFork artwork

- `saltyfork-full-body.png`: full-resolution transparent full-body mascot master.
- `saltyfork-full-body.svg`: saved automatic vector trace for reference; the owner
  selected the PNG for the landing hero to retain the illustration's appearance.
- `logo-icon-navy.svg` / `.png`: the `logo-mark-square-tight.svg` crop on the
  original navy `#0C2340` background. Used for the landing header and footer.
- `favicon.ico`: the same navy square icon at 16, 32, 48, 64, 128, and 256 pixels.
  The landing also advertises the SVG icon as its modern favicon.
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
