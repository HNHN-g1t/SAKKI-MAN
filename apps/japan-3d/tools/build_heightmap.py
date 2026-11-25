"""日本列島のハイトマップ data/heightmap.webp と県境の線 data/borders.json を作る。

使い方:  python3 apps/japan-3d/tools/build_heightmap.py [タイルの置き場]
  - 標高は AWS の公開標高タイル（Terrarium 形式、ズーム8＝約500m）から取る
      https://elevation-tiles-prod.s3.amazonaws.com/terrarium/{z}/{x}/{y}.png
    （国土地理院の PNG 標高タイルに替えるときは fetch_tile() と decode() だけ直せばよい）
  - タイルは置き場（既定: apps/japan-3d/.tiles/、git には入れない）に保存し、2回目からはそれを使う
  - 座標は日本地図タップドリルと同じ投影（x = (経度-128)×cos36°×60、y = (45.8-緯度)×60）。3D では x→X、y→Z
  - 陸と海: 標高 > 0 か、ドリルの県の形（paths.json・hoppo.json）の中なら陸。琵琶湖など（lakes.json）は湖

heightmap.webp の中身（可逆 WebP。1画素＝0.5、左上が x=X0, y=Z0）
  R*256+G = 標高[m] + 12000   … 陸は 1m きざみ。海は海底の深さを 100m きざみ（色分けにだけ使う・軽くするため）
  B = 255 日本の陸 / 64 国外の陸（朝鮮半島・ロシア沿岸。平らなグレーで描く） / 128 湖 / 0 海
  国外の陸: 標高タイルの陸のうち、ドリルの県の形と重ならない大きなまとまり（5000画素以上）
"""
import concurrent.futures as cf
import io
import json
import math
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

APP = Path(__file__).resolve().parent.parent
QUIZ = APP.parent / "japan-map-quiz" / "data"
OUT = APP / "data"
K = math.cos(math.radians(36))
X0, Z0, CELL, W, H = -30.0, 0.0, 0.5, 2120, 2380
Z = 8


def proj(lat, lon):
    return ((lon - 128) * K * 60, (45.8 - lat) * 60)


def tile_dir():
    d = Path(sys.argv[1]) if len(sys.argv) > 1 else APP / ".tiles"
    d.mkdir(parents=True, exist_ok=True)
    return d


def fetch_tile(tx, ty, d):
    f = d / f"{Z}_{tx}_{ty}.png"
    if not f.exists():
        url = f"https://elevation-tiles-prod.s3.amazonaws.com/terrarium/{Z}/{tx}/{ty}.png"
        f.write_bytes(urllib.request.urlopen(url, timeout=60).read())
    return f


def decode(f):
    a = np.asarray(Image.open(f).convert("RGB"), dtype=np.float64)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def main():
    # 出力の各画素の緯度経度 → メルカトルのピクセル座標（ズーム Z、1タイル256px）
    xs = X0 + (np.arange(W) + 0.5) * CELL
    zs = Z0 + (np.arange(H) + 0.5) * CELL
    lon = 128 + xs / (K * 60)
    lat = 45.8 - zs / 60
    n = 2 ** Z * 256
    px = (lon + 180) / 360 * n
    py = (1 - np.log(np.tan(np.radians(lat)) + 1 / np.cos(np.radians(lat))) / math.pi) / 2 * n
    tx0, tx1 = int(px.min() // 256), int(px.max() // 256)
    ty0, ty1 = int(py.min() // 256), int(py.max() // 256)
    d = tile_dir()
    jobs = [(tx, ty) for tx in range(tx0, tx1 + 1) for ty in range(ty0, ty1 + 1)]
    print(f"tiles {len(jobs)}")
    with cf.ThreadPoolExecutor(16) as ex:
        files = dict(zip(jobs, ex.map(lambda j: fetch_tile(*j, d), jobs)))
    mosaic = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256))
    for (tx, ty), f in files.items():
        mosaic[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = decode(f)
    # 双線形で取り出す
    gx = px - tx0 * 256 - 0.5
    gy = py - ty0 * 256 - 0.5
    X, Y = np.meshgrid(gx, gy)
    x0 = np.clip(np.floor(X).astype(int), 0, mosaic.shape[1] - 2)
    y0 = np.clip(np.floor(Y).astype(int), 0, mosaic.shape[0] - 2)
    fx, fy = X - x0, Y - y0
    h = (mosaic[y0, x0] * (1 - fx) * (1 - fy) + mosaic[y0, x0 + 1] * fx * (1 - fy)
         + mosaic[y0 + 1, x0] * (1 - fx) * fy + mosaic[y0 + 1, x0 + 1] * fx * fy)

    # 陸・湖のマスク（ドリルの県の形をそのまま使う）
    mask = Image.new("L", (W, H), 0)
    dr = ImageDraw.Draw(mask)
    to_px = lambda x, y: ((x - X0) / CELL, (y - Z0) / CELL)
    paths = json.load(open(QUIZ / "paths.json", encoding="utf-8"))
    for p in paths:
        for ring in parse_path(p["d"]):
            dr.polygon([to_px(*q) for q in ring], fill=255)
    hoppo = json.load(open(QUIZ / "hoppo.json", encoding="utf-8"))
    for poly in hoppo["polys"]:
        dr.polygon([to_px(*proj(la, lo)) for lo, la in poly], fill=255)
    lakes = json.load(open(QUIZ / "lakes.json", encoding="utf-8"))["lakes"]
    lake_img = Image.new("L", (W, H), 0)
    ld = ImageDraw.Draw(lake_img)
    for lk in lakes:
        for ring in parse_path(lk["d"]):
            ld.polygon([to_px(*q) for q in ring], fill=255)
    poly = np.asarray(mask) > 0
    lake = np.asarray(lake_img) > 0
    land = (h > 0.5) | poly
    # 県の形の中なのに標高 0 以下（干拓地・海抜ゼロ地帯・形のずれ）は 1m にそろえて陸として描く
    h = np.where(poly & (h < 1), 1.0, h)
    # 県の形の外の小さな標高（タイルの誤差）は残す。湖は湖面の高さのまま色だけ水にする
    from scipy import ndimage
    lab, nlab = ndimage.label(land)
    sizes = np.bincount(lab.ravel())
    touch = np.zeros(nlab + 1, bool)
    touch[np.unique(lab[poly])] = True
    foreign_ids = np.where((~touch) & (sizes >= 5000))[0]
    foreign = np.isin(lab, foreign_ids[foreign_ids > 0])
    h = np.where(foreign, 1.0, h)
    b = np.where(lake, 128, np.where(foreign, 64, np.where(land, 255, 0))).astype(np.uint8)
    print("foreign px", int(foreign.sum()))
    h = np.where(b == 0, np.round(np.minimum(h, 0) / 100) * 100, np.round(h))
    v = np.clip(h + 12000, 0, 65535).astype(np.uint32)
    rgb = np.stack([(v >> 8).astype(np.uint8), (v & 255).astype(np.uint8), b], axis=-1)
    OUT.mkdir(exist_ok=True)
    Image.fromarray(rgb, "RGB").save(OUT / "heightmap.webp", lossless=True, quality=100, method=6)
    print("heightmap", W, H, "max", h.max(), "min", h.min(), (OUT / "heightmap.webp").stat().st_size // 1024, "KB")

    # 県境（2つの県が共有する辺）と海岸線（1つの県だけの辺）に分ける
    from collections import Counter
    rk = lambda q: (round(q[0], 1), round(q[1], 1))
    rings = [ring for p in paths for ring in parse_path(p["d"])]
    cnt = Counter(tuple(sorted([rk(a), rk(b_)])) for ring in rings for a, b_ in zip(ring, ring[1:] + ring[:1]))
    border, coast, done = [], [], set()
    for ring in rings:
        for a, b_ in zip(ring, ring[1:] + ring[:1]):
            key = tuple(sorted([rk(a), rk(b_)]))
            if key in done:
                continue
            done.add(key)
            (border if cnt[key] > 1 else coast).append([*rk(a), *rk(b_)])
    for poly_ in hoppo["polys"]:
        pts = [rk(proj(la, lo)) for lo, la in poly_]
        coast += [[*a, *b_] for a, b_ in zip(pts, pts[1:])]
    json.dump({"note": "線分 [x1,y1,x2,y2]。border＝県境、coast＝海岸線。日本地図タップドリルの paths.json・hoppo.json から",
               "border": border, "coast": coast}, open(OUT / "borders.json", "w"), separators=(",", ":"))
    print("border segs", len(border), "coast segs", len(coast), (OUT / "borders.json").stat().st_size // 1024, "KB")
    json.dump({"x0": X0, "z0": Z0, "cell": CELL, "w": W, "h": H, "k": K}, open(OUT / "grid.json", "w"))


def parse_path(d):
    rings = []
    for part in re.split(r"[Zz]", d):
        nums = re.findall(r"-?\d+(?:\.\d+)?", part)
        pts = [(float(nums[i]), float(nums[i + 1])) for i in range(0, len(nums) - 1, 2)]
        if len(pts) >= 3:
            rings.append(pts)
    return rings


if __name__ == "__main__":
    main()
