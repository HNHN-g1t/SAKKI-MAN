from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / "data"
import json, math, sys
from shapely.geometry import shape, MultiPolygon, Polygon
from shapely.affinity import translate

src = sys.argv[1]
TOL = float(sys.argv[2]) if len(sys.argv) > 2 else 0.012
with open(src, encoding="utf-8") as f:
    d = json.load(f)

K = math.cos(math.radians(36))
LON0, LAT1 = 128.0, 45.8
S = 60.0  # px per degree (lon*K)

# Okinawa inset offset (degrees), moves main island to the top-left sea area
OKI_DX, OKI_DY = 1.6, 16.0


def keep(code, poly):
    c = poly.centroid
    if code == 13 and c.y < 33.0:  # Ogasawara
        return False
    if code == 47 and (c.x < 126.5 or c.x > 129):  # Miyako, Yaeyama, Daito
        return False
    return True


def proj(x, y):
    return ((x - LON0) * K * S, (LAT1 - y) * S)


out = []
for ft in d["features"]:
    p = ft["properties"]
    code = int(p["iso_3166_2"].split("-")[1])
    g = shape(ft["geometry"])
    polys = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    polys = [q for q in polys if keep(code, q)]
    biggest = max(polys, key=lambda q: q.area)
    # drop tiny islets except the main body
    polys = [q for q in polys if q is biggest or q.area > 0.0015]
    parts = []
    xs, ys = [], []
    for q in polys:
        q = q.simplify(TOL, preserve_topology=True)
        if q.is_empty:
            continue
        ring = list(q.exterior.coords)
        pts = [proj(x, y) for x, y in ring]
        xs += [a for a, _ in pts]; ys += [b for _, b in pts]
        parts.append("M" + "L".join(f"{a:.1f},{b:.1f}" for a, b in pts[:-1]) + "Z")
    bb = biggest.bounds
    bx0, by1 = proj(bb[0], bb[1]); bx1, by0 = proj(bb[2], bb[3])
    rp = biggest.representative_point()
    lx, ly = proj(rp.x, rp.y)
    extra = {}
    if code == 47:
        # inset copy: same scale, shifted so its box sits in the sea south of Kyushu/Shikoku
        TX, TY = -94.0, 887.0
        sx, sy = TX - min(xs), TY - min(ys)
        def sh(dstr):
            import re
            return re.sub(r"(-?\d+\.?\d*),(-?\d+\.?\d*)", lambda m: f"{float(m.group(1))+sx:.1f},{float(m.group(2))+sy:.1f}", dstr)
        extra = {"di": sh("".join(parts)), "li": [round(lx + sx, 1), round(ly + sy, 1)],
                 "bi": [round(min(xs)+sx, 1), round(min(ys)+sy, 1), round(max(xs)+sx, 1), round(max(ys)+sy, 1)]}
    out.append({**extra,
        "c": code,
        "d": "".join(parts),
        "l": [round(lx, 1), round(ly, 1)],
        "b": [round(bx0, 1), round(by0, 1), round(bx1, 1), round(by1, 1)],
    })

out.sort(key=lambda o: o["c"])
allx = [o["b"][0] for o in out] + [o["b"][2] for o in out]
ally = [o["b"][1] for o in out] + [o["b"][3] for o in out]
print("count", len(out), "bounds", min(allx), min(ally), max(allx), max(ally))
print("size", len(json.dumps(out, separators=(",", ":"))))
oki = out[46]["b"]
print("okinawa box", oki)
with open(str(DATA / "paths.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, separators=(",", ":"))
