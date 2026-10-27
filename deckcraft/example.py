"""Two-slide example deck. Run: python example.py (writes to ../out/)."""

import os

from decklib import CORAL, LIGHT, MINT, NAVY, TEAL, WHITE, build

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")


def title(s):
    s.add("design.background", {"color": NAVY})
    s.text([80, 190, 800, 70], "How a request moves", size=40, bold=True, color=WHITE)
    s.text([82, 265, 800, 36], "An example built with decklib.py", size=18, color=LIGHT)


def flow(s):
    s.header("Three steps", "Boxes, arrows, icons, a numbered list, and a table")
    for i, (label, fill, icon) in enumerate(
        [("Submit", TEAL, "file-text"), ("Review", MINT, "search"), ("Decide", CORAL, "circle-check")]
    ):
        x = 80 + i * 290
        s.box([x, 150, 220, 90], label, fill=fill, color=WHITE, size=20, bold=True)
        s.icon(icon, [x + 12, 162, 24, 24], WHITE)
        if i < 2:
            s.arrow(x + 225, 195, x + 285, 195)
    s.steps([80, 280, 380, 150], ["Fill in the form", "Someone checks it", "You get an answer"])
    s.table([520, 280, 360, 120], [["Step", "Days"], ["Review", "2"], ["Decide", "1"]], widths=[240, 120])
    s.note([80, 450, 800, 50], "Render every slide to PNG and look at it before calling it done.", icon="lightbulb")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    deck = os.path.join(OUT_DIR, "example.deckcraft")
    build(
        [title, flow],
        deck,
        title="Example deck",
        png_dir=os.path.join(OUT_DIR, "example-slides"),
        pptx=os.path.join(OUT_DIR, "example.pptx"),
    )
    print("built", deck)
