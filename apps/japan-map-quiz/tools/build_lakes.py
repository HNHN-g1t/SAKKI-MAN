"""湖の輪郭 → data/lakes.json（地図の上に海と同じ色で重ねる湖）

使い方:  python3 tools/build_lakes.py <inwatera.geojson>
    入手先: 地球地図日本（国土地理院、1:100万）の内水面 inwatera
        https://raw.githubusercontent.com/hfu/gmjp22topojson/master/inwatera.geojson
    （Natural Earth の湖データには日本の湖が琵琶湖しかないため、2026-11-22 に地球地図日本へ切りかえた）
投影は build_paths.py と同じ（x = (経度-128)×cos36°×60, y = (45.8-緯度)×60）。
面積の大きい湖ベスト10（琵琶湖・霞ヶ浦・サロマ湖・猪苗代湖・中海・屈斜路湖・宍道湖・支笏湖・洞爺湖・浜名湖）と、
霞ヶ浦の北浦、地形クイズに出る十和田湖を描く。県名ラベルが湖にかかる県は、湖を除いた陸のいちばん広い所（polylabel）へ移す。
"""
from pathlib import Path
import json, math, re, sys
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union, polylabel

DATA = Path(__file__).resolve().parent.parent / "data"
K = math.cos(math.radians(36)); LON0, LAT1, S = 128.0, 45.8, 60.0
proj = lambda x, y: ((x - LON0) * K * S, (LAT1 - y) * S)
# id, 名前, 県コード（ラベルを動かす県）, 地球地図の名前 または 中心の経緯度（名前のない湖）
LAKES = [
    ("biwa", "琵琶湖", [25], "BIWA KO"),
    ("kasumi", "霞ヶ浦", [8], "KASUMI-GA URA"),
    ("kitaura", "北浦", [8], "KITA URA"),
    ("saroma", "サロマ湖", [1], "SAROMA KO"),
    ("inawashiro", "猪苗代湖", [7], "INAWASHIRO KO"),
    ("nakaumi", "中海", [32, 31], (133.225, 35.468)),
    ("kussharo", "屈斜路湖", [1], "KUSSHARO KO"),
    ("shinji", "宍道湖", [32], (132.958, 35.443)),
    ("shikotsu", "支笏湖", [1], "SHIKOTSU KO"),
    ("toya", "洞爺湖", [1], "TOYA KO"),
    ("hamana", "浜名湖", [22], "HAMANA KO"),
    ("towada", "十和田湖", [2, 5], "TOWADA KO"),
]

def rings_of(g):
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    return [pl[0] for pl in polys]

src = json.load(open(sys.argv[1], encoding="utf-8"))["features"]
def find(key):
    if isinstance(key, str):
        return [f for f in src if f["properties"].get("nam") == key][0]
    best = None
    for f in src:
        r = rings_of(f["geometry"])[0]
        cx = sum(p[0] for p in r) / len(r); cy = sum(p[1] for p in r) / len(r)
        dd = (cx - key[0]) ** 2 + (cy - key[1]) ** 2
        if best is None or dd < best[0]: best = (dd, f)
    return best[1]

out, shapes = [], []
for lid, name, codes, key in LAKES:
    f = find(key)
    polys = [Polygon([proj(x, y) for x, y in r]).buffer(0).simplify(0.15) for r in rings_of(f["geometry"])]
    d = "".join("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in list(p.exterior.coords)[:-1]) + "Z" for p in polys)
    shapes.append((codes, unary_union(polys)))
    out.append({"id": lid, "name": name, "c": codes[0], "d": d})

# 県名ラベル：今の位置が湖の上（または湖のすぐそば）なら、湖を除いた陸のいちばん広い所へ
paths = {int(p["c"]): p for p in json.load(open(DATA / "paths.json", encoding="utf-8"))}
def pref_poly(dstr):
    ps = []
    for part in re.findall(r"M[^M]+", dstr):
        pts = [tuple(map(float, xy.split(","))) for xy in re.findall(r"-?[\d.]+,-?[\d.]+", part)]
        if len(pts) >= 3: ps.append(Polygon(pts).buffer(0))
    return unary_union(ps)
moved = {}
for codes, lake in shapes:
    for c in codes:
        p = paths[c]; lab = json.loads(p["l"]) if isinstance(p["l"], str) else p["l"]
        if Point(lab).distance(lake) > 12: continue
        land = pref_poly(p["d"]).difference(unary_union([s for cs, s in shapes if c in cs]).buffer(4))
        big = max(getattr(land, "geoms", [land]), key=lambda g: g.area)
        pt = polylabel(big, tolerance=0.5)
        moved[c] = [round(pt.x, 1), round(pt.y, 1)]
# ラベルを動かす県は、県ごとに1回だけ書く
labels = {str(c): xy for c, xy in moved.items()}
(DATA / "lakes.json").write_text(json.dumps({"lakes": out, "labels": labels}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("lakes:", [o["name"] for o in out]); print("labels moved:", labels)
