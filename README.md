# ArtCraft usage notes

Verified notes and small Python helpers for driving the ArtCraft command-line tools
(installed under `C:\Program Files\<Tool>`) from scripts and AI agents.

The goal is to save time and tokens: an agent reads one short notes file and reuses a helper,
instead of exploring `--help`, `commands`, and `describe` output and failing a few runs first.

| Tool | Status | Notes | Helper | Example |
| --- | --- | --- | --- | --- |
| DeckCraft (slides) | Covered | [deckcraft/NOTES.md](deckcraft/NOTES.md) | [decklib.py](deckcraft/decklib.py) | [example.py](deckcraft/example.py) |
| WordCraft (Word documents) | Covered | [wordcraft/NOTES.md](wordcraft/NOTES.md) | [doclib.py](wordcraft/doclib.py) | [example.py](wordcraft/example.py) |
| PhotoCraft (images and sprites) | Covered | [photocraft/NOTES.md](photocraft/NOTES.md) | [photolib.py](photocraft/photolib.py) | [example.py](photocraft/example.py) |
| CADCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, LightCraft, PdfCraft, SoundCraft, VectorCraft | Not yet | | | |

## Quick start

```
cd wordcraft
python example.py      # writes out/example.docx and a PNG per page
cd ../deckcraft
python example.py      # writes out/example.deckcraft, .pptx, and a PNG per slide
cd ../photocraft
python example.py      # writes transparent source and processed PNGs in out/photocraft-*
```

Needs Python 3 and the tools installed. `Slide.picture()` needs Pillow (`pip install pillow`).
Output goes to `out/`, which git ignores.

## Adding a tool

Add a folder with `NOTES.md` (only commands you ran and confirmed, plus the gotchas that cost a failed run),
a small helper if the commands are verbose, and an example that builds and renders something.
Note the date and tool path you verified against.
