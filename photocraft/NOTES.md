# PhotoCraft CLI: verified usage

Verified **2026-10-27**, Windows PowerShell 5.1, `photocraft-cli 0.16.0 (b1794c6e0, 2026-10-25)`.
Executable: `C:\Program Files\PhotoCraft\photocraft-cli.exe`. Use the CLI executable, not the desktop application.
Every command and its parameters: [REFERENCE.md](REFERENCE.md) (search it, do not read it whole).

## Start here

Run `python photocraft/example.py` from the repository root. It creates a transparent shape, crops it,
resizes it, pads it, checks dimensions, and writes PNGs into a unique ignored `out/photocraft-*` folder.
Open both PNGs before accepting the result. The example was run and visually checked.
Python 3 standard library only; no Pillow dependency. Copy `photolib.py` beside your script or add its folder to `sys.path`.

```python
from photolib import Photo
p = Photo()
print(p.info("source.png"))
p.run("source.png", "frame.png", [
    ("image.crop", {"x":0,"y":0,"width":128,"height":128}),
    ("image.canvasSize", {"width":160,"height":160,
                          "anchor":"center","extensionColor":"transparent"}),
])
```

The helper refuses existing output paths, passes arguments directly without a shell,
reports successful stderr warnings, raises on a nonzero exit, and checks `run` wrote its output.

## Confirmed commands

| CLI / engine command | Parameters and behavior |
| --- | --- |
| `info FILE --compact` | JSON dimensions, document mode, layers and warnings. |
| `run FILE --cmd ID --params JSON --out FILE` | Repeat command/parameter pairs to apply ordered operations. Outputs command results as JSON lines. |
| `run --new JSON --out FILE` | New document: `width`, `height`, `background:"transparent"`, `mode:"rgb"`, `depth:8`. |
| `convert IN OUT` | Export by extension. PNG/WebP transparency round trip verified. |
| `image.crop` | `x`, `y`, `width`, `height`. |
| `image.imageSize` | `width`, `height`, `resample:"nearest"` for pixel art. |
| `image.canvasSize` | `width`, `height`, `anchor:"center"` or `"bottom"`, `extensionColor:"transparent"`. Changes canvas, not pixel scale. |
| `image.trim` | `basedOn:"transparent"`. |
| `file.placeEmbedded` | `path`, `center:[x,y]`, `scale:100`, `fit:false`, `smartObject:false`; tested assembling isolated frames. |
| `shape.create` | Tested ellipse: `kind:"ellipse"`, `rect:[x,y,w,h]`, `fill:"#00BBDD"`, `stroke:{"width":4,"color":"#FFFFFF"}`, `name`. |

For a transparent new document with the helper, pass `source=None` and `new={...}` to `run`.
Use `.pcraft` for editable layered masters; PNG exports flatten layers. The flattening warning does not mean alpha was removed.

## Sprite workflow and gotchas

- **PowerShell 5.1 strips JSON quotes in ordinary native arguments.** Use the Python helper's subprocess argument list; JSON encoding alone is not shell escaping.
- The resize command is `image.imageSize`, not `resize`.
- Explicitly request transparent backgrounds and canvas extensions; defaults can introduce opaque backgrounds.
- Isolate each frame before resizing. Preserve a common cell size, anchor, and pixel scale across animation frames.
- For an uneven grid, compute shared crop boundaries with `floor(index * dimension / count + 0.5)`, then transparently pad each crop to a common square. This preserves pixels without fractional cells. It cannot repair artwork already crossing cell boundaries.
- Assemble a sheet on a transparent canvas with `file.placeEmbedded`, exact cell centers, `fit:false`, and `scale:100`.
- WebP export without `--quality` was lossless; supplying quality selects lossy WebP, including quality 100. JPEG cannot retain transparency.
- `channels.alpha:[]` in metadata means no named alpha channels; it does not prove pixel transparency is absent.
- CLI `run`/`convert` reject same input/output without `--in-place`. Keep sources intact and use new paths.
- An invalid command after a valid command returned failure with no exported output in testing. Do not assume other workflows provide transactional rollback.

## Batch processing

Tested action file format:

```json
{"steps":[["image.imageSize",{"width":128,"height":128,"resample":"nearest"}]]}
```

Invoke `batch --actions actions.json --in input-directory --out output-directory --format png`.
Use a fresh output directory. This particular action stretches inputs to square, so use already square frames.

## Persistent automation / MCP

Both `serve` JSON-lines and `mcp` initialization/tool discovery were verified. Restrict file access with
`--automation-read-root DIRECTORY --automation-write-root DIRECTORY`; outside-root access was rejected.
MCP without allowed roots denies file access. Desktop bridge mode was not tested.

`serve` requests use `{ "id":1, "method":"doc.open", "params":{"path":"..."} }`.
Other tested methods: `doc.inspect`, `doc.save`, and `engine.execute` with
`{"command":"image.imageSize","params":{"width":128,"height":128,"resample":"nearest"}}`.
Check response `ok` and `error`: a failed request can coexist with process exit zero.

MCP discovery used protocol `2025-06-18`. Tools include `doc_open`, `doc_new`, `doc_inspect`,
`command_list`, `command_run`, `command_batch`, `doc_save`, and `render_preview`.
MCP `command_run` uses `{"id":"image.imageSize","params":{...}}`, unlike serve's `command` key.
MCP batch steps use `id` and `params`; do not assume atomic rollback.
`render_preview` accepts `max_side` up to 2048. These are protocol/discovery notes, not a claim that every tool was exercised.

No AI text-to-image command was found in the installed registry. Local shapes and image processing are supported;
do not confuse those operations with an image-generation service. Inspect unfamiliar schemas only when needed, then record confirmed behavior here.
