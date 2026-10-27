# DeckCraft CLI notes

Verified on 2026-10-26 against `C:\Program Files\DeckCraft\deckcraft-cli.exe`.
Use `decklib.py` instead of writing commands by hand; `example.py` shows every helper.

## Running

`deckcraft-cli run [--in deck.deckcraft] --cmd 'id={json}' ... --save deck.deckcraft [--export out.png --export-params '{"slide": i}']`

- There is no script file option, and Windows limits command-line length, so build **one slide per run**
  (`--in` and `--save` the same file). `decklib.build()` does this.
- Call the CLI from Python `subprocess.run([exe, ...args])`. Passing JSON through PowerShell quoting breaks.
- Slide is 960 x 540 pt; every `rect` is `[x, y, w, h]`.
- First slide: `design.theme {"name": "Harbor"}`, `slide.layout {"layout": "blank"}`. Later slides: `slide.last`, then `slide.new {"layout": "blank"}`.
- Inserting a shape selects it; the next `shape.*` and `format.*` commands act on that selection.

## Commands

| Purpose | Command and params |
| --- | --- |
| Shape | `shape.insert {"preset": "rect" \| "roundRect" \| "ellipse" \| "straightConnector1", "rect", "text"}` |
| Fill and outline | `shape.fill {"color": "#RRGGBB"}` or `{"none": true}`; `shape.line {"color", "width", "tail": "triangle"}` or `{"none": true}` |
| Arrow direction | connectors draw left-to-right and top-to-bottom; use `shape.flip {"axis": "horizontal" \| "vertical"}` |
| Text style | `format.fontDialog {"size", "bold", "color", "family"}`, `format.align {"align"}`, `format.anchor {"anchor": "middle"}`, `format.autofit {"mode": "none"}`, `format.wrap {"on": true}`, `format.margins {"left", ...}` |
| Numbered text | `format.numbering {"on": true, "scheme": "arabicPeriod", "color"}`, `format.paragraph {"spaceAfter"}` |
| Icon | `insert.icon {"name", "rect"}` then `shape.line {"color"}` (icons are outlines; fill does nothing) |
| Picture | `insert.picture {"path", "rect"}`; compute the rect to keep the aspect ratio (`Slide.picture()`, needs Pillow) |
| Table | `insert.table {"rows", "cols", "rect"}`, `table.style {"style": "medium2-accent1"}`, `text.set {"text", "cell": [r, c]}`, then `text.exit`, `format.size`, `table.cellAlign {"anchor": "middle"}`, `table.columnWidth {"col", "width"}` |
| Slide background | `design.background {"color"}` (current slide) |
| Slide numbers | `design.headerFooter {"slideNumber": true, "hideOnTitle": true, "all": true}` |
| Title metadata | `file.properties {"title"}` (a rebuild clears it, so set it again) |

Icon names: arrow-up/down/left/right, chevron-right, undo-2, refresh-cw, check, x, plus, minus, star, flag, award,
circle-check, triangle-alert, user, users, circle-user, calendar, clock, hourglass, mail, phone, message-circle,
bell, megaphone, chart-column, chart-bar, chart-pie, trending-up, target, lightbulb, file, file-text, folder,
clipboard, link, house, map-pin, globe, building, briefcase, image, search, info, circle-alert, lock, key, settings.

## Output

- Export one slide: `run --in deck --cmd 'slide.go={"index": i}' --export s.png --export-params '{"slide": i}'`.
- PowerPoint copy: `deckcraft-cli convert deck.deckcraft deck.pptx`. Slide list: `deckcraft-cli info deck`.
- Render every slide to PNG and look at it before calling the deck done; text overflow and overlaps only show there.
