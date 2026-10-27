"""PhotoCraft helper; Python standard library only."""
import json
import subprocess
from pathlib import Path

class Photo:
    def __init__(self, exe=r"C:\Program Files\PhotoCraft\photocraft-cli.exe"):
        self.exe = exe

    def call(self, *args):
        p = subprocess.run([self.exe, *map(str, args)], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        if p.returncode:
            raise RuntimeError(f"PhotoCraft exit {p.returncode}: {p.stdout}\n{p.stderr}")
        if p.stderr.strip():
            print(p.stderr.strip())
        return p.stdout

    def info(self, source):
        return json.loads(self.call("info", source, "--compact"))

    def run(self, source, out, steps=(), *, new=None):
        if (source is None) == (new is None):
            raise ValueError("Provide source or new, exclusively")
        out = Path(out).resolve()
        if out.exists():
            raise FileExistsError(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        args = ["run", str(source)] if source else ["run", "--new", json.dumps(new)]
        for command, params in steps:
            args += ["--cmd", command, "--params", json.dumps(params)]
        self.call(*args, "--out", out)
        if not out.is_file():
            raise RuntimeError(f"Missing output: {out}")
        return out
