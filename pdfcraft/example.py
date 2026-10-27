"""Example PDF: new document, text, page footer, watermark, then a PNG of page 1. Writes to ../out/."""

import json
import os
import subprocess

PDF = r"C:\Program Files\PdfCraft\pdfcraft-cli.exe"
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out"))


def run_script(steps, name):
    """Run pdfcraft tools from a JSON script (UTF-8, no BOM) and return the --report result."""
    path = os.path.join(OUT_DIR, f"{name}-script.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(steps, f)
    r = subprocess.run([PDF, "run", "--script", path, "--report"], capture_output=True, text=True, encoding="utf-8")
    os.remove(path)
    if r.returncode != 0:
        raise SystemExit(f"pdfcraft failed:\n{r.stderr[-2000:]}\n{r.stdout[-2000:]}")
    return json.loads(r.stdout)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "example.pdf")
    run_script(
        [
            {"tool": "doc_create", "args": {"from": "blank", "pages": 2, "width": 595, "height": 842}},
            {
                "tool": "page_add_text",
                "args": {"doc": 1, "page": 1, "at": [72, 72], "width": 450, "text": "Example PDF",
                         "size": 28, "bold": True, "color": "#12384D"},
            },
            {
                "tool": "page_add_text",
                "args": {"doc": 1, "page": 1, "at": [72, 120], "width": 450, "size": 12,
                         "text": "Built with pdfcraft-cli run --script. Positions are points from the top-left."},
            },
            {"tool": "doc_header_footer", "args": {"doc": 1, "footer_center": "Page <<1>> of <<n>>", "font_size": 9}},
            {"tool": "doc_watermark", "args": {"doc": 1, "text": "DRAFT", "opacity": 0.15, "rotation": 45, "font_size": 96}},
            {"tool": "doc_save", "args": {"doc": 1, "path": out}},
        ],
        "example",
    )
    png = os.path.join(OUT_DIR, "example-pdf-page-1.png")
    subprocess.run([PDF, "render", out, "--page", "1", "--dpi", "72", "--out", png], check=True)
    print("built", out, "and", png)
