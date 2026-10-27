"""Generic transparent image example; inspect the generated PNG."""
from pathlib import Path
from uuid import uuid4
from photolib import Photo

photo = Photo()
out = Path(__file__).resolve().parents[1] / "out" / ("photocraft-" + uuid4().hex[:8])
source = photo.run(None, out / "sprite.png", [
    ("shape.create", dict(kind="ellipse", rect=[16,16,96,96],
                          fill="#00BBDD", stroke=dict(width=4,color="#FFFFFF"), name="Circle"))
], new=dict(width=128,height=128,background="transparent",mode="rgb",depth=8))
result = photo.run(source, out / "padded.png", [
    ("image.crop", dict(x=8,y=8,width=112,height=112)),
    ("image.imageSize", dict(width=64,height=64,resample="nearest")),
    ("image.canvasSize", dict(width=96,height=96,anchor="center",extensionColor="transparent"))])
info = photo.info(result)
assert (info["width"],info["height"]) == (96,96), info
print(result)
