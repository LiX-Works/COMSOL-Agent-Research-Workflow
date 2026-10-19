"""Build the README workflow figure (assets/workflow.png) with the Python standard library.

Writes workflow.svg and a workflow.html wrapper next to the --output path; render the
HTML to PNG at 2x (3200 x 1760), e.g. with headless Chrome or Edge. The physical
graphics are illustrative and independent of the bundled example.
"""
from pathlib import Path
import argparse
import math
from xml.sax.saxutils import escape

cli = argparse.ArgumentParser(description=__doc__)
cli.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "workflow.svg")
args = cli.parse_args()

W, H = 1600, 880
FONT = "'Segoe UI Variable Display','Segoe UI',system-ui,sans-serif"
C = dict(
    ink="#16203A", sub="#2C3850", line="#2E3A55", card="#FFFFFF", cardStroke="#C3CDDD",
    band="#E9F0F9", amber="#E8960F", amberText="#A9650A", lead0="#22386A", lead1="#3866A6",
)
STEP = {  # accent, panel tint
    "build": ("#36579A", "#E4ECF8"),
    "run": ("#2F7D6B", "#E0F2EB"),
    "inspect": ("#5A3CC2", "#ECE6FB"),
    "refine": ("#C2760A", "#FCEFD6"),
}

out = []
add = out.append


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def text(x, y, s, size=26, weight=600, fill=C["ink"], anchor="start", extra=""):
    add(f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
        f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def line(d, stroke, width, extra=""):
    add(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def arrow(x1, y1, x2, y2, color=C["line"], marker="arrow"):
    add(f'<path d="M{f(x1)} {f(y1)} L{f(x2)} {f(y2)}" fill="none" stroke="{color}" '
        f'stroke-width="5.5" marker-end="url(#{marker})"/>')


# ---------- layout ----------
GAP = 120
CW, CH = 370, 300
X0, Y0 = 370, 100
cols = (X0, X0 + CW + GAP)
rows = (Y0, Y0 + CH + GAP)
cards = {
    "build": (cols[0], rows[0]), "run": (cols[1], rows[0]),
    "inspect": (cols[1], rows[1]), "refine": (cols[0], rows[1]),
}
HUB = (cols[0] + CW + GAP / 2, rows[0] + CH + GAP / 2)
SIDE_W = 250
IN_X, OUT_X = 40, W - 40 - SIDE_W


def step_card(key, n, title, caption):
    x, y = cards[key]
    accent, tint = STEP[key]
    add(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="24" fill="{C["card"]}" '
        f'stroke="{C["cardStroke"]}" stroke-width="1.8" filter="url(#shadow)"/>')
    add(f'<circle cx="{x + 46}" cy="{y + 46}" r="19" fill="{accent}"/>')
    text(x + 46, y + 55, str(n), 24, 700, "#FFFFFF", "middle")
    text(x + 80, y + 56, title, 30, 700)
    add(f'<rect x="{x + 28}" y="{y + 86}" width="{CW - 56}" height="150" rx="16" fill="{tint}"/>')
    text(x + CW / 2, y + 274, caption, 24, 600, C["sub"], "middle")
    return x + 28, y + 86, CW - 56, 150


def side_card(x, y, lines, caption):
    add(f'<rect x="{x}" y="{y}" width="{SIDE_W}" height="{CH}" rx="24" fill="{C["card"]}" '
        f'stroke="{C["cardStroke"]}" stroke-width="1.8" filter="url(#shadow)"/>')
    for i, s in enumerate(lines):
        text(x + SIDE_W / 2, y + 56 + i * 36, s, 30, 700, anchor="middle")
    text(x + SIDE_W / 2, y + 274, caption, 24, 600, C["sub"], "middle")


# ---------- illustrations ----------
def draw_build(px, py, pw, ph):
    accent = STEP["build"][0]
    x, y, w, h, nx, ny = px + 52, py + 58, 222, 72, 6, 3
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#meshFill)" stroke="{accent}" stroke-width="2.6"/>')
    dx, dy = w / nx, h / ny
    for i in range(1, nx):
        line(f"M{f(x + i * dx)} {y}v{h}", "#7E9CCB", 1.6)
    for j in range(1, ny):
        line(f"M{x} {f(y + j * dy)}h{w}", "#7E9CCB", 1.6)
    for i in range(nx):
        for j in range(ny):
            line(f"M{f(x + i * dx)} {f(y + j * dy)}l{f(dx)} {f(dy)}", "#7E9CCB", 1.3)
    # fixed boundary with hatching
    add(f'<rect x="{x - 12}" y="{y - 8}" width="10" height="{h + 16}" fill="{accent}"/>')
    for k in range(6):
        line(f"M{x - 12} {f(y - 2 + k * 15)}l-12 12", accent, 2.2)
    # boundary load
    for i in range(6):
        ax = x + 18 + i * (w - 36) / 5
        line(f"M{f(ax)} {y - 40}v24", "#D9822B", 3.4)
        add(f'<path d="M{f(ax - 7)} {y - 18} L{f(ax)} {y - 6} L{f(ax + 7)} {y - 18}Z" fill="#D9822B"/>')


def draw_run(px, py, pw, ph):
    tw, th, gx, gy = 82, 50, 14, 14
    x0 = px + (pw - (3 * tw + 2 * gx)) / 2
    y0 = py + (ph - (2 * th + gy)) / 2
    angles = (0, 35, 70, 110, 150, 200)
    for k in range(6):
        i, j = k % 3, k // 3
        x, y = x0 + i * (tw + gx), y0 + j * (th + gy)
        add(f'<rect x="{f(x)}" y="{f(y)}" width="{tw}" height="{th}" rx="8" fill="#FFFFFF" stroke="#8CC3AE" stroke-width="1.8"/>')
        add(f'<rect x="{f(x + 6)}" y="{f(y + 6)}" width="{tw - 12}" height="{th - 12}" rx="4" fill="url(#field{k})"/>')
    defs_extra.extend(
        f'<linearGradient id="field{k}" gradientTransform="rotate({a} .5 .5)">'
        f'<stop offset="0" stop-color="#4E78D0"/><stop offset=".5" stop-color="#8FD0BC"/>'
        f'<stop offset="1" stop-color="#F2A65A"/></linearGradient>' for k, a in enumerate(angles))


def draw_inspect(px, py, pw, ph):
    accent = STEP["inspect"][0]
    ox, oy, ax, ay = px + 34, py + ph - 22, pw - 62, ph - 40
    line(f"M{ox} {oy - ay}V{oy}H{ox + ax}", "#4A4763", 2.8)
    pts_a, pts_b = [], []
    for i in range(41):
        t = i / 40
        xx = ox + 12 + t * (ax - 20)
        v = 0.5 + 0.32 * math.sin(2 * math.pi * (t * 1.15 + 0.05)) * (1 - 0.25 * t)
        pts_a.append((xx, oy - 12 - v * (ay - 26)))
        pts_b.append((xx, oy - 12 - (v - 0.045 + 0.03 * t) * (ay - 26)))
    to_d = lambda pts: "M" + " L".join(f"{f(a)} {f(b)}" for a, b in pts)
    line(to_d(pts_a), accent, 4.2)
    line(to_d(pts_b), "#2F9C84", 3.4, 'stroke-dasharray="7 7"')
    cx, cy = pts_a[30]
    add(f'<circle cx="{f(cx)}" cy="{f(cy - 4)}" r="17" fill="#FFFFFF" stroke="{accent}" stroke-width="2.4"/>')
    line(f"M{f(cx - 8)} {f(cy - 4)} l5.5 6 l10 -12", "#2F7D6B", 3.6)


def draw_refine(px, py, pw, ph):
    accent = STEP["refine"][0]
    s = 92
    x, y = px + 24, py + (ph - s) / 2
    add(f'<rect x="{f(x)}" y="{f(y)}" width="{s}" height="{s}" fill="#F7DFC2" stroke="#B07A45" stroke-width="2.6"/>')
    for k in range(1, 4):
        line(f"M{f(x + k * s / 4)} {f(y)}v{s}", "#C29A72", 1.5)
        line(f"M{f(x)} {f(y + k * s / 4)}h{s}", "#C29A72", 1.5)
    # arrow
    line(f"M{f(x + s + 16)} {f(py + ph / 2)}h26", accent, 4)
    add(f'<path d="M{f(x + s + 40)} {f(py + ph / 2 - 9)} L{f(x + s + 54)} {f(py + ph / 2)} '
        f'L{f(x + s + 40)} {f(py + ph / 2 + 9)}Z" fill="{accent}"/>')
    # refined domain: notched shape with a finer mesh
    rx0, ry0, rw = x + s + 70, y, 120
    shape = (f"M{f(rx0)} {f(ry0)} H{f(rx0 + 28)} L{f(rx0 + 44)} {f(ry0 + 22)} H{f(rx0 + 76)} "
             f"L{f(rx0 + 92)} {f(ry0)} H{f(rx0 + rw)} V{f(ry0 + s)} H{f(rx0 + 92)} L{f(rx0 + 76)} {f(ry0 + s - 22)} "
             f"H{f(rx0 + 44)} L{f(rx0 + 28)} {f(ry0 + s)} H{f(rx0)} Z")
    defs_extra.append(f'<clipPath id="refined"><path d="{shape}"/></clipPath>')
    add(f'<path d="{shape}" fill="#F2BE8A"/>')
    add('<g clip-path="url(#refined)">')
    step = rw / 8
    for k in range(9):
        line(f"M{f(rx0 + k * step)} {f(ry0)}v{s}", "#B98256", 1.2)
    for k in range(7):
        line(f"M{f(rx0)} {f(ry0 + k * s / 6)}h{rw}", "#B98256", 1.2)
    for i in range(8):
        for j in range(6):
            line(f"M{f(rx0 + i * step)} {f(ry0 + j * s / 6)}l{f(step)} {f(s / 6)}", "#B98256", 1.0)
    add("</g>")
    add(f'<path d="{shape}" fill="none" stroke="#A8632C" stroke-width="2.6" stroke-linejoin="round"/>')


def draw_question(cx, cy):
    col = "#3F4B63"
    add(f'<path d="M{cx - 62} {cy - 44} h124 a12 12 0 0 1 12 12 v58 a12 12 0 0 1 -12 12 h-72 l-26 22 v-22 '
        f'h-26 a12 12 0 0 1 -12 -12 v-58 a12 12 0 0 1 12 -12z" fill="#FFF6E3" stroke="#C99A3A" stroke-width="3"/>')
    line(f"M{cx - 40} {cy - 16}h80M{cx - 40} {cy + 6}h52", "#C99A3A", 4)


def draw_findings(cx, cy):
    x, y = cx - 46, cy - 62
    add(f'<path d="M{x} {y} h66 l26 26 v98 h-92z" fill="#FFFFFF" stroke="#5E8F70" stroke-width="3"/>')
    add(f'<path d="M{x + 66} {y} v26 h26" fill="none" stroke="#5E8F70" stroke-width="3"/>')
    line(f"M{x + 16} {y + 30}h36M{x + 16} {y + 44}h52", "#8FB39C", 3)
    line(f"M{x + 16} {y + 108}v-44M{x + 16} {y + 108}h60", "#5E8F70", 2.6)
    line(f"M{x + 22} {y + 98} l14 -14 l12 6 l20 -24", "#2F7D6B", 3.6)


# ---------- assemble ----------
defs_extra = []
body_start = len(out)

# frame band for the loop
add(f'<rect x="{X0 - 40}" y="20" width="{2 * CW + GAP + 80}" height="{H - 40}" rx="30" fill="{C["band"]}"/>')
text(HUB[0], 66, "AGENT RESEARCH LOOP", 22, 700, C["ink"], "middle", 'letter-spacing="2"')

panels = {
    "build": step_card("build", 1, "Build model", "Geometry & physics"),
    "run": step_card("run", 2, "Run in COMSOL", "Trial → full study"),
    "inspect": step_card("inspect", 3, "Inspect results", "Compare & check"),
    "refine": step_card("refine", 4, "Refine model", "Adjust assumptions"),
}
draw_build(*panels["build"])
draw_run(*panels["run"])
draw_inspect(*panels["inspect"])
draw_refine(*panels["refine"])

side_card(IN_X, rows[0], ["Research", "question"], "Your goal")
draw_question(IN_X + SIDE_W / 2, rows[0] + 168)
side_card(OUT_X, rows[1], ["Findings"], "Plots & report")
draw_findings(OUT_X + SIDE_W / 2, rows[1] + 160)

# arrows: main flow in ink, return paths in amber
g = 7
top_mid, bot_mid = rows[0] + CH / 2, rows[1] + CH / 2
left_mid, right_mid = cols[0] + CW / 2, cols[1] + CW / 2
arrow(IN_X + SIDE_W + g, top_mid, cols[0] - g, top_mid)
arrow(cols[0] + CW + g, top_mid, cols[1] - g, top_mid)
arrow(right_mid - 34, rows[0] + CH + g, right_mid - 34, rows[1] - g)
arrow(right_mid + 34, rows[1] - g, right_mid + 34, rows[0] + CH + g, C["amber"], "arrowAmber")
text(right_mid + 58, HUB[1] + 9, "rerun", 25, 700, C["amberText"])
arrow(cols[1] - g, bot_mid, cols[0] + CW + g, bot_mid)
arrow(left_mid, rows[1] - g, left_mid, rows[0] + CH + g, C["amber"], "arrowAmber")
text(left_mid + 24, HUB[1] + 9, "iterate", 25, 700, C["amberText"])
arrow(cols[1] + CW + g, bot_mid, OUT_X - g, bot_mid)

# agent hub at the centre of the loop
hx, hy = HUB
add(f'<circle cx="{hx}" cy="{hy}" r="80" fill="{C["band"]}"/>')
add(f'<circle cx="{hx}" cy="{hy}" r="70" fill="url(#hubGrad)" filter="url(#hubShadow)"/>')
add(f'<circle cx="{hx}" cy="{hy}" r="70" fill="url(#sheen)"/>')
text(hx, hy - 4, "AI", 40, 700, "#FFFFFF", "middle")
text(hx, hy + 31, "Agent", 27, 650, "#F2F6FD", "middle")

body = out[body_start:]
defs = f"""<defs>
  <linearGradient id="hubGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['lead0']}"/><stop offset="1" stop-color="{C['lead1']}"/></linearGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="meshFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D3E3FB"/><stop offset="1" stop-color="#B3CCF0"/></linearGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#16203A" flood-opacity=".10"/></filter>
  <filter id="hubShadow" x="-40%" y="-40%" width="180%" height="190%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#22386A" flood-opacity=".35"/></filter>
  <marker id="arrow" viewBox="0 0 16 16" refX="13" refY="8" markerWidth="21" markerHeight="21" markerUnits="userSpaceOnUse" orient="auto"><path d="M1.5 1.5 L14.5 8 L1.5 14.5 Z" fill="{C['line']}"/></marker>
  <marker id="arrowAmber" viewBox="0 0 16 16" refX="13" refY="8" markerWidth="21" markerHeight="21" markerUnits="userSpaceOnUse" orient="auto"><path d="M1.5 1.5 L14.5 8 L1.5 14.5 Z" fill="{C['amber']}"/></marker>
  {''.join(defs_extra)}
</defs>"""
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'font-family="{FONT}" role="img" aria-labelledby="title desc">\n'
       '<title id="title">An agent-guided research loop in COMSOL</title>\n'
       '<desc id="desc">A research question enters a loop led by an AI agent: build a model, run it in COMSOL, '
       'inspect the results, and refine the model, then iterate. Inspection can also send cases back to rerun. '
       'Interpretable results leave the loop as plots and a report. The physical graphics are illustrative.</desc>\n'
       f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n{defs}\n' + "\n".join(body) + "\n</svg>\n")
args.output.write_text(svg, encoding="utf-8")
args.output.with_suffix(".html").write_text(
    '<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}svg{display:block}</style>' + svg,
    encoding="utf-8")
print(args.output)
