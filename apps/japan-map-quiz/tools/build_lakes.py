"""琵琶湖の輪郭 → data/lakes.json（地図の上に海と同じ色で重ねる湖）

使い方:  python3 tools/build_lakes.py <ne_10m_lakes.geojson>
    入手先: https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes.geojson
投影は build_paths.py と同じ（x = (経度-128)×cos36°×60, y = (45.8-緯度)×60）。
"""
from pathlib import Path
import json, math, sys

DATA = Path(__file__).resolve().parent.parent / "data"
K = math.cos(math.radians(36)); LON0, LAT1, S = 128.0, 45.8, 60.0
proj = lambda x, y: ((x - LON0) * K * S, (LAT1 - y) * S)
# 名前, 県コード, 県名ラベルの置き場所（湖の上に県名が乗らないよう、湖を除いた陸の一番広い所。shapely の polylabel で求めた点）
LAKES = {"Biwa Ko": ("琵琶湖", 25, [398.8, 646.1])}

d = json.load(open(sys.argv[1], encoding="utf-8"))
out = []
for ft in d["features"]:
    name = ft["properties"].get("name")
    if name not in LAKES:
        continue
    g = ft["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    parts = []
    for poly in polys:
        ring = poly[0]
        pts = [proj(x, y) for x, y in ring]
        parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts[:-1]) + "Z")
    jp, code, label = LAKES[name]
    out.append({"name": jp, "c": code, "l": label, "d": "".join(parts)})
(DATA / "lakes.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"lakes: {[o['name'] for o in out]}")
