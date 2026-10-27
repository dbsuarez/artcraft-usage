# SoundCraft CLI notes

Verified on 2026-10-27 against `C:\Program Files\SoundCraft\soundcraft-cli.exe` (a Pro Tools-style audio editor).
Every command and its parameters: [REFERENCE.md](REFERENCE.md) (search it, do not read it whole).
`example.py` runs both workflows below.

## Simple jobs (no session)

| Job | Command |
| --- | --- |
| File summary | `soundcraft-cli info file.wav` (channels, rate, seconds, JSON) |
| Convert | `soundcraft-cli convert in.wav out.flac [--bit-depth 16\|24\|32f] [--rate 44100] [--normalize]` |

Writes **wav, aif/aiff, and flac only** (no mp3). Reads common audio files.

## Editing (script)

`soundcraft-cli script steps.txt [--in S.scraft] [--save S.scraft] [--bounce out.wav [--start T --end T]]`

- `steps.txt` has one `command.id {json}` per line. Write it from Python (`json.dumps`): Windows paths need escaped backslashes.
- `--bounce` writes the mix (wav, aiff, or flac by extension) of the whole session unless `--start`/`--end` are given, and prints its loudness and peak.
- `run --cmd ID=JSON ...` does the same inline, but quoting JSON on Windows breaks; prefer a script file.
- Times are strings in seconds (`"1.5"`); results report samples (at 48 kHz, 1 s = 48000).
- Track and clip ids are shared object ids, not 1, 2, 3 per kind (an imported track was id 2). Use the id a step returns,
  a track name, or leave `tracks` out to act on the current selection.
- Most edits act on the edit selection: set it first with `edit.select` or `edit.select_all`.

| Purpose | Command and params |
| --- | --- |
| New session | `session.new {"name", "sample_rate": 48000, "bit_depth": 24}` |
| New track | `track.new {"kind": "audio", "format": "mono" \| "stereo", "name"}` (also aux, midi, instrument) |
| Import audio | `file.import_audio {"path"}` (new track by default; returns the track and clip ids) |
| Select | `edit.select_all {}`; `edit.select {"tracks": [id or name], "start": "1.5", "end": "2"}` |
| Tone | `audiosuite.process {"process": "signal_generator", "params": {"frequency": 440, "level": -12}}` fills the selection |
| Normalize | `audiosuite.process {"process": "normalize"}` (peak -0.1 dB; a `peak_db` param was ignored) |
| Other processing | `audiosuite.process {"process": "gain" \| "reverse" \| "pitch_shift" \| "time_stretch" \| <plugin id>}`; plugin ids from `soundcraft-cli plugins` (eq_7band, compressor, de_esser, maximizer, room_reverb...) |
| Fade | `edit.fades_create {"shape": "s-curve"}` over the selection (linear, equal power, exponential, logarithmic) |
| Volume | `mix.volume {"tracks", "db"}` |
| Bounce from a step | `file.bounce_mix {"path", "format", "bit_depth", "normalize"}`; stems: `file.bounce_stems {"dir"}` |
| MIDI | `midi.new_clip {"track"}`, `midi.note_add {"clip", "pitch", "start_ticks", "length_ticks": 480}` |
| Save | `session.save_as {"path": "x.scraft"}` or `--save` |

Check results with `soundcraft-cli info out.wav` and the bounce line (peak and LUFS); there is no picture to look at.
