"""Example part: a 60 x 40 x 8 mm plate with rounded corners and a hole, exported to STEP and STL,
measured, and pictured. Writes to ../out/."""

import json
import os
import subprocess

SOLID = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out"))


def run(steps, outputs, save=None, name="solid"):
    """Run commands from a JSON script and write each output (format from its extension)."""
    path = os.path.join(OUT_DIR, f"{name}-script.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"commands": [{"command": c, "params": p} for c, p in steps]}, f)
    args = [SOLID, "run", path]
    for o in outputs:
        args += ["--out", o]
    if save:
        args += ["--save", save]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    os.remove(path)
    if r.returncode != 0:
        raise SystemExit(f"solidcraft failed:\n{r.stderr[-2000:]}\n{r.stdout[-2000:]}")


def measure(design):
    r = subprocess.run([SOLID, "eval", design], capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(r.stdout)["bodies"][0]


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    design = os.path.join(OUT_DIR, "example-plate.sc")
    corners = [[0, 0, 4], [60, 0, 4], [60, 40, 4], [0, 40, 4]]  # a point on each vertical edge
    run(
        [
            ("sketch.create", {"plane": "XY"}),
            ("sketch.rectangle.two_point", {"p0": [0, 0], "p1": [60, 40]}),
            ("solid.extrude", {"distance": 8}),
            ("solid.fillet", {"edges": corners, "radius": 5}),
            ("solid.hole", {"position": [30, 20, 8], "diameter": 10, "through_all": True}),
        ],
        [os.path.join(OUT_DIR, "example-plate.step"), os.path.join(OUT_DIR, "example-plate.stl")],
        save=design,
    )
    body = measure(design)
    png = os.path.join(OUT_DIR, "example-plate.png")
    subprocess.run(
        [SOLID, "snapshot", design, "--out", png, "--view", "iso", "--width", "640", "--height", "400"],
        check=True,
        capture_output=True,
    )
    print(f"built {design}: volume {body['volume_mm3']:.0f} mm3, {body['faces']} faces, picture {png}")
