"""Build the README workflow illustration using only the Python standard library."""
from pathlib import Path
import argparse
import math
from xml.sax.saxutils import escape
cli=argparse.ArgumentParser(description=__doc__)
cli.add_argument("--layout",choices=("direct","grouped"),default="direct")
cli.add_argument("--refinement",choices=("shape","opening"),default="shape")
cli.add_argument("--output",type=Path,default=Path(__file__).resolve().parents[1]/"workflow.svg")
args=cli.parse_args()
OUT=args.output
p=[]
def add(s):p.append(s)
def text(x,y,s,size=30,weight=600,fill="#20333e",anchor="start"):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')
def card(x,y,w,h,fill,stroke):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
def path(d,stroke="#647784",width=4,fill="none",extra=""):
    add(f'<path d="{d}" stroke="{stroke}" stroke-width="{width}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640" role="img" aria-labelledby="title desc">')
add('<title id="title">An agent-guided research loop in COMSOL</title><desc id="desc">A research question enters model construction. The agent builds a model, runs a study, inspects the results, and refines the model before another calculation. Interpretable results lead to plots and findings. All physical graphics are illustrative.</desc>')
add('<defs>')
add('<linearGradient id="meshfill" x2="0" y2="1"><stop stop-color="#d5e6ff"/><stop offset="1" stop-color="#b7d2f5"/></linearGradient>')
add('<linearGradient id="field" x1="0" x2="1"><stop stop-color="#6d8fde"/><stop offset=".5" stop-color="#a2d4c5"/><stop offset="1" stop-color="#f3bc7d"/></linearGradient>')
add('</defs><rect width="1200" height="640" rx="20" fill="#ffffff"/>')
add('<g font-family="Arial,Helvetica,sans-serif">')
# The group identifies the agent's repeated work, without a robotic mascot.
# The optional neutral outline makes a grouped entry unambiguous.
if args.layout=="grouped":
 add('<rect x="235" y="74" width="690" height="538" rx="24" fill="#ffffff" stroke="#c7cfd5" stroke-width="2" stroke-dasharray="8 7"/>')
text(580,59,'Agent research loop',33,700,anchor='middle')
# Input, four steps, and one output branch.
input_y=88 if args.layout=="direct" else 228
card(18,input_y,182,222,'#fff8e6','#dabe76')
text(109,input_y+40,'Research',30,700,anchor='middle')
text(109,input_y+73,'question',30,700,anchor='middle')
path(f'M60 {input_y+104}h99v48H98l-17 16v-16H60z','#b3913e',3)
path(f'M76 {input_y+120}h66M76 {input_y+133}h43','#b3913e',3)
text(109,input_y+202,'Your goal',26,500,anchor='middle')
# Main step cards.
for x,y,fill,stroke in [(258,88,'#eaf2ff','#b8cbe6'),(603,88,'#e7f4ed','#b5d4c2'),(603,375,'#f0ecfa','#c8bde3'),(258,375,'#fff0e4','#e6c3a5')]:card(x,y,297,222,fill,stroke)
text(282,128,'Build model',32,700)
text(627,128,'Run in COMSOL',30,700)
text(627,415,'Inspect results',31,700)
text(282,415,'Refine model',31,700)
# Model: a meshed plate with boundary load arrows.
add('<path d="M298 169h203v85H298z" fill="url(#meshfill)" stroke="#5c83b3" stroke-width="2.5"/>')
for i in range(1,6):path(f'M{298+i*34} 169v85','#7b9fc8',1.6)
for y in [197,226]:path(f'M298 {y}h203','#7b9fc8',1.6)
for row in range(3):
 for c in range(6):
  x=298+c*34;y=169+row*28
  path(f'M{x} {y}l34 28','#7b9fc8',1.4)
path('M294 165v93','#426a9a',5)
for x in [322,365,408,451,494]:
 path(f'M{x} 149v14','#d28d58',3)
 add(f'<path d="m{x-4} 158 4 6 4-6" fill="none" stroke="#d28d58" stroke-width="2.5"/>')
text(406,290,'Geometry & physics',26,500,anchor='middle')
# Run: a group of different cases rather than a play button.
for row in range(2):
 for col in range(3):
  x=635+col*78;y=153+row*47
  add(f'<rect x="{x}" y="{y}" width="66" height="38" rx="7" fill="#fff" stroke="#9ec5af" stroke-width="1.6"/>')
  add(f'<rect x="{x+7}" y="{y+7}" width="52" height="24" rx="3" fill="url(#field)" opacity="{0.65+0.1*col}"/>')
# The field-map array represents repeated calculation cases.
text(751,290,'Trial → full study',27,500,anchor='middle')
# Inspection: two interpretable response curves on visible axes.
path('M638 544V451M638 544h225','#5a5671',2.5)
path('M651 526C677 522 689 481 716 477S758 528 789 504 833 467 854 475','#8f78b4',4)
path('M651 532C677 528 689 486 716 482S758 533 789 509 833 471 854 479','#54a89c',3,extra='stroke-dasharray="5 6"')
add('<circle cx="786" cy="505" r="16" fill="#fff" stroke="#b2a4ce" stroke-width="2"/>')
path('m779 505 5 5 10-12','#667d6d',3)
text(751,576,'Compare & check',27,500,anchor='middle')
# A visible geometry change carries the meaning without extra time labels.
# These generic domains are illustrative, independent of the paper example.
add('<rect x="280" y="451" width="85" height="88" fill="#f6dfc9" stroke="#af8059" stroke-width="2.6"/>')
for x in [301,322,343]:path(f'M{x} 451v88','#bc9776',1.5)
for y in [473,495,517]:path(f'M280 {y}h85','#bc9776',1.5)
if args.refinement=="shape":
 refined='M412 451H439L454 471H487L502 451H530V539H502L487 519H454L439 539H412Z'
else:
 refined='M412 451H530V539H412Z M489 495a18 18 0 1 0-36 0a18 18 0 1 0 36 0Z'
add(f'<path d="{refined}" fill="#f3c396" fill-rule="evenodd"/>')
add(f'<defs><clipPath id="refined-domain"><path d="{refined}" clip-rule="evenodd"/></clipPath></defs>')
add('<g clip-path="url(#refined-domain)">')
for x in [412,436,460,484,508,532]:path(f'M{x} 451v88','#ba865c',1.4)
for y in [451,473,495,517,539]:path(f'M412 {y}h118','#ba865c',1.4)
for row in range(4):
 for col in range(5):
  x=412+col*24;y=451+row*22
  path(f'M{x} {y}l24 22','#ba865c',1.2)
add('</g>')
path(refined,'#ad703e',2.8,extra='fill-rule="evenodd"')
# The short connector shares a centerline and overlaps the arrowhead base.
path('M378 495h15','#ad703e',3.5)
add('<path d="M402 495 391 489 391 501Z" fill="#ad703e"/>')
text(406,585,'Adjust assumptions',26,500,anchor='middle')
# Directional transitions: repeat through refinement, branch to interpretation.
def connector(points,color):
    # All points belong to the same arrow. The final segment defines its tip
    # and tangent; the shaft joins inside the head, avoiding marker offsets.
    tip=points[-1]; prev=points[-2]
    dx,dy=tip[0]-prev[0],tip[1]-prev[1]
    length=math.hypot(dx,dy); ux,uy=dx/length,dy/length
    head=14.0; half=7.0
    base=(tip[0]-head*ux,tip[1]-head*uy)
    end=(base[0]+1.5*ux,base[1]+1.5*uy)
    route=points[:-1]+[end]
    d='M'+' L'.join(f'{x:g} {y:g}' for x,y in route)
    path(d,color,5)
    left=(base[0]-half*uy,base[1]+half*ux)
    right=(base[0]+half*uy,base[1]-half*ux)
    add(f'<path d="M{tip[0]:g} {tip[1]:g} L{left[0]:g} {left[1]:g} L{right[0]:g} {right[1]:g}z" fill="{color}"/>')
if args.layout=="direct":
 connector([(210,199),(246,199)],'#7396bf')
else:
 connector([(210,339),(250,339)],'#7396bf')
connector([(565,199),(591,199)],'#7396bf')
connector([(751,320),(751,363)],'#65a78c')
connector([(592,486),(565,486)],'#9682b7')
connector([(406,365),(406,322)],'#cd9568')
text(427,348,'iterate',26,600,fill='#a5714d')
# The outcome is a separate branch, rather than another forced loop stage.
card(984,375,197,222,'#eef5ee','#bdd2bd')
text(1082,415,'Findings',31,700,anchor='middle')
add('<path d="M1037 449h61l23 22v75h-84z" fill="#fff" stroke="#85a68b" stroke-width="2.5"/><path d="M1098 449v23h23" fill="none" stroke="#85a68b" stroke-width="2.5"/>')
path('M1050 489h37M1050 500h53','#8caa92',2.5)
path('M1050 532v-22m0 22h53m-45-6 14-11 12 5 13-12','#619475',2.5)
text(1082,576,'Plots & report',26,500,anchor='middle')
connector([(910,486),(972,486)],'#718b7c')
# The findings branch is already labeled by its destination.
add('</g></svg>')
OUT.write_text('\n'.join(p)+'\n',encoding='utf-8')
print(OUT)
