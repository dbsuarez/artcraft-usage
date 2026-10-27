"""Example Word document. Run: python example.py (writes to ../out/)."""

import os

from doclib import Doc, render

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")

doc = Doc()
doc.title("How a request moves", "An example built with doclib.py")
doc.h1("Overview", page_break=True)
doc.para("A request goes through **three steps**: submit, review, and decide.")
doc.bullets(["**Submit:** fill in the form.", "**Review:** someone checks it.", "**Decide:** you get an answer."])
doc.callout("Tip: every block starts with start(), so formatting never leaks into the next paragraph.")
doc.h2("Steps in order")
doc.bullets(["Open the form", "Fill in every field", "Press Submit"], numbered=True)
doc.warn("Check the dates before you submit.")
doc.h2("Timing")
doc.table([["Step", "Who", "Days"], ["Review", "Reviewer", "2"], ["Decide", "Manager", "1"]], [200, 171, 80])
doc.good("Done. Render the pages and look at them before sharing.")

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "example.docx")
    pages = doc.save(out)
    for p in range(1, pages + 1):
        render(out, os.path.join(OUT_DIR, f"example-page-{p}.png"), page=p)
    print(f"built {out} ({pages} pages)")
