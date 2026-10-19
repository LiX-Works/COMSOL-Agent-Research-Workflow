#!/usr/bin/env python3
"""Replot the existing S2 scan as a scientific two-panel figure; no solver call."""

import argparse
import csv
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


def outline():
    vertices = [(-0.5, 0), (0.5, 0)]
    for c in (3, 6.5, 10, 13.5):
        vertices += [(0.5,c-0.5),(4,c-0.5),(4,c+0.5),(0.5,c+0.5)]
    vertices += [(0.5,16),(-0.5,16)]
    for c in (13.5,10,6.5,3):
        vertices += [(-0.5,c+0.5),(-4,c+0.5),(-4,c-0.5),(-0.5,c-0.5)]
    return np.array(vertices+[vertices[0]])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-csv", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[2]/"examples/edge-current/assets")
    args = parser.parse_args()
    with args.source_csv.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    xs = np.array(sorted({float(r["x_um"]) for r in rows}))
    ys = np.array(sorted({float(r["y_um"]) for r in rows}))
    if (len(xs),len(ys),len(rows)) != (46,86,3956):
        parser.error("Expected the full 46 by 86 S2 map.")
    xi,yi = {x:i for i,x in enumerate(xs)},{y:i for i,y in enumerate(ys)}
    values = np.full((len(ys),len(xs)),np.nan)
    for r in rows:
        x,y=float(r["x_um"]),float(r["y_um"])
        if np.isfinite(values[yi[y],xi[x]]):
            parser.error("Duplicate scan position.")
        values[yi[y],xi[x]]=float(r["EdgeNormal_A"])
    if not np.isfinite(values).all():
        parser.error("Missing or non-finite result.")
    peak=float(np.max(np.abs(values)))
    if peak == 0:
        parser.error("Zero response map.")
    digest=hashlib.sha256(args.source_csv.read_bytes()).hexdigest()
    plt.rcParams.update({
        "font.family":"DejaVu Sans","font.size":19,
        "axes.labelsize":21,"axes.titlesize":22,"xtick.labelsize":18,
        "ytick.labelsize":18,"legend.fontsize":18,
        "axes.linewidth":1.15,"svg.fonttype":"none",
        "savefig.facecolor":"white","figure.facecolor":"white",
    })
    fig=plt.figure(figsize=(12,6.5),dpi=100)
    grid=fig.add_gridspec(1,2,width_ratios=(1,1.28),left=.075,right=.98,bottom=.16,top=.89,wspace=.48)
    ax=fig.add_subplot(grid[0,0])
    cmap=LinearSegmentedColormap.from_list("signed",["#254ab0","#ffffff","#c52a37"],N=256)
    im=ax.pcolormesh(xs,ys,values/peak,cmap=cmap,vmin=-1,vmax=1,shading="nearest")
    polygon=outline()
    ax.plot(polygon[:,0],polygon[:,1],color="black",lw=1.1)
    ax.set(aspect="equal",xlim=(-4.6,4.6),ylim=(-.6,16.6),
           xlabel="Spot x (µm)",ylabel="Spot y (µm)",title="Scanning response")
    ax.set_xticks([-4,0,4]);ax.set_yticks([0,4,8,12,16])
    ax.tick_params(direction="out",length=5)
    cb=fig.colorbar(im,ax=ax,fraction=.065,pad=.075,shrink=.91,ticks=[-1,0,1])
    cb.solids.set_rasterized(False)
    cb.set_label(r"$I\,/\,I_{\mathrm{peak}}$",labelpad=8)
    cb.outline.set_linewidth(.8)
    ax.text(-.34,1.06,"a",transform=ax.transAxes,fontweight="bold",fontsize=27)
    ax2=fig.add_subplot(grid[0,1])
    for c in (3,6.5,10,13.5):
        ax2.axvspan(c-.5,c+.5,color="#e8e8e8",zorder=0,lw=0)
    il=int(np.argmin(abs(xs+.7)));ir=int(np.argmin(abs(xs-.7)))
    assert abs(xs[il]+.7)<1e-9 and abs(xs[ir]-.7)<1e-9
    ax2.plot(ys,values[:,il]/peak,color="#3c68aa",lw=3.2,label="x = −0.7 µm",zorder=3)
    ax2.plot(ys,values[:,ir]/peak,color="#b94b4b",lw=2.1,ls=(0,(5,3)),label="x = +0.7 µm",zorder=4)
    ax2.axhline(0,color="#666666",lw=.9,zorder=1)
    ax2.set(xlim=(-.5,16.5),ylim=(-1.08,1.08),xlabel="Spot y (µm)",
            ylabel=r"$I\,/\,I_{\mathrm{peak}}$",title="Longitudinal profiles")
    ax2.set_xticks([0,4,8,12,16]);ax2.set_yticks([-1,-.5,0,.5,1])
    ax2.tick_params(direction="out",length=5)
    ax2.legend(loc="upper right",frameon=False,handlelength=2.8,borderpad=.2)
    ax2.spines[["top","right"]].set_visible(False)
    ax2.text(-.19,1.06,"b",transform=ax2.transAxes,fontweight="bold",fontsize=27)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    stem=args.output_dir/"example-results"
    description=("Replot of an existing independent public-source S2 simulation, not a new solve. "
                 "Panel a: every scan value on its original grid, without interpolation. "
                 "Panel b: exact x=-0.7 and +0.7 micrometre scan columns; grey bands mark cross arms. "
                 f"Both panels use the same full-S2-map peak {peak:.16e} A. "
                 "The source strength is arbitrary, without experimental amplitude calibration. "
                 f"Source CSV SHA256: {digest}. Reference DOI: 10.1038/s41565-018-0323-8.")
    fig.savefig(stem.with_suffix(".png"),dpi=100,metadata={"Description":description})
    fig.savefig(stem.with_suffix(".svg"),metadata={"Description":description,"Creator":"COMSOL Agent Research Workflow"})
    plt.close(fig)
    print(f"Saved {stem}.png and .svg; peak_A={peak:.16e}; source_sha256={digest}")


if __name__=="__main__":
    main()
