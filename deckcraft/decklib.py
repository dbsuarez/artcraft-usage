"""Small helper for driving deckcraft-cli from Python.

Collect commands for one slide in a `Slide`, then `build()` runs one deckcraft-cli call per slide
(the CLI has no script file and Windows limits command-line length).
"""

import json
import subprocess

DECK = r"C:\Program Files\DeckCraft\deckcraft-cli.exe"

# Palette (calm teal and navy, suits the Harbor theme)
NAVY = "#12384D"
TEAL = "#1B7FA6"
MINT = "#36B3A8"
SAND = "#F2C14E"
CORAL = "#F78154"
INK = "#1E2B3C"
MUTED = "#5B6B7A"
LIGHT = "#E4EEF2"
WHITE = "#FFFFFF"
RED = "#D64545"
GREEN = "#2EA36F"
BORDER = "#C9D6DE"


def c(cmd, params=None):
    """Format one `--cmd` argument: `id` or `id={json}`."""
    if params is None:
        return cmd
    return f"{cmd}={json.dumps(params)}"


class Slide:
    def __init__(self):
        self.cmds = []

    def add(self, cmd, params=None):
        self.cmds.append(c(cmd, params))
        return self

    def box(
        self,
        rect,
        text="",
        fill=None,
        line=None,
        preset="roundRect",
        size=16,
        color=INK,
        bold=False,
        align="center",
        anchor="middle",
        line_width=1.5,
        font=None,
    ):
        """A shape with optional fill, outline, and text. `rect` is [x, y, w, h] in points."""
        self.add("shape.insert", {"preset": preset, "rect": rect, "text": text})
        self.add("shape.fill", {"color": fill} if fill else {"none": True})
        self.add("shape.line", {"color": line, "width": line_width} if line else {"none": True})
        if text:
            self.add(
                "format.fontDialog",
                {"size": size, "bold": bold, "color": color, **({"family": font} if font else {})},
            )
            self.add("format.align", {"align": align})
            self.add("format.anchor", {"anchor": anchor})
            self.add("format.autofit", {"mode": "none"})
            self.add("format.wrap", {"on": True})
        return self

    def text(self, rect, text, size=16, color=INK, bold=False, align="left", anchor="top", font=None):
        return self.box(
            rect, text, preset="rect", size=size, color=color, bold=bold, align=align, anchor=anchor, font=font
        )

    def arrow(self, x1, y1, x2, y2, color=MUTED, width=2.5):
        """Arrow from (x1, y1) to (x2, y2). Connectors draw left-to-right and top-to-bottom, so flip as needed."""
        x, y = min(x1, x2), min(y1, y2)
        w, h = max(abs(x2 - x1), 1), max(abs(y2 - y1), 1)
        self.add("shape.insert", {"preset": "straightConnector1", "rect": [x, y, w, h]})
        self.add("shape.line", {"color": color, "width": width, "tail": "triangle", "tailSize": "med"})
        if x2 < x1:
            self.add("shape.flip", {"axis": "horizontal"})
        if y2 < y1:
            self.add("shape.flip", {"axis": "vertical"})
        return self

    def icon(self, name, rect, color):
        """Icons are outlines: color them with shape.line, fill does nothing."""
        self.add("insert.icon", {"name": name, "rect": rect})
        self.add("shape.line", {"color": color})
        return self

    def header(self, title, subtitle=None):
        self.box([60, 30, 56, 6], fill=TEAL, preset="rect")
        self.text([56, 42, 850, 50], title, size=28, bold=True, color=NAVY)
        if subtitle:
            self.text([58, 92, 850, 30], subtitle, size=15, color=MUTED)
        return self

    def note(self, rect, text, fill=LIGHT, color=NAVY, size=14, icon=None):
        """A rounded callout, with an optional icon at the left."""
        self.box(rect, text, fill=fill, size=size, color=color, align="left", preset="roundRect")
        self.add("format.margins", {"left": 44 if icon else 14, "right": 14})
        if icon:
            self.icon(icon, [rect[0] + 12, rect[1] + rect[3] / 2 - 11, 22, 22], color)
        return self

    def steps(self, rect, items, size=14, color=INK, number_color=TEAL):
        """A numbered list in one text box."""
        self.box(rect, "\n".join(items), preset="rect", size=size, color=color, align="left", anchor="top")
        self.add("format.numbering", {"on": True, "scheme": "arabicPeriod", "color": number_color})
        self.add("format.paragraph", {"spaceAfter": 6})
        self.add("format.margins", {"left": 4, "right": 4, "top": 2})
        return self

    def picture(self, path, box, align="center", border=BORDER):
        """Insert an image scaled to fit `box` [x, y, w, h], keeping its aspect ratio (needs Pillow)."""
        from PIL import Image

        w, h = Image.open(path).size
        bx, by, bw, bh = box
        scale = min(bw / w, bh / h)
        pw, ph = round(w * scale, 1), round(h * scale, 1)
        x = bx + (bw - pw) / 2 if align == "center" else bx
        self.add("insert.picture", {"path": path, "rect": [x, by, pw, ph]})
        if border:
            self.add("shape.line", {"color": border, "width": 1})
        return [x, by, pw, ph]

    def table(self, rect, rows, size=12, style="medium2-accent1", widths=None):
        """A table filled from a list of rows; the first row is the header."""
        self.add("insert.table", {"rows": len(rows), "cols": len(rows[0]), "rect": rect})
        self.add("table.style", {"style": style})
        for r, row in enumerate(rows):
            for col, cell in enumerate(row):
                self.add("text.set", {"text": cell, "cell": [r, col]})
        self.add("text.exit")
        self.add("format.size", {"size": size})
        self.add("table.cellAlign", {"anchor": "middle"})
        for col, width in enumerate(widths or []):
            self.add("table.columnWidth", {"col": col, "width": width})
        return self


def run(cmds, src=None, save=None, export=None, export_params=None):
    args = [DECK, "run"]
    if src:
        args += ["--in", src]
    for x in cmds:
        args += ["--cmd", x]
    if save:
        args += ["--save", save]
    if export:
        args += ["--export", export]
    if export_params:
        args += ["--export-params", json.dumps(export_params)]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"deckcraft failed:\n{r.stderr}\n{r.stdout[-2000:]}")
    return r.stdout


def build(slide_fns, out, theme="Harbor", title=None, png_dir=None, pptx=None):
    """Build a deck from functions that each fill one `Slide`, one CLI run per slide.

    Optionally sets the title, exports every slide to PNG (to check the result), and writes a .pptx copy.
    """
    for i, fn in enumerate(slide_fns):
        s = Slide()
        if i == 0:
            s.add("design.theme", {"name": theme})
            s.add("slide.layout", {"layout": "blank"})
        else:
            s.add("slide.last")
            s.add("slide.new", {"layout": "blank"})
        fn(s)
        try:
            run(s.cmds, src=out if i else None, save=out)
        except SystemExit as exc:
            raise SystemExit(f"slide {i + 1} ({fn.__name__}): {exc}")
    final = [c("design.headerFooter", {"slideNumber": True, "hideOnTitle": True, "all": True})]
    if title:
        final.append(c("file.properties", {"title": title}))
    run(final, src=out, save=out)
    if png_dir:
        import os

        os.makedirs(png_dir, exist_ok=True)
        for i in range(len(slide_fns)):
            run(
                [c("slide.go", {"index": i})],
                src=out,
                export=os.path.join(png_dir, f"slide-{i + 1:02d}.png"),
                export_params={"slide": i},
            )
    if pptx:
        r = subprocess.run([DECK, "convert", out, pptx], capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise SystemExit(f"convert failed:\n{r.stderr}")
