"""Example drawing: shapes, outline, and text, exported to SVG and PNG. Writes to ../out/."""

import json
import os
import subprocess

VEC = r"C:\Program Files\VectorCraft\vectorcraft-cli.exe"
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out"))


def run(steps, exports, scale=2, name="vector"):
    """Run commands from a JSON file (Windows quoting breaks inline JSON) and export each path."""
    path = os.path.join(OUT_DIR, f"{name}-script.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump([{"command": c, "params": p} for c, p in steps], f)
    args = [VEC, "run", "--commands", path]
    for e in exports:
        args += ["--export", e]
    r = subprocess.run(args + ["--scale", str(scale)], capture_output=True, text=True, encoding="utf-8")
    os.remove(path)
    if r.returncode != 0:
        raise SystemExit(f"vectorcraft failed:\n{r.stderr[-2000:]}\n{r.stdout[-2000:]}")
    return [json.loads(line) for line in r.stdout.splitlines() if line.strip()]


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    svg, png = os.path.join(OUT_DIR, "example.svg"), os.path.join(OUT_DIR, "example-vector.png")
    run(
        [
            ("file.new", {"width": 400, "height": 200, "units": "Points"}),
            ("shape.rectangle", {"x": 20, "y": 20, "width": 160, "height": 80, "radius": 12}),
            ("paint.setFill", {"color": "#1b7fa6"}),
            ("paint.setStroke", {"none": True}),
            ("shape.ellipse", {"x": 220, "y": 20, "width": 80, "height": 80}),
            ("paint.setFill", {"color": "#f78154"}),
            ("paint.setStroke", {"color": "#12384d"}),
            ("stroke.set", {"weight": 4}),
            ("text.create", {"x": 20, "y": 150, "text": "Example drawing", "size": 28, "color": "#12384d"}),
        ],
        [svg, png],
    )
    print("built", svg, "and", png)
