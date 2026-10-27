# WordCraft CLI notes

Verified on 2026-10-26 against `C:\Program Files\WordCraft\wordcraft-cli.exe`.
Use `doclib.py` instead of writing commands by hand; `example.py` shows every helper.

## Running

`wordcraft-cli run --script script.json`, where the file is
`{"commands": [{"command": "id", "params": {...}}, ...], "save": ["out.docx"]}`.

- The JSON must be UTF-8 **without BOM**. PowerShell `Set-Content -Encoding utf8` adds a BOM and the run fails with "bad JSON". Write it from Python.
- Use absolute paths for `save` and pictures.
- Check output: `wordcraft-cli info out.docx` (JSON with `pages`), `wordcraft-cli render out.docx p.png --page N --scale 1.2` (pages start at 1).
- Build Word files with these commands. Converting Markdown to `.docx` gives poor formatting.

## Commands

| Purpose | Command and params |
| --- | --- |
| Page setup | `layout.size {"name": "A4"}`, `layout.margins {"preset": "normal"}` (A4 text width is 451 pt) |
| Style defaults | `styles.modify {"style": "Heading1", "chr": {"font", "size", "bold", "color": "RRGGBB"}, "para": {"spaceBefore", "spaceAfter"}}` (a float `lineSpacing` is rejected) |
| Paragraph style | `para.style {"style": "Normal" \| "Heading1" \| "Heading2" \| "Caption"}` |
| Text | `text.insert {"text"}`, `text.newParagraph`, `text.pageBreak` |
| Inline bold or color | `format.set {"props": {"bold": true, "size", "color"}}` then `format.resetChar` (setting props to null does not reset) |
| Lists | `para.bullets` / `para.bullets {"off": true}`; `para.numbering {"kind": "numbered"}` + `para.restartNumbering` / `{"off": true}` |
| Callout | `para.shading {"color": "E4EEF2"}`, `para.borders {"kind": "left", "width": 3, "color"}`; clear with `{"color": null}` and `{"kind": "none"}` |
| Keep with next, spacing, align | `para.keepNext`; `para.set {"props": {"spaceBefore": 10}}`; `para.alignCenter` / `para.alignLeft` |
| Picture | `insert.picture {"path", "width": pt, "alt"}` |
| Table | `insert.table {"rows", "cols", "style": "GridTable4AccentBlue"}` (also TableGrid, ListTable3AccentBlue, Green/Orange/Purple variants), `table.autofit {"mode": "fixed"}`; caret starts in cell (0,0), `text.tab` moves to the next cell, `caret.docEnd` leaves the table |
| Column width | `table.columnWidth {"width": pt}` acts on the caret's column, so set it while in each header cell |
| Page numbers | `insert.pageNumber {"position": "bottom", "align": "center"}` (do this last) |

## Gotchas

- `para.set` and `format.set` carry over into every following paragraph (headings lose bold, gaps grow).
  Start each block with `para.style`, `para.reset`, `format.resetChar` (`Doc.start()` does this).
- Page breaks before headings that already land at a page top leave blank pages. Prefer `para.keepNext` on headings and few explicit breaks.
- Render every page and look at it before calling the document done.
