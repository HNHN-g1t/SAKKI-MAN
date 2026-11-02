"""src/template.html に地図データ（__PATHS__ ← data/paths.json、__REGIONS__ ← data/regions.json）と
都市データ（__CITIES__ ← data/cities.json）、地形データ（__TERRAIN__ ← data/terrain.json）を埋め込んで index.html を作る。

使い方:  python3 tools/build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
for key, file in (("__PATHS__", "paths.json"), ("__REGIONS__", "regions.json"), ("__CITIES__", "cities.json"), ("__TERRAIN__", "terrain.json")):
    assert template.count(key) == 1, f"template に {key} が1つだけ必要"
    template = template.replace(key, (ROOT / "data" / file).read_text(encoding="utf-8"))
out = ROOT / "index.html"
# Windows でも改行を LF にそろえる（どの端末でビルドしても同じ出力になるように）
out.write_text(template, encoding="utf-8", newline="\n")
print(f"wrote {out} ({out.stat().st_size:,} bytes)")
