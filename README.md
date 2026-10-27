# ArtCraft usage notes

Verified notes, full command references, and small Python helpers for driving the ArtCraft command-line tools
(installed under `C:\Program Files\<Tool>`) from scripts and AI agents.

The goal is to save time and tokens: an agent reads one short notes file, searches the reference for anything else,
and reuses a helper, instead of exploring `--help`, `commands`, and `describe` output and failing a few runs first.

Each covered tool's folder has:

- `NOTES.md`: how to run the CLI, the common workflows, and gotchas, all tested.
- `REFERENCE.md`: every command with its parameters, generated from the CLI's own catalogue. Search it; it is large.
- A helper (where commands are verbose) and `example.py`, which builds and renders something.

| Tool | Notes | Reference | Helper | Example |
| --- | --- | --- | --- | --- |
| DeckCraft (slides) | [NOTES](deckcraft/NOTES.md) | [327 commands](deckcraft/REFERENCE.md) | [decklib.py](deckcraft/decklib.py) | [example.py](deckcraft/example.py) |
| WordCraft (Word documents) | [NOTES](wordcraft/NOTES.md) | [643 commands](wordcraft/REFERENCE.md) | [doclib.py](wordcraft/doclib.py) | [example.py](wordcraft/example.py) |
| PhotoCraft (images and sprites) | [NOTES](photocraft/NOTES.md) | [940 commands](photocraft/REFERENCE.md) | [photolib.py](photocraft/photolib.py) | [example.py](photocraft/example.py) |
| PdfCraft (PDF) | [NOTES](pdfcraft/NOTES.md) | [179 tools](pdfcraft/REFERENCE.md) | | [example.py](pdfcraft/example.py) |
| SoundCraft (audio) | [NOTES](soundcraft/NOTES.md) | [482 commands](soundcraft/REFERENCE.md) | | [example.py](soundcraft/example.py) |
| VectorCraft (vector art) | [NOTES](vectorcraft/NOTES.md) | [811 commands](vectorcraft/REFERENCE.md) | | [example.py](vectorcraft/example.py) |
| CADCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, LightCraft | Not yet | | | |

## Quick start

```
cd wordcraft
python example.py      # writes out/example.docx and a PNG per page
cd ../deckcraft
python example.py      # writes out/example.deckcraft, .pptx, and a PNG per slide
cd ../photocraft
python example.py      # writes transparent source and processed PNGs in out/photocraft-*
cd ../pdfcraft
python example.py      # writes out/example.pdf and a PNG of page 1
cd ../vectorcraft
python example.py      # writes out/example.svg and out/example-vector.png
cd ../soundcraft
python example.py      # writes out/example-tone.wav and out/example-edited.flac
```

Needs Python 3 and the tools installed. `Slide.picture()` needs Pillow (`pip install pillow`).
Output goes to `out/`, which git ignores.

## Updating the references

After installing or updating a tool, regenerate its reference: `python tools/gen_reference.py` (all tools)
or `python tools/gen_reference.py vectorcraft`. Then rerun that tool's example to catch changed commands.

## Adding a tool

Add the tool to `tools/gen_reference.py` and generate its `REFERENCE.md`. Then add `NOTES.md`
(only commands you ran and confirmed, plus the gotchas that cost a failed run), a small helper if the commands
are verbose, and an example that builds and renders something. Note the date and tool path you verified against.
