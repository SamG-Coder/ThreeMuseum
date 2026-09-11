"""Generate original measured SVG plans and a vector PDF design booklet.
Requires Python: reportlab, svglib. Not needed to run the museum.
Input: public/architecture.json, emitted by npm run plans.
"""
from pathlib import Path
import json, html, csv, math, textwrap
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'public/architecture.json').read_text())
OUT=ROOT/'public/plans';OUT.mkdir(parents=True,exist_ok=True)
INK='#223b36';PAPER='#f4f0e5';GOLD='#af7f45';MUTED='#6d796f'

def esc(s):return html.escape(str(s))
def rect(x,y,w,h,fill,extra=''):return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" {extra}/>'
def text(x,y,s,size=14,fill=INK,extra=''):return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" {extra}>{esc(s)}</text>'
def line(x,y,x2,y2,color=INK,width=1,extra=''):return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" {extra}/>'
def svg_start(w,h):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Arial, sans-serif">',rect(0,0,w,h,PAPER)]

def floor_plan(ceiling=False):
 a=svg_start(1000,1250);S=9.5;X=lambda x:500+x*S;Z=lambda z:620+z*S
 a+=[text(60,56,'THREE MUSEUM',29,extra='font-weight="700"'),text(60,86,'P02  /  REFLECTED CEILING CONCEPT' if ceiling else 'P01  /  GROUND FLOOR + OVERLOOK',15,GOLD),text(60,111,'Original design. All dimensions in metres. Not an as-built Melbourne Museum plan.',12,MUTED)]
 a+=[rect(X(-42),Z(29),84*S,18*S,'#e4e1d5')]
 for r in D['rooms']:
  x1,x2,z1,z2=r['bounds'];a.append(rect(X(x1),Z(z1),(x2-x1)*S,(z2-z1)*S,r['color'],'fill-opacity=".23"'))
 if ceiling:
  for p in D['pieces']:
   if p.get('section')!='roof' or p['kind']!='box':continue
   x,y,z=p['position'];w,h,d=p['size'];color='#b1c8c2' if p['material']=='skylight' else '#877158' if p['material']=='oakDark' else '#334541'
   a.append(rect(X(x-w/2),Z(z-d/2),w*S,d*S,color,'fill-opacity=".5"'))
 else:
  # Raised deck is indicated in outline; it does not falsely occlude the ground floor.
  x1,x2,z1,z2=D['deck']['bounds'];a.append(rect(X(x1),Z(z1),(x2-x1)*S,(z2-z1)*S,'#d3c1a2','fill-opacity=".65" stroke="#9e7845" stroke-dasharray="5 4"'))
  ra=D['ramp'];a.append(rect(X(ra['x1']),Z(-36),(ra['x2']-ra['x1'])*S,42*S,'#d3c1a2'))
  for seg in ra['segments']:
   a.append(line(X(ra['x1']),Z(seg['z2']),X(ra['x2']),Z(seg['z2']),GOLD,.7))
  for b in D['colliders']:
   if b['id'] in ('site-boundary','ramp-side') or b['min'][1]>1.8 or b['max'][1]<=.06:continue
   x1,y1,z1=b['min'];x2,y2,z2=b['max'];a.append(rect(X(x1),Z(z1),max(.8,(x2-x1)*S),max(.8,(z2-z1)*S),'#52645b','fill-opacity=".65"'))
  route=' '.join(f'{X(x):.1f},{Z(z):.1f}' for x,z in D['visitorRoute'])
  a.append(f'<polyline points="{route}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="7 5" stroke-linejoin="round"/>')
  for e in D['exhibits']:
   x,y,z=e['position'];w,h,d=e['envelope'];a.append(rect(X(x-w/2),Z(z-d/2),w*S,d*S,'none',f'stroke="{GOLD}" stroke-width="1.1" stroke-dasharray="3 2"'))
   # IDs on small paper labels remain readable against the architectural footprints.
   a.append(rect(X(x)-15,Z(z)-7,30,14,PAPER,'rx="2"'))
   a.append(text(X(x),Z(z)+3,e['id'],10,INK,'text-anchor="middle" font-weight="700"'))
  a.append(text(X(-35.8),Z(-13),'RAMP  /  1:15',10,INK,f'text-anchor="middle" transform="rotate(-90 {X(-35.8)} {Z(-13)})"'))
  a.append(text(X(-24),Z(-40.1),'OVERLOOK  +2.40',10,INK,'text-anchor="middle" font-weight="700"'))
 # Architectural perimeter and selected room identifiers.
 for p in D['pieces']:
  if p.get('section')!='wall' or not p['id'].startswith('wall-'):continue
  x,y,z=p['position'];w,h,d=p['size'];a.append(rect(X(x-w/2),Z(z-d/2),max(1.3,w*S),max(1.3,d*S),INK))
 names={'arrival':('ARRIVAL HALL',0,24),'dinosaurs':('01  DEEP TIME HALL',-19,-34.5),'court':('LIGHT COURT',0,-31),'diversity':('02  DIVERSITY',13,-5.7),'habitats':('03  HABITATS',29,-5.7),'anatomy':('04  SMALL WORLDS',12.5,-9),'arachnids':('05  EIGHT-LEGGED',29,-9),'feature':('06  LAST GIANTS',12.5,-25),'theatre':('07  BIG QUESTIONS',29.5,-25),'learning':('08  DISCOVERY',29,15),'rest':('VISITOR LOUNGE',-29,15)}
 for r in D['rooms']:
  label,x,z=names[r['id']]
  if ceiling: x=(r['bounds'][0]+r['bounds'][1])/2;z=(r['bounds'][2]+r['bounds'][3])/2;label=f'{r["height"]:.1f} m'
  if r['id']=='court' and not ceiling:
   a.append(text(X(x),Z(z),label,10,INK,f'text-anchor="middle" transform="rotate(-90 {X(x)} {Z(z)})"'))
  else:
   a.append(text(X(x),Z(z),label,11 if not ceiling else 17,INK,'text-anchor="middle" font-weight="700"'))
 a+=[line(X(-38),188,X(38),188,MUTED),line(X(-38),180,X(-38),203,MUTED),line(X(38),180,X(38),203,MUTED),text(500,180,'76.00 m',13,MUTED,'text-anchor="middle"')]
 a+=[line(107,Z(-43),107,Z(29),MUTED),line(100,Z(-43),120,Z(-43),MUTED),line(100,Z(29),120,Z(29),MUTED),text(96,(Z(-43)+Z(29))/2,'72.00 m',13,MUTED,f'text-anchor="middle" transform="rotate(-90 96 {(Z(-43)+Z(29))/2})"')]
 a+=[text(923,210,'N',16,INK,'text-anchor="middle"'),line(923,262,923,225,INK,2),f'<path d="M 917 234 L 923 222 L 929 234" fill="none" stroke="{INK}" stroke-width="2"/>']
 a.append(text(500,Z(37),'MUSEUM FORECOURT',17,INK,'text-anchor="middle" letter-spacing="2"'))
 a.append(text(500,Z(40),'8 m entrance opening  /  canopy above',12,MUTED,'text-anchor="middle"'))
 a.append(line(60,1110,940,1110,'#d1ccbd',1))
 if ceiling:
  a+=[rect(60,1136,18,12,'#b1c8c2'),text(88,1147,'Glazed northlight and central roofs',14),rect(510,1136,18,12,'#877158'),text(538,1147,'Timber acoustic fin zones',14),text(60,1180,'Ceiling heights are design parameters, not surveyed dimensions.',13,MUTED)]
 else:
  a+=[line(60,1140,95,1140,GOLD,3,'stroke-dasharray="6 4"'),text(106,1145,'Suggested visitor loop',14),rect(355,1133,22,14,'none',f'stroke="{GOLD}" stroke-dasharray="3 2"'),text(390,1145,'Future model envelope',14),rect(675,1133,22,14,'#d3c1a2'),text(710,1145,'Raised circulation',14),text(60,1178,'D = dinosaurs   B = bugs   F = feature   L = learning   C = court',13,MUTED)]
 for i in range(2):a.append(rect(60+i*5*S,1203,5*S,7,INK if i%2==0 else '#b6b6a8'))
 a += [text(60,1226,'0',10),text(60+5*S,1226,'5',10),text(60+10*S,1226,'10 m',10),text(940,1226,'Use written dimensions; viewer/print size changes scale.',11,MUTED,'text-anchor="end"'),'</svg>']
 return ''.join(a)

(OUT/'ground-floor.svg').write_text(floor_plan(),encoding='utf-8')
(OUT/'ceiling-plan.svg').write_text(floor_plan(True),encoding='utf-8')
a=svg_start(1000,550);a+=[text(60,55,'THE LONG VIEW',29,extra='font-weight="700"'),text(60,85,'P03  /  WEST RAMP LONGITUDINAL SECTION',15,GOLD),text(60,111,'Same horizontal and vertical scale. Railings shown schematically.',12,MUTED)]
S=17;X=lambda z:110+(6-z)*S;Y=lambda y:405-y*S
# Northlight datum and ground establish truthful relative scale.
a+=[rect(90,Y(11.8),850,5,'#617c73'),text(940,Y(11.8)-10,'Hall roof +11.80 m',13,MUTED,'text-anchor="end"'),line(90,Y(0),940,Y(0),INK,2),text(95,Y(0)+23,'GROUND  +0.00',12)]
for seg in D['ramp']['segments']:
 x1,x2,y1,y2=X(seg['z1']),X(seg['z2']),Y(seg['y1']),Y(seg['y2']);a.append(f'<polygon points="{x1},{y1} {x2},{y2} {x2},{y2+4} {x1},{y1+4}" fill="{GOLD}"/>');a.append(line(x1,Y(seg['y1']+1.1),x2,Y(seg['y2']+1.1),INK,1.3))
 for j in range(math.ceil((seg['z1']-seg['z2'])/1.5)):
  t=j/max(1,math.ceil((seg['z1']-seg['z2'])/1.5));z=seg['z1']+(seg['z2']-seg['z1'])*t;y=seg['y1']+(seg['y2']-seg['y1'])*t;a.append(line(X(z),Y(y),X(z),Y(y+1.1),INK,.7))
 label='12 m / 1:15' if seg['y2']>seg['y1'] else '3 m'
 a.append(text((x1+x2)/2,450,label,12,INK,'text-anchor="middle"'))
a+=[rect(X(-36),Y(2.4),6.5*S,.26*S,GOLD),text(930,Y(2.4)-12,'OVERLOOK +2.40 m',13,INK,'text-anchor="end"'),text(60,496,'Three 12 m slopes + two 3 m landings = 42 m run. Ramp width at rail centrelines: 3.30 m.',14),text(60,522,'Virtual-world dimensions only. No structural, fire, disability-access or building-code certification is implied.',11,MUTED),'</svg>']
(OUT/'ramp-section.svg').write_text(''.join(a),encoding='utf-8')
with (ROOT/'docs/EXHIBIT_SCHEDULE.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['ID','Gallery','Subject','Fixture','X_m','Y_m','Z_m','Width_m','Height_m','Depth_m','Model_path','Brief'])
 for e in D['exhibits']:w.writerow([e['id'],e['room'],e['subject'],e['kind'],*e['position'],*e['envelope'],'models/'+e['id']+'.glb',e['brief']])

# Standalone, no-engine-required design browser.
roomrows=''.join(f'<tr><td>{esc(r["name"])}</td><td>{r["bounds"][1]-r["bounds"][0]} × {r["bounds"][3]-r["bounds"][2]} m</td><td>{r["height"]} m</td></tr>' for r in D['rooms'])
exhibits=''.join(f'<article><span>{e["id"]} · {esc(e["kind"].upper())}</span><h3>{esc(e["subject"])}</h3><b>{" × ".join(map(str,e["envelope"]))} m</b><p>{esc(e["brief"])}</p></article>' for e in D['exhibits'])
sources=''.join(f'<li>[{s["id"]}] <a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["title"])}</a></li>' for s in D['sources'])
(OUT/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ThreeMuseum | Design atlas</title><style>*{{box-sizing:border-box}}body{{margin:0;background:{PAPER};color:{INK};font:16px/1.6 system-ui,sans-serif}}header{{background:{INK};color:#f3eddb;padding:64px max(6vw,24px)}}header p{{max-width:750px;color:#c5cdbd}}h1{{font:normal clamp(44px,7vw,88px)/1.05 Georgia,serif;margin:18px 0}}.eyebrow{{letter-spacing:3px;font-size:12px;text-transform:uppercase}}main{{max-width:1200px;margin:auto;padding:40px 24px}}h2{{font:normal 36px Georgia,serif;margin:50px 0 18px}}a{{color:inherit}}nav{{display:flex;gap:24px;flex-wrap:wrap}}nav a{{border-bottom:1px solid #b29263;text-decoration:none}}.plans{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}img{{width:100%;display:block;border:1px solid #d8d0bf}}.wide{{grid-column:1/-1}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}article{{background:#faf7ef;border:1px solid #ddd6c7;padding:24px}}article span{{font-size:12px;letter-spacing:1px;color:#926b3b}}article h3{{font:normal 24px/1.15 Georgia,serif;margin:14px 0}}article p{{font-size:14px;color:#5d6b60}}article b{{font-size:13px}}table{{width:100%;border-collapse:collapse}}td,th{{text-align:left;padding:13px;border-bottom:1px solid #d8d0bf}}.note{{padding:24px;border-left:4px solid #ae8951;background:#e9e6da}}footer{{padding:40px 24px;max-width:1200px;margin:auto;font-size:13px;color:#5d6b60}}@media(max-width:760px){{.cards,.plans{{grid-template-columns:1fr}}header{{padding:40px 24px}}}}@media print{{header{{padding:24px}}.cards{{grid-template-columns:1fr 1fr}}article{{break-inside:avoid}}}}</style><header><div class="eyebrow">THREE MUSEUM / DESIGN ATLAS 01</div><h1>Small worlds.<br>Deep time.</h1><p>An original museum building inspired by Melbourne Museum's natural-history galleries. Architecture, visitor circulation and exhibit allowances only. No specimen models.</p><nav><a href="../../">Open the walkable world ↗</a><a href="ThreeMuseum_Design_Plan.pdf">Design booklet PDF ↓</a><a href="#schedule">30 exhibit positions</a></nav></header><main><p class="note"><b>76 × 72 m footprint · 11 connected spaces · 30 Blender-ready origins.</b><br>All dimensions are original design choices, not measurements of the real Melbourne Museum. The plans work without Three.js or an internet connection.</p><h2>The measured plan</h2><div class="plans"><a href="ground-floor.svg"><img src="ground-floor.svg" alt="Original measured ground floor plan showing dinosaur hall, bug galleries and connecting walks"></a><a href="ceiling-plan.svg"><img src="ceiling-plan.svg" alt="Ceiling concept with gallery heights and skylights"></a><a class="wide" href="ramp-section.svg"><img src="ramp-section.svg" alt="Measured longitudinal ramp section"></a></div><h2>The rooms</h2><table><thead><tr><th>Space</th><th>Design footprint</th><th>Ceiling datum</th></tr></thead><tbody>{roomrows}</tbody></table><h2 id="schedule">Your Blender exhibit schedule</h2><p>Dimensions are width × height × depth. Each origin is bottom-centred. These are installation allowances, not claims about animal size.</p><div class="cards">{exhibits}</div><h2>Research references</h2><p>Primary sources reviewed 11 September 2026. Their imagery, plans, specimens and exhibition text are not redistributed here.</p><ol>{sources}</ol></main><footer>Independent project. Not affiliated with Museums Victoria. Concept architecture for a virtual world; not a construction, husbandry, conservation or accessibility certification package.</footer></html>''',encoding='utf-8')

# Vector PDF: fixed, measured plans plus consistently flowed text.
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
W,H=A4
PDF=OUT/'ThreeMuseum_Design_Plan.pdf';c=canvas.Canvas(str(PDF),pagesize=A4)
c.setTitle('ThreeMuseum | Design and Blender Handoff');c.setAuthor('ThreeMuseum project')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10.3,leading=15,textColor=HexColor(INK),spaceAfter=7)
small=ParagraphStyle('small',parent=style,fontSize=8.5,leading=12)
number=0

def para(s,x,y,w,kind=style):
 p=Paragraph(s,kind);_,h=p.wrap(w,H);p.drawOn(c,x,y-h);return y-h-8

def page(title,tag):
 global number
 number+=1;c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(HexColor(GOLD));c.setFont('Helvetica-Bold',8);c.drawString(42,H-38,'THREE MUSEUM  /  ARCHITECTURAL EDITION')
 c.setFillColor(HexColor(INK));c.setFont('Times-Roman',29);c.drawString(42,H-78,title)
 c.setFillColor(HexColor(MUTED));c.setFont('Helvetica',9);c.drawString(43,H-99,tag)
 c.setStrokeColor(HexColor('#ccc5b6'));c.line(42,42,W-42,42);c.setFont('Helvetica',8);c.drawString(42,27,'ORIGINAL DESIGN  /  NOT AN AS-BUILT SURVEY');c.drawRightString(W-42,27,f'{number:02d}')
 return H-126

def head(s,x,y):
 c.setFillColor(HexColor(INK));c.setFont('Helvetica-Bold',12);c.drawString(x,y,s);return y-14

def table(rows,widths,x,y,fontsize=8.3):
 ts=ParagraphStyle('cell',parent=small,fontSize=fontsize,leading=fontsize+3)
 vals=[[Paragraph(esc(v),ts) for v in row] for row in rows]
 t=Table(vals,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#ded9c9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,HexColor('#d4cebd')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
 _,h=t.wrap(sum(widths),H);t.drawOn(c,x,y-h);return y-h-14

def diagram(filename,x,y,w,maxh=None):
 drawing=svg2rlg(str(OUT/filename));scale=w/drawing.width
 if maxh:scale=min(scale,maxh/drawing.height)
 drawing.scale(scale,scale);height=drawing.height*scale;renderPDF.draw(drawing,c,x,y-height);return y-height-10

def finish():c.showPage()

# 01
number+=1;c.setFillColor(HexColor(INK));c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(HexColor('#c6ad7e'));c.setFont('Helvetica-Bold',10);c.drawString(46,H-60,'THREE MUSEUM / DESIGN ATLAS 01')
c.setFillColor(HexColor(PAPER));c.setFont('Times-Roman',53);c.drawString(44,H-151,'Small worlds.');c.drawString(44,H-207,'Deep time.')
pale=ParagraphStyle('pale',parent=style,textColor=HexColor('#d5dbce'),fontSize=12,leading=19)
y=para('A walkable natural-history museum.<br/>A complete architectural shell.<br/>A place for your Blender exhibits.',46,H-244,W-92,pale)
c.setStrokeColor(HexColor('#708176'));c.line(46,440,W-46,440)
for i,(big,label) in enumerate([('76 × 72','metre footprint'),('11','connected spaces'),('30','exhibit origins')]):
 x=46+i*174;c.setFillColor(HexColor(PAPER));c.setFont('Times-Roman',30);c.drawString(x,391,big);c.setFont('Helvetica',9);c.setFillColor(HexColor('#c6ad7e'));c.drawString(x,369,label.upper())
y=para('<b>Architectural edition / no specimen models</b><br/>Dinosaur plinths, insect cabinets, empty habitats, a roof-lit connecting court, visitor controls, measured plans and a Blender handoff. The building is original; Melbourne Museum provides the research reference, not an exact floor plan.',46,318,W-92,pale)
para('Research reviewed 11 September 2026.<br/>Independent project; not affiliated with Museums Victoria.<br/>Virtual-world concept, not a construction or accessibility certification.',46,154,W-92,ParagraphStyle('foot',parent=pale,fontSize=9,leading=14))
finish()
# 02
y=page('Research into spatial decisions','What the source establishes; what ThreeMuseum deliberately changes.')
research=[('S1 / Bugs Alive!','The official gallery combines pinned collections, living enclosures, enlarged anatomy and a theatre.','Separate the bug wing into diversity, habitats, anatomy and arachnids. Use hollow cabinets, not rooms full of generic cubes.'),('S2-S3 / Dinosaur Walk','The museum describes visitors moving around and beneath mounted skeletons, including a long-necked Mamenchisaurus.','Build a tall hall, a split-support centrepiece bay, comparison tables and a raised long-view position. Do not imitate skeletons with placeholder geometry.'),('S4 / Triceratops','Melbourne has a separate immersive Triceratops exhibition.','Create Last Giants as a distinct, quieter feature room with a walk-around mount allowance. Do not reproduce Horridus.'),('S5 / Official visitor map','The Science and Life galleries connect with the museum’s broader circulation and Forest Gallery.','Group the two subject areas beside a legible connecting court. The footprint and room dimensions in this atlas are invented design parameters.'),('S6 / Denton Corker Marshall','The architect describes a campus of elements rather than a single monumental object.','Use distinct ceiling heights and volumes: one tall hall, a bright circulation spine and smaller galleries.'),('S7 / Accessibility','The museum documents sensory supports and access planning for visitors.','Provide no head bob or compulsory sound, a lower eye-height option, keyboard look, room-map shortcuts and a quiet theatre.')]
for title,fact,response in research:
 y=head(title,42,y);y=para('<b>Reference:</b> '+fact,42,y,W-84);y=para('<b>Design response:</b> '+response,42,y,W-84);y-=9
finish()
# 03
y=page('The whole museum','P01 / Ground floor, raised overlook and optional visitor loop.')
y=diagram('ground-floor.svg',42,y,W-84,620)
para('The dashed route was checked against the collision geometry. It is optional: visitors may choose a short bug-only or dinosaur-only visit and use the map to change galleries.',42,y,W-84,small)
finish()
# 04
y=page('Height, daylight and the long view','P02-P03 / A varied section without stairs on the main route.')
y=diagram('ramp-section.svg',42,y,W-84)
left=42;right=323
z=y-6
z=head('Room-specific atmosphere',left,z)
z=para('Deep Time Hall: 11.8 m roof datum.<br/>Last Giants: 8.0 m.<br/>Bug rooms: 5.6 m.<br/>Light Court: 10.0 m.<br/>Arrival hall: 9.0 m.',left,z,250)
z=para('Three 12 m sloping runs rise 0.8 m each. Two 3 m landings interrupt the ascent. The ramp is 3.3 m wide; the overlook is at +2.4 m, with a 1.1 m guardrail datum.',left,z,250)
z=para('These are game-space design choices. No claim is made that the ramp, glazing, guardrails or exits satisfy a particular building regulation.',left,z,250,small)
diagram('ceiling-plan.svg',right,y-5,230,330)
finish()
# 05
y=page('A building organised for visiting','Room footprints include partition allowances; they are not net lettable areas.')
rows=[['SPACE','DESIGN FOOTPRINT','GROSS AREA','ROOF']]
for r in D['rooms']:
 w=r['bounds'][1]-r['bounds'][0];d=r['bounds'][3]-r['bounds'][2];rows.append([r['name'],f'{w} × {d} m',f'{w*d:,} m²',f'{r["height"]} m'])
y=table(rows,[204,114,104,89],42,y)
y=head('Three useful routes',42,y-5)
y=para('<b>Short visit:</b> Arrival → Diversity → Living Habitats → Gallery Street → Arrival. <b>Deep time visit:</b> Arrival → Deep Time Hall → ramp → overlook → return ramp. <b>Long loop:</b> Hall → Light Court → Last Giants → Theatre → arachnid and anatomy rooms → Diversity → Arrival.',42,y,W-84)
y=para('The 76 × 72 m footprint is 5,472 m². The room rectangles account for 5,328 m²; the remaining 144 m² is the side portion of Gallery Street. The overlook and ramp are additional raised circulation within the footprint. These figures are derived from the model, not from Melbourne Museum.',42,y,W-84,small)
finish()
# 06
y=page('Deep Time Hall','Nine mounting and interpretation positions. All are intentionally empty.')
y=para('The centrepiece is D01, a 28 m-long design allowance with two separate support islands. Its 7 m cross-passage remains physically open. A final model must keep that passage clear above 2.8 m and must not allow its neck, tail or supports to intrude into the adjacent walk. The 28 m envelope is not a claimed specimen measurement.',42,y,W-84)
rows=[['ID / SUBJECT','FIXTURE','W × H × D (m)']]
for e in D['exhibits']:
 if e['id'].startswith('D'):rows.append([e['id']+' / '+e['subject'],e['kind'],' × '.join(map(str,e['envelope']))])
y=table(rows,[266,98,147],42,y)
y=para('D08 is suspended; its origin is 7 m above ground. D09 sits on the overlook, with its specimen origin at +3.28 m. Distinguish pterosaurs and later megafauna from dinosaurs in the final interpretation. Scientific labels, species-specific claims and mount authenticity still require review. [S2-S3]',42,y,W-84)
finish()
# 07
y=page('The bug galleries','Sixteen future exhibits, organised by the questions visitors ask.')
rows=[['ID / SUBJECT','FIXTURE','W × H × D (m)']]
for e in D['exhibits']:
 if e['id'].startswith('B'):rows.append([e['id']+' / '+e['subject'],e['kind'],' × '.join(map(str,e['envelope']))])
y=table(rows,[266,98,147],42,y,8.2)
y=para('The themes draw on Bugs Alive!, but the rooms and fixture dimensions are new. Habitat cases contain no animals, branches, water or substrate dressing. The tarantula case is a presentation allowance, not a quarantine facility. Microscope, mouthpart and lifecycle models remain a Blender task. [S1]',42,y,W-84,small)
finish()
# 08
y=page('The supporting spaces','Feature gallery, learning studio, light court and restrained materials.')
rows=[['ID / SUBJECT','FIXTURE','W × H × D (m)']]
for e in D['exhibits']:
 if e['id'][0] in 'FLC':rows.append([e['id']+' / '+e['subject'],e['kind'],' × '.join(map(str,e['envelope']))])
y=table(rows,[266,98,147],42,y)
y=head('Material and lighting direction',42,y)
for name,desc in [('Limestone and terrazzo','Quiet, low-gloss bases and circulation floors. Keep fine detail in the texture rather than oversized bump patterns.'),('Oak and dark bronze','Warmer dinosaur flooring, acoustic ceiling fins, handrails, light tracks and cabinet framing.'),('Glazing','A lightweight tinted-glass approximation for the baseline web scene. No ray-traced or physically accurate transmission claim.'),('Daylight and gallery light','Roof-lit arrival and court, a long dinosaur northlight, warm case lamps and a fixed pool of four local fill lights.'),('Lighting restraint','No heavy fog, bloom, flashing projections or artificial lens dirt. Screen and planting infrastructure are present, but films and plants are absent.')]:
 y=para('<b>'+name+':</b> '+desc,42,y,W-84)
finish()
# 09
y=page('Blender to the exhibit bay','One coordinate system, explicit origins and no automatic placement guesswork.')
steps=[('01 / Build the reference','Run blender/build_shell.py in Blender. It reconstructs the architectural geometry from public/architecture.json, creates named origins and wire envelopes, and leaves the roof hidden. Save the resulting scene as your own .blend file.'),('02 / Author the content','Put static world-space specimen geometry in MODEL_D01, MODEL_B05, and so on. Leave the building, display case, labels and wire envelope out of the exhibit collection. All dimensions are metres.'),('03 / Export','For static models in the reference scene, set EXHIBIT_ID in export_static_exhibit.py and run it. For animated assets, author/export a self-contained GLB in local coordinates with a bottom-centred origin; see BLENDER_HANDOFF.md.'),('04 / Preview and validate','Press B in the museum, choose a bay, and open the GLB. Set offset, rotation and uniform scale. The fit button is a convenience: it changes presentation size and does not certify scientific scale.'),('05 / Persist the installation','Copy the GLB to public/models, export the manifest from the installation panel and replace public/exhibits.json. Browser previews cannot silently save files into the project directory.')]
for title,body_ in steps:y=head(title,42,y);y=para(body_,42,y,W-84);y-=12
yp=y-5;y=head('Coordinate contract',42,yp)
y=para('<b>Three.js:</b> X east, Y up, north is -Z. <b>Blender:</b> (x, y, z) = (Three X, -Three Z, Three Y). A slot position is the bottom centre of the exhibit. A GLB scale of 1 means one metre stays one metre. Offsets use metres; UI rotations use degrees.',42,y,W-84)
y=para('Imported GLBs do not create physics colliders. Keep them inside their display envelopes and add explicit solids to architecture.js when an exhibit truly needs additional collision. Standard GLBs with embedded textures are supported; Draco/KTX2 decoder wiring is not included.',42,y,W-84,small)
finish()
# 10
y=page('What this build does - and does not','An architectural starting point with explicit validation boundaries.')
y=head('Implemented',42,y)
y=para('Procedural museum geometry; 30 empty display allowances; roof-off inspection; first-person walking and touch input; wall/case collision with displacement substeps; continuous ramp support; map destinations; readable exhibit briefs; GLB preview and manifest export; editable source; static-server and Pages deployment scripts.',42,y,W-84)
y=head('Checked in this delivery environment',42,y-8)
y=para('22 dependency-free geometry and navigation tests pass. They cover room spawns, front doors, the full drawn visitor loop, display collisions, high-displacement wall blocking, ramp ascent/descent, deck guardrails and safe reading positions. JavaScript and Blender-script syntax checks are separate from runtime rendering.',42,y,W-84)
y=head('Not verified here',42,y-8)
y=para('The environment could not retrieve the Three.js runtime, so live WebGL rendering, shader compilation, visual lighting quality and in-browser GLB installation were not exercised. Blender was not available, so the reference/export scripts were syntax-checked but not executed inside Blender. These are real remaining checks, not claimed passes.',42,y,W-84)
y=head('Deliberately outside scope',42,y-8)
y=para('No dinosaur, insect, arachnid, fossil, plant, microscope or habitat-dressing models. No crowds, film content, soundscape, complete scientific labels, collection-management backend, real animal housing, construction documentation or claim of legal accessibility compliance. No exact replica of Melbourne Museum or its proprietary specimens.',42,y,W-84)
y=head('Local acceptance pass',42,y-8)
y=para('Install dependencies, start the server and check every room at visitor eye height. Walk the ramp both ways, inspect the roof-off plan, preview a small test GLB, reload its exported manifest, and test touch controls on the intended device. Recheck every circulation route after adding large models. Use docs/TEST_REPORT.md as the starting checklist.',42,y,W-84)
finish()
# 11
y=page('Primary research sources','Reviewed 11 September 2026. References inform themes, not surveyed dimensions.')
for s in D['sources']:
 y=head('['+s['id']+'] '+s['title'].split(' — ')[0],42,y)
 y=para(esc(s['title']),42,y,W-84)
 y=para('<link href="'+esc(s['url'])+'" color="#805c31">'+esc(s['url'])+'</link>',42,y,W-84,small);y-=13
para('The official visitor map was inspected as a spatial reference. Source imagery, source maps, exhibit text and specimen assets are not redistributed. All plans in this booklet are generated from ThreeMuseum’s own architecture records.',42,y-4,W-84,small)
finish();c.save()
print('Created SVG plans, standalone atlas, exhibit CSV and '+str(PDF))
