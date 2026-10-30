# SolidCraft CLI notes

Verified on 2026-10-30 against `C:\Program Files\SolidCraft\solidcraft-cli.exe` (parametric 3D CAD: sketches and a feature timeline).
Official docs: https://github.com/tangency-labs/solidcraft (see `docs/scripts.md`, `docs/features.md`, `docs/mcp.md`).
Every command and its parameters: [REFERENCE.md](REFERENCE.md) (542 commands; search it, do not read it whole).
`example.py` runs the workflow below.

`solvecraft-cli.exe` in the same folder is deprecated; use `solidcraft-cli`. The installer may not add it to PATH: use the full path.

## Running

`solidcraft-cli run script.json --out part.step --out part.stl --save part.sc`

- `script.json` is `{"commands": [{"command": id, "params": {...}}, ...]}` (UTF-8, no BOM). Write it from Python.
- `--out` picks the format from the extension (step, stl, obj, 3mf...) and can repeat; `--save` writes the editable `.sc` design.
- A feature that fails stops the run and writes nothing (`--allow-errors` writes anyway). `--param-check strict` checks every step's params first.
- `--in design.sc` (or a `.step`) runs the script on top of an existing design.
- One command without a script: `solidcraft-cli exec <command> [json-params]`. A saved design back to a script: `solidcraft-cli script design.sc --out script.json`.
- Lengths are **mm**, angles in degrees unless a command says otherwise. Expressions such as `"W / 2"` work where params say `expr`.

## Checking the result

- `solidcraft-cli eval part.sc` prints JSON per body: `volume_mm3`, `area_mm2`, `bbox`, `center_of_mass`, `faces`, `edges`, `closed`, `mass_g`.
  Compare the volume with hand arithmetic; it is the cheapest check.
- `solidcraft-cli snapshot part.sc --out shot.png --view iso --width 640 --height 400` draws a picture
  (`--view front|top|right|...`, `--section z=4` cuts it open, `--no-grid`). `render` makes a slower, realistic image.
- `--json-out FILE` writes eval or run results as plain UTF-8 (a PowerShell `>` adds a BOM).

## Commands used most

| Purpose | Command and params |
| --- | --- |
| Start a sketch | `sketch.create {"plane": "XY" \| "XZ" \| "YZ"}` (or `{"face": [x, y, z]}` to sketch on a face) |
| Rectangle | `sketch.rectangle.two_point {"p0": [x, y], "p1": [x, y]}` |
| Lines, circles | `sketch.line {"points": [[x, y], ...]}`; search REFERENCE.md for `sketch.circle` variants |
| Extrude | `solid.extrude {"distance": 20}` (or `"through_all": true`, `"taper"`) |
| Revolve | `solid.revolve {"axis": "X" \| "Y" \| "Z" \| sketch line id, ...}` |
| Fillet, chamfer | `solid.fillet {"edges": [[x, y, z], ...], "radius": 3}`, `solid.chamfer {"edges", "distance"}` |
| Hole | `solid.hole {"position": [x, y, z] on a face, "diameter": 10, "through_all": true}` |
| Shell | `solid.shell {"faces": [[x, y, z]], "thickness": 2}` |
| Export from a step | `file.export {"path", "format"}`; save `file.save {"path"}` |

Edges and faces are picked by **a point on them** in world mm, for example `[0, 0, 10]` is on the vertical edge at the origin
of a box that is 20 mm tall. Pick a point in the middle of the edge, not at a corner, so only one edge matches.
