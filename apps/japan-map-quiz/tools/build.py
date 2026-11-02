"""src/template.html の __PATHS__ に data/paths.json、__CITIES__ に data/cities.json を埋め込んで index.html を作る。

使い方:  python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
for key, file in (("__PATHS__", "paths.json"), ("__CITIES__", "cities.json")):
    assert template.count(key) == 1, f"template に {key} が1つだけ必要"
    template = template.replace(key, (ROOT / "data" / file).read_text(encoding="utf-8"))
out = ROOT / "index.html"
# Windows でも改行を LF にそろえる（どの端末でビルドしても同じ出力になるように）
out.write_text(template, encoding="utf-8", newline="\n")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
