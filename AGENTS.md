# Instructions for AI agents

- Before using an ArtCraft CLI, read that tool's `NOTES.md` here instead of running `--help`, `commands`, or `describe`.
- Reuse the helper (`deckcraft/decklib.py`, `wordcraft/doclib.py`, `photocraft/photolib.py`) by copying it next to your build script or adding its folder to `sys.path`.
- For a command the notes do not cover, search that tool's `REFERENCE.md` (every command and its parameters); do not read it whole.
- For how a feature works (not just its parameters), read the tool's official GitHub docs, linked in README.md, before experimenting.
- Only explore a tool's own help when a command fails or the reference is out of date (then run `python tools/gen_reference.py <tool>`);
  update the notes with what you confirmed.
- Always render the output to PNG and look at it before reporting a document or deck as done.
- Keep this repo generic: no project names, people, company data, or screenshots from private work.
