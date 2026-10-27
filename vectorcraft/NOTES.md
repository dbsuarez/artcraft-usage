# VectorCraft CLI notes

Verified on 2026-10-27 against `C:\Program Files\VectorCraft\vectorcraft-cli.exe` (an Illustrator-style vector editor).
Every command and its parameters: [REFERENCE.md](REFERENCE.md) (811 commands; search it, do not read it whole).
`example.py` runs the workflow below.

## Simple jobs (no script)

| Job | Command |
| --- | --- |
| Convert between formats | `vectorcraft-cli convert in.svg out.pdf` (also .png, .eps, .ai, .dxf, .emf, .psd...; `--scale 2` for raster size, `--artboard 0`) |
| SVG text as shapes | `vectorcraft-cli convert in.svg out.svg --outline-text` |
| Summary | `vectorcraft-cli info file.svg` (artboards, object counts, fonts, import warnings, JSON) |

Reads .svg, .pdf, .ai, .eps, .png, .jpg, .psd, .dxf, .emf, Affinity files and more; the extension picks the format.

## Drawing (run)

`vectorcraft-cli run [--in FILE] --commands steps.json --export out.svg --export out.png --scale 2`

- `steps.json` is a JSON array of `{"command": id, "params": {...}}` (or one object per line). Write it from Python.
  Single steps also work as `--cmd ID --params JSON`, but quoting JSON on Windows breaks; prefer a file.
- Each `--export` writes a file in the format its extension picks; `--scale` is pixels per point for raster exports.
- It prints one JSON result per step; errors name the step (counting from 0).
- Coordinates are points, origin at the top-left of the artboard, y down.
- Drawing a shape selects it; `paint.*` and `stroke.*` apply to the selection.

| Purpose | Command and params |
| --- | --- |
| New document | `file.new {"width", "height", "units": "Points"}` (or `"width": "210 mm"`; presets via `file.newPresets`) |
| Rectangle | `shape.rectangle {"x", "y", "width", "height", "radius", "rotation"}` |
| Ellipse | `shape.ellipse {"x", "y", "width", "height"}` |
| Polygon, star | `shape.polygon {"cx", "cy", "radius", "sides"}`, `shape.star {"cx", "cy", "radius1", "radius2", "points"}` |
| Line | `shape.line {"x1", "y1", "x2", "y2"}` |
| Fill | `paint.setFill {"color": "#rrggbb"}` or `{"none": true}` |
| Outline | `paint.setStroke {"color"}` or `{"none": true}`, then `stroke.set {"weight", "cap", "join", "dash": [d, g]}` |
| Text | `text.create {"x", "y", "text", "size", "font", "color"}`; wrapped text: add `"area": {"width", "height"}` |
| Group | `object.group {"ids": [...]}` (ids come back from each shape command) |
| Artboard | `artboard.new {"x", "y", "width", "height", "name"}` |
| Save editable | `file.save {"path": "art.vectorcraft"}` (or .svg, .pdf, .ai) |

Shapes get a default black outline; set `paint.setStroke {"none": true}` when you want none.
Always export a PNG and look at it before reporting done.
