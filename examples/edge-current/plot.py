#!/usr/bin/env python3
"""Plot one full scan produced by scripts/comsol-run.py (no COMSOL process)."""

import argparse
import csv
import json
from pathlib import Path


def outline(shape):
    length = 16 if shape == "S2" else 9
    centers = [3, 6.5, 10, 13.5] if shape == "S2" else [4.5]
    points = [(-0.5, 0), (0.5, 0)]
    for y in centers:
        points += [(0.5, y-0.5), (4, y-0.5), (4, y+0.5), (0.5, y+0.5)]
    points += [(0.5, length), (-0.5, length)]
    for y in reversed(centers):
        points += [(-0.5, y+0.5), (-4, y+0.5), (-4, y-0.5), (-0.5, y-0.5)]
    return points + [points[0]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True, help="completed full-example run directory")
    parser.add_argument("--source", choices=("BulkFixed", "EdgeFixed", "EdgeNormal"), default="EdgeNormal")
    parser.add_argument("--output", type=Path, help="new PNG path; default: <run>/data/<source>.png")
    args = parser.parse_args()
    run = args.run.expanduser().resolve()
    manifest = json.loads((run / "run.json").read_text(encoding="utf-8"))
    if manifest["state"] != "COMPLETE" or manifest["plan"]["mode"] != "full-example":
        parser.error("Plotting requires a completed full-example run; smoke samples are not a resolved map.")
    output = args.output or run / "data" / f"{args.source}.png"
    if output.exists():
        parser.error(f"Output already exists; choose another filename: {output}")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    with (run / "data" / "scan.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    xs = sorted({float(row["x_um"]) for row in rows})
    ys = sorted({float(row["y_um"]) for row in rows})
    if len(xs)*len(ys) != len(rows):
        parser.error("The scan is not a complete rectangular grid.")
    xi, yi = {x: i for i, x in enumerate(xs)}, {y: i for i, y in enumerate(ys)}
    values = np.full((len(ys), len(xs)), np.nan)
    for row in rows:
        values[yi[float(row["y_um"])]][xi[float(row["x_um"])]] = float(row[args.source+"_A"])
    if not np.all(np.isfinite(values)):
        parser.error("Missing or non-finite scan values.")
    peak = float(np.max(np.abs(values)))
    if peak == 0:
        parser.error("The scan is identically zero.")
    shape = manifest["plan"]["geometry"]
    fig, ax = plt.subplots(figsize=(5.5, 7.5), constrained_layout=True)
    image = ax.pcolormesh(xs, ys, values/peak, cmap="RdBu_r", vmin=-1, vmax=1, shading="nearest")
    polygon = outline(shape)
    ax.plot([p[0] for p in polygon], [p[1] for p in polygon], color="black", linewidth=0.8)
    ax.set(aspect="equal", xlabel="Spot x (µm)", ylabel="Spot y (µm)",
           title=f"{shape}: {args.source}\nmax |I| = {peak*1e12:.4g} pA (arbitrary source amplitude)")
    fig.colorbar(image, ax=ax, label="Bottom current / own map max |I|")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=180)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
