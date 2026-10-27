"""Example audio: generate a 2 s tone, then import it, normalize, and fade it out. Writes to ../out/."""

import json
import os
import subprocess

SND = r"C:\Program Files\SoundCraft\soundcraft-cli.exe"
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out"))


def script(steps, bounce, name="sound"):
    """Run `command {json}` lines from a file (json.dumps escapes Windows paths) and bounce the mix."""
    path = os.path.join(OUT_DIR, f"{name}-script.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(f"{cmd} {json.dumps(params)}\n" for cmd, params in steps)
    r = subprocess.run([SND, "script", path, "--bounce", bounce], capture_output=True, text=True, encoding="utf-8")
    os.remove(path)
    if r.returncode != 0:
        raise SystemExit(f"soundcraft failed:\n{r.stderr[-2000:]}\n{r.stdout[-2000:]}")
    return r.stdout


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    tone = os.path.join(OUT_DIR, "example-tone.wav")
    print(script(
        [
            ("session.new", {"name": "Tone", "sample_rate": 48000}),
            ("track.new", {"kind": "audio", "format": "stereo", "name": "Tone"}),
            ("edit.select", {"tracks": ["Tone"], "start": "0", "end": "2"}),
            ("audiosuite.process", {"process": "signal_generator", "params": {"frequency": 440, "level": -12}}),
        ],
        tone,
    ))
    edited = os.path.join(OUT_DIR, "example-edited.flac")
    print(script(
        [
            ("session.new", {"name": "Edit"}),
            ("file.import_audio", {"path": tone}),
            ("edit.select_all", {}),
            ("audiosuite.process", {"process": "normalize"}),
            ("edit.select", {"start": "1.5", "end": "2"}),
            ("edit.fades_create", {"shape": "s-curve"}),
        ],
        edited,
    ))
    print("built", tone, "and", edited)
