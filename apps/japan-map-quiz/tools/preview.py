from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / "data"
import json, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as P

data = json.load(open(str(DATA / "paths.json")))
fig, ax = plt.subplots(figsize=(9, 10))
for o in data:
    for part in re.findall(r"M([^Z]+)Z", o["d"]):
        pts = [tuple(map(float, s.split(","))) for s in part.split("L")]
        ax.add_patch(P(pts, closed=True, fc="#9cd", ec="k", lw=0.4))
    ax.text(o["l"][0], o["l"][1], str(o["c"]), fontsize=6, ha="center", va="center")
ax.set_xlim(0, 880); ax.set_ylim(980, 0); ax.set_aspect("equal")
plt.savefig(str(DATA / "preview.png"), dpi=90)
