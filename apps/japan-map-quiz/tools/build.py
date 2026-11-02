"""src/template.html の __PATHS__ に data/paths.json を埋め込んで index.html を作る。

使い方:  python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
paths = (ROOT / "data" / "paths.json").read_text(encoding="utf-8")
assert template.count("__PATHS__") == 1, "template に __PATHS__ が1つだけ必要"
out = ROOT / "index.html"
# Windows でも改行を LF にそろえる（どの端末でビルドしても同じ出力になるように）
out.write_text(template.replace("__PATHS__", paths), encoding="utf-8", newline="\n")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
