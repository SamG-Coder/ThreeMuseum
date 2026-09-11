"""Author original interpretive specimens via Blender MCP.

All generated collections contain models only, never shell display furniture.
Specimens are detailed interpretive reconstructions, not digitised vouchers.
"""
import bpy
import sys
import math
import json
import runpy
import importlib
from pathlib import Path
from mathutils import Vector,Matrix
P=Path('D:/ThreeMuseum')
sys.path.insert(0,str(P/'blender'))
import specimen_geometry as sg
importlib.reload(sg)
from specimen_geometry import *
DATA=json.loads((P/'public/architecture.json').read_text())
ENTRIES={e['id']:e for e in DATA['exhibits']}

def place(m,fn,p=(0,0,0),s=1,rot=None,**kwargs):
    old=m.scope(p,s,rot);fn(m,**kwargs);m.restore(old)

def wall(south=False):
    return Matrix.Rotation(-PI/2 if south else PI/2,3,'X')@(Matrix.Rotation(PI,3,'Z') if south else Matrix.Identity(3))

def build(id):
    m=Model(id)
    if id=='B01':
        for j in range(2):
            for i in range(4):place(m,butterfly,(-1.05+i*.7,0,.43+j*.82),.43,wall(True),color=['blue','orange','cream','green'][(i+j)%4],swallow=i%2==1)
    elif id=='B02':
        for j in range(2):
            for i in range(7):place(m,beetle,(-2.20+i*.73,0,.40+j*.83),.20,wall(True),kind=['scarab','stag','longhorn'][i%3],color=['green','blue','gold'][i%3])
    elif id=='B03':
        place(m,beetle,(-.75,0,.03),.48,kind='stag',color='gold')
        place(m,beetle,(.67,0,.03),.48,kind='longhorn',color='blue')
    elif id=='B04':
        place(m,beetle,(-.92,0,.02),.27,color='green')
        place(m,butterfly,(0,0,.03),.52,color='orange')
        place(m,ant,(.99,0,.03),.68)
    elif id=='B05':
        habitat(m,3.2,2.7)
        m.curve('tree_branch',[(-1,-.4,.12),(-.45,0,.8),(.18,.08,1.37),(.85,.18,1.94)],[.09,.065,.04,.015],'bark',n=20)
        for j in range(18):
            a=j*2.399;p=Vector((.20,.08,1.25))+Vector((math.cos(a)*.36,math.sin(a)*.27,.24*math.cos(j*.7)))
            m.leaf('woven_nest_leaf',p,p+Vector((math.cos(a)*.40,math.sin(a)*.35,.15)),.18,'leaf')
        for j in range(11):
            a=j*.65;m.curve('larval_silk_seam',[(.2+.35*math.cos(a),.08+.28*math.sin(a),1.18),(.2+.4*math.cos(a+.2),.08+.3*math.sin(a+.2),1.34)],.002,'silk',n=5)
        for j in range(11):place(m,ant,(-.78+j*.145,-.25+j*.044,.31+j*.10),.13,Matrix.Rotation(-.7,3,'Z'))
        for j in range(6):m.leaf('branch_leaf',(.4,.12,1.5),(.4+math.cos(j)*.6,.12+math.sin(j)*.45,1.7+j*.035),.13)
    elif id=='B06':
        habitat(m,1.15,2.3)
        m.curve('upright_branch',[(-.25,-.55,.1),(-.16,-.10,.46),(.04,.45,1.03),(.21,.7,1.47)],[.045,.032,.02,.008],'bark',n=16)
        place(m,mantid,(0,.03,.28),.69)
        for j in range(5):m.leaf('habitat_leaf',(-.10,-.1,.4+j*.19),(-.45 if j%2 else .40,.3+j*.1,.65+j*.18),.10)
    elif id=='B07':
        habitat(m,1.15,2.3,'aquatic')
        for j in range(8):
            x=RNG.uniform(-.45,.45);y=RNG.uniform(-.9,.9)
            m.curve('water_plant',[(x,y,.06),(x+.09,y,.4),(x-.07,y+.1,.9)],[.018,.012,.002],'leaf',n=8)
        # Aquatic beetle and freshwater gastropod teaching models.
        place(m,beetle,(0,-.3,.10),.31,color='gold')
        for j in range(3):place(m,snail,(-.22+j*.23,.43,.10),.70)
        m.ellipsoid('water_meniscus',(0,0,1.07),(.50,1.02,.012),'water',48,8)
    elif id=='B08':
        habitat(m,2.8,1.05,'litter')
        place(m,millipede,(-.58,0,.07),.77,Matrix.Rotation(.4,3,'Z'))
        place(m,millipede,(.43,.05,.07),.58,Matrix.Rotation(-1.0,3,'Z'))
        for j in range(6):
            x=-.9+j*.33
            m.tube('fungal_stipe',[(x,.3,.08),(x,.3,.21)],[.012,.015],'cream',10)
            m.ellipsoid('fungal_cap',(x,.3,.21),(.058,.052,.025),'orange',24,12)
    elif id=='B09':place(m,beetle,(0,0,.02),1.12,opened=True)
    elif id=='B10':
        # Separate head studies show mandibles, a coiled proboscis, and stylet.
        for x in (-.83,0,.83):
            m.ellipsoid('head_capsule',(x,0,.27),(.23,.20,.22),'chitin',36,24,.025)
            for s in (-1,1):m.ellipsoid('compound_eye',(x+s*.18,.08,.31),(.058,.09,.10),'gold',24,16)
        for s in (-1,1):m.curve('chewing_mandible',[(-.83+s*.11,.14,.22),(-.83+s*.21,.37,.16),(-.83+s*.05,.50,.15)],[.055,.046,.002],'boneLight',n=12)
        pts=[]
        for j in range(100):
            t=j/99;a=t*PI*4;r=.15*(1-t)+.02
            pts.append((r*math.cos(a),.25+r*math.sin(a),.18))
        m.tube('coiled_proboscis',pts,.014,'gold',10)
        m.tube('piercing_stylet',[(.83,.16,.22),(.83,.57,.07)],[.018,.001],'gold',10)
    elif id=='B11':
        rot=wall()
        old=m.scope((-2.2,0,.8),1,rot)
        m.leaf('host_leaf',(-.25,-.20,0),(.25,.18,.02),.18)
        for j in range(9):m.ellipsoid('egg',(-.07+(j%3)*.06,-.08+(j//3)*.06,.04),(.022,.025,.031),'cream',18,12)
        m.restore(old)
        old=m.scope((-.8,0,.85),1,rot)
        for j in range(12):
            p=(-.35+j*.064,.06*math.sin(j*.5),.09)
            m.ellipsoid('larval_segment',p,(.045,.075,.067),'leafLight',24,14)
            for s in (-1,1):m.tube('larval_seta',[(p[0],p[1]+s*.05,p[2]),(p[0],p[1]+s*.09,p[2]+.02)],[.004,.001],'chitin',5)
        m.restore(old)
        old=m.scope((.65,0,.83),1,rot)
        m.ellipsoid('pupa',(0,0,.05),(.16,.37,.12),'leaf',36,22,.03)
        for j in range(8):m.curve('pupal_segment',[(-.1,-.24+j*.062,.1),(0,-.26+j*.062,.17),(.1,-.24+j*.062,.1)],.005,'gold',n=6)
        m.restore(old)
        place(m,butterfly,(2.02,0,.85),.8,rot,color='orange')
    elif id=='B12':
        for j in range(3):
            x=-.8+j*.8
            for k in range(10):
                a=k*2*PI/10
                m.leaf('flower_petal',(x,0,.21),(x+.29*math.cos(a),.29*math.sin(a),.24),.08,'cream')
            m.ellipsoid('flower_disc',(x,0,.23),(.09,.09,.055),'orange',24,16)
            for k in range(15):
                a=k*2.399;r=.07*math.sqrt(k/15)
                m.ellipsoid('pollen_grain',(x+r*math.cos(a),r*math.sin(a),.28),(.009,.009,.01),'gold',10,6)
        place(m,butterfly,(0,0,.29),.43,color='orange')
    elif id=='B13':
        place(m,spider,(-.78,0,.04),.65)
        place(m,scorpion,(.75,-.1,.03),.70)
    elif id=='B14':
        habitat(m,1.15,2.3)
        place(m,spider,(0,-.3,.09),.51,hairy=True)
        m.ellipsoid('burrow_roof',(0,.65,.21),(.38,.43,.19),'bark',36,20,.10)
    elif id=='B15':
        habitat(m,1.15,2.3)
        for x in (-.45,.45):m.curve('web_anchor_branch',[(x,-.6,.1),(x,.1,.7),(x,.55,1.4)],[.033,.026,.008],'bark',n=12)
        old=m.scope((0,.25,.80),.70,Matrix.Rotation(PI/2,3,'X'))
        web(m,.59)
        place(m,spider,(0,0,.01),.16)
        m.restore(old)
    elif id=='B16':
        old=m.scope((-1.03,0,.85),1,wall());web(m,.70);m.restore(old)
        old=m.scope((1.05,0,.85),1,wall());web(m,.69,irregular=True);m.restore(old)
    elif id=='L02':
        place(m,microscope,(-.42,0,0),1)
        for j in range(5):
            x=.25+(j%2)*.24;y=-.30+(j//2)*.25
            m.ellipsoid('sample_dish',(x,y,.015),(.10,.10,.015),'white',24,12)
            place(m,beetle,(x,y,.03),.045,color='gold')
    elif id=='L01':
        for j in range(4):
            place(m,ammonite,(-1.45+j*.95,0,.02),.85,r=.33)
        place(m,beetle,(0,.60,.03),.13,color='blue')
    elif id=='C01':
        for j in range(3):
            y=-3.7+j*3.65;h=4.2-j*.38
            m.curve('tree_fern_trunk',[(0,y,0),(.10,y+.05,h*.4),(.02,y,h)],[.13,.10,.075],'bark',n=24)
            for k in range(26):
                z=(k+.6)*h/26;m.ellipsoid('trunk_leaf_scar',(0,y,z),(.132,.132,.027),'stone',16,8,.12)
            fern(m,(0,y,h),1.42)
        for j in range(13):fern(m,((-.43 if j%2 else .43),-5.2+j*.85,.03),.45)
    else:
        import palaeo_specimens
        importlib.reload(palaeo_specimens)
        return palaeo_specimens.palaeo_build(id)
    return m

def web(m,r,irregular=False):
    for j in range(22):
        a=j*2*PI/22
        m.tube('radial_silk',[(0,0,0),(r*math.cos(a),r*math.sin(a),0)],.0018,'silk',5)
    pts=[]
    for i in range(850):
        t=i/849;a=t*PI*2*18;rad=r*(.08+.86*t)
        if irregular:rad*=1+.1*math.sin(a*3)
        pts.append((rad*math.cos(a),rad*math.sin(a),.002*math.sin(a*7)))
    m.tube('capture_spiral',pts,.0012,'silk',5)

IDS=globals().get('IDS',[f'B{i:02}' for i in range(1,17)]+['L01','L02','C01']+[f'D{i:02}' for i in range(1,10)]+['F01','F02'])
report=[]
for id in IDS:
    e=ENTRIES[id];col=bpy.data.collections['MODEL_'+id]
    # Rebuild only our own original generated parts, preserving anything else.
    for ob in list(col.objects):
        if ob.get('specimen_authoring') in {'Original interpretive model; not a specimen scan','Smithsonian Institution Triceratops, CC0; reoriented and materialised'}:
            me=ob.data;bpy.data.objects.remove(ob,do_unlink=True)
            if me.users==0:bpy.data.meshes.remove(me)
        else:raise RuntimeError('Unrecognised content in '+col.name)
    m=build(id)
    if m is None:continue
    x,y,z=e['position'];obs=m.finish(col,Vector((x,-z,y)))
    bpy.context.view_layer.update()
    pp=[ob.matrix_world@Vector(v) for ob in obs for v in ob.bound_box]
    lo=[min(v[i] for v in pp) for i in range(3)];hi=[max(v[i] for v in pp) for i in range(3)]
    w,h,d=e['envelope'];dims=[hi[0]-lo[0],hi[2]-lo[2],hi[1]-lo[1]]
    within=lo[0]>=x-w/2-.02 and hi[0]<=x+w/2+.02 and lo[1]>=-z-d/2-.02 and hi[1]<=-z+d/2+.02 and lo[2]>=y-.02 and hi[2]<=y+h+.02
    if not within:raise RuntimeError(f'{id} exceeds its envelope: {lo}, {hi}; origin {e["position"]}, envelope {e["envelope"]}')
    runpy.run_path(str(P/'blender/export_static_exhibit.py'),init_globals={'EXHIBIT_ID':id})
    report.append({'id':id,'dimensions_xyz':dims,'within_envelope':within,'vertices':sum(len(ob.data.vertices) for ob in obs),'bytes':(P/'public/models'/f'{id}.glb').stat().st_size})
    print('Completed',id)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'blender/ThreeMuseum_Collection.blend'))
report_path=P/'docs/validation/specimen-build.json'
existing={e['id']:e for e in json.loads(report_path.read_text())} if report_path.exists() else {}
existing.update({e['id']:e for e in report})
report_path.write_text(json.dumps(list(existing.values()),indent=2))
result={'exhibits':report}
