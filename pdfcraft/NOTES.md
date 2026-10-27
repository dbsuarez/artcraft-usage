# PdfCraft CLI notes

Verified on 2026-10-27 against `C:\Program Files\PdfCraft\pdfcraft-cli.exe`.
Every tool and its arguments: [REFERENCE.md](REFERENCE.md) (search it, do not read it whole). `example.py` runs the workflow below.

## Simple jobs (no script)

| Job | Command |
| --- | --- |
| Summary (pages, size, title, PDF/A) | `pdfcraft-cli info in.pdf` (JSON) |
| Look at a page | `pdfcraft-cli render in.pdf --page 1 --dpi 96 --out p1.png` (pages start at 1) |
| Text | `pdfcraft-cli text in.pdf [--page N]` (pages separated by form feeds) |
| Merge | `pdfcraft-cli combine a.pdf b.pdf --out all.pdf` |
| Pick pages | `pdfcraft-cli extract in.pdf --pages 3,1,5-8 --out out.pdf` (in the order given) |
| Split | `pdfcraft-cli split in.pdf --every 1 --out-dir parts` or `--before 3,7` |
| Rotate, delete, move, title | `pdfcraft-cli edit in.pdf --out out.pdf --rotate 1:90 --delete 4 --move 5:1 --title T --author A` (options run in order) |
| Compress, OCR | `pdfcraft-cli batch in.pdf --steps optimize,ocr --out-dir out` |
| Find fake redactions | `pdfcraft-cli audit in.pdf` (fails when found) |

## Scripts (everything else)

`pdfcraft-cli run --script steps.json [--report]`, where the file is a JSON array of
`{"tool": name, "args": {...}}`. `--report` prints one JSON result for the whole run.
One tool alone: `pdfcraft-cli run page_render doc=1 ...` (`key=value` args).

- `doc_open {"path"}` or `doc_create {...}` returns a document id; the first one in a run is `1`. Pass it as `"doc": 1` to later tools.
- Nothing is written until `doc_save {"doc": 1, "path": "out.pdf"}`. Use absolute paths.
- Positions are points from the **top-left** of the page (A4 is 595 x 842, US Letter 612 x 792).

| Purpose | Tool and args |
| --- | --- |
| New PDF | `doc_create {"from": "blank", "pages", "width", "height"}` (default 1 Letter page); also `"from": "images", "paths": [...]` |
| Add text | `page_add_text {"doc", "page", "text", "at": [x, y], "width", "size", "bold", "color": "#RRGGBB", "align"}` |
| Add image | `page_add_image {"doc", "page", "path", "rect": [x, y, w, h]}` (no rect: centred at natural size) |
| Header or footer | `doc_header_footer {"doc", "footer_center": "Page <<1>> of <<n>>", "font_size", "pages"}` (also header_left/center/right, footer_left/right) |
| Watermark | `doc_watermark {"doc", "text": "DRAFT", "opacity": 0.15, "rotation": 45, "font_size"}` or `"file"` for an image |
| Insert another PDF | `page_insert_file {"doc", "path", "at", "pages"}` |
| Password | `doc_protect {"doc", "open_password", "permissions_password", "printing", "copy"}` then `doc_save` |
| Find text | `text_find {"doc", "query"}` (page and rectangles) |
| PDF to Word, PowerPoint, HTML | `doc_export_office {"doc", "path": "out.docx"}` (format from the extension) |
| Smaller copy | `doc_reduce {"doc", "path"}` |

## Making PDFs from other tools

- Word: `wordcraft-cli run --script s.json` with `"save": ["out.docx", "out.pdf"]`, or `wordcraft-cli convert in.docx out.pdf`.
- Vector art: `vectorcraft-cli convert in.svg out.pdf`.
- Then add headers, watermarks, or a password with PdfCraft.
