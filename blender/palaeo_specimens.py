"""Original skeletal reconstructions for the Deep Time galleries.

These are interpretive meshes with approximate proportions, not scans or
scientifically measured reconstructions of individual museum specimens.
"""
from specimen_geometry import *

def vertebra(m,p,r=.12,length=.18,spine=.18):
    x,y,z=p
    m.bone('centrum',(x,y-length/2,z),(x,y+length/2,z),r)
    for s in (-1,1):
        m.curve('neural_arch',[(x+s*r*.7,y,z),(x+s*r*.65,y,z+r*1.45),(x,y,z+r*1.9)],[r*.32,r*.29,r*.34],'boneLight',n=10)
        m.bone('transverse_process',(x+s*r*.4,y,z+r),(x+s*r*2.0,y+length*.1,z+r*.72),r*.28)
    m.tube('neural_spine',[(x,y,z+r*1.7),(x,y-length*.15,z+r*1.7+spine)],[r*.37,r*.23],'bone',10)

def ribcage(m,y0,length,z,width,height,count=15):
    for j in range(count):
        t=j/(count-1);y=y0+length*(t-.5);f=math.sin(PI*(.12+.76*t))**.65
        vertebra(m,(0,y,z),.11*width,.86*length/count,.20*height)
        for s in (-1,1):
            pts=[(s*.09*width,y,z+.06*height),(s*.60*width,y-.10*length,z-.10*height),
                 (s*width*f,y-.06*length,z-.48*height),(s*.73*width*f,y-.02*length,z-.90*height),
                 (s*.20*width,y+.01*length,z-height)]
            m.curve('dorsal_rib',pts,[.047*width,.058*width,.045*width,.032*width,.013*width],'boneLight',steps=7,n=12)
    m.curve('sternum',[(0,y0-length*.3,z-height),(0,y0,z-height*1.05),(0,y0+length*.33,z-height*.92)],.075*width,'bone',n=12)

def digits(m,p,s=1,count=4,mat='bone'):
    x,y,z=p
    for j in range(count):
        dx=(j-(count-1)/2)*.11*s
        a=(x+dx,y,z+.08*s);b=(x+dx*1.2,y+.23*s,z+.035*s);c=(x+dx*1.35,y+.38*s,z+.025*s)
        m.bone('metapodial',a,b,.040*s,mat);m.bone('phalange',b,c,.032*s,mat)
        m.curve('ungual',[c,(c[0],c[1]+.10*s,c[2]+.02*s),(c[0],c[1]+.18*s,c[2]-.015*s)],[.047*s,.028*s,.001*s],'bone',n=10)

def leg(m,hip,knee,ankle,r=.12,foot=1,with_foot=True):
    m.bone('femur_or_humerus',hip,knee,r)
    m.bone('tibia_or_radius',knee,ankle,r*.75)
    offset=Vector((r*.8,0,0))
    m.bone('fibula_or_ulna',Vector(knee)+offset,Vector(ankle)+offset,r*.28)
    m.ellipsoid('articular_condyle',knee,(r*1.2,r*.82,r*.9),'boneLight',24,14,.05)
    if with_foot:
        x,y,z=ankle
        for j in range(5):
            a=(j-2)*.40
            p=(x+math.sin(a)*.16*foot,y+math.cos(a)*.18*foot,z*.5)
            m.bone('short_metapodial',(p[0],p[1]-.06*foot,z+.12*foot),p,.055*foot)
            m.ellipsoid('terminal_phalanx',(p[0],p[1]+.05*foot,p[2]),(.055*foot,.085*foot,.055*foot),'boneLight',20,12,.03)

def skull(m,kind='theropod'):
    # Open, fenestrated cheek structures connect the roof, jugal and snout.
    width=.27 if kind=='theropod' else .22
    for s in (-1,1):
        x=s*width
        m.curve('maxilla',[(x,0,.29),(x*1.18,.37,.19),(x*.7,.94,.13),(x*.30,1.15,.18)],[.055,.073,.045,.025],'boneLight',n=14)
        m.curve('nasal_roof',[(x*.52,0,.66),(x*.72,.4,.54),(x*.44,.94,.32),(x*.30,1.15,.18)],[.060,.062,.044,.025],'bone',n=14)
        m.curve('orbital_rim',[(x,0,.3),(x*1.15,-.08,.50),(x*.62,.04,.68),(x*.95,.25,.49),(x,0,.3)],.043,'boneLight',steps=7,n=12)
        m.bone('lacrimal',(x*.95,.25,.49),(x*1.18,.37,.19),.052)
        m.bone('antorbital_strut',(x*.78,.58,.46),(x*.95,.64,.18),.030)
        m.curve('dentary',[(x,-.10,.18),(x*.96,.2,-.01),(x*.65,.80,-.07),(x*.2,1.11,.02)],[.065,.065,.040,.020],'boneLight',n=14)
        m.bone('quadrate',(x,-.10,.18),(x*.64,-.13,.53),.05)
        if kind=='theropod':
            for j in range(13):
                t=j/12;y=.22+t*.80;xx=x*(1.12-.78*t);zz=.19-.05*t
                length=.12+.11*math.sin(PI*t)
                m.curve('maxillary_tooth',[(xx,y,zz),(xx,y+.022,zz-length*.7),(xx,y+.045,zz-length)],[.026,.017,.001],'ivory',steps=3,n=10)
                m.curve('dentary_tooth',[(xx*.85,y,-.02),(xx*.85,y+.02,.05),(xx*.85,y+.04,.10)],[.023,.013,.001],'ivory',steps=3,n=10)
        else:
            for j in range(12):
                y=.50+j*.041
                m.bone('tooth_battery',(x*.8,y,.12),(x*.8,y,.24),.019,'ivory')
    m.ellipsoid('braincase',(0,-.06,.47),(.17,.19,.17),'bone',28,20,.09)
    m.bone('palatal_arch',(-width,.10,.22),(width,.10,.22),.04)
    m.bone('premaxillary_arch',(-width*.30,1.12,.19),(width*.30,1.12,.19),.032)
    if kind in ('triceratops','protoceratops'):
        # Frill is a curved bony sheet, with a scalloped perimeter.
        vs=[(0,-.09,.48)];fs=[]
        for j in range(49):
            a=2*PI*j/48
            rad=1+.035*math.cos(a*16)
            vs.append((.68*math.cos(a)*rad,-.22-.25*math.sin(a),.65+.57*math.sin(a)*rad))
        fs=[(0,j+1,j+2) for j in range(48)]
        m.mesh('parietosquamosal_frill',vs,fs,'boneLight')
        m.tube('frill_rim',vs[1:],.033,'bone',10)
        for j in range(15):
            a=j*PI/14
            p=Vector((.68*math.cos(a),-.22-.25*math.sin(a),.65+.57*math.sin(a)))
            m.tube('epoccipital', [p,p+Vector((math.cos(a)*.075,0,math.sin(a)*.075))],[.047,.001],'bone',10)
        m.curve('rostral_beak',[(0,.98,.28),(0,1.20,.21),(0,1.22,.05)],[.105,.07,.001],'bone',n=18)
        if kind=='triceratops':
            for s in (-1,1):m.curve('brow_horn',[(s*.26,.04,.65),(s*.32,.37,1.04),(s*.27,.73,1.25)],[.10,.065,.001],'boneLight',steps=9,n=20)
            m.curve('nasal_horn',[(0,.81,.33),(0,.86,.60),(0,.94,.74)],[.078,.042,.001],'boneLight',n=18)

def sauropod(m):
    ribcage(m,-5.8,3.6,4.8,1.10,1.55,15)
    for y in (-7.15,-4.0):
        for s in (-1,1):
            hip=(s*.82,y,4.45);knee=(s*.92,y+.20,2.3);ankle=(s*.92,y+.05,.17)
            leg(m,hip,knee,ankle,.24,1.0)
            m.curve('girdle',[(s*.18,y-.45,4.94),(s*.8,y,4.50),(s*1.01,y+.43,3.75)],[.12,.22,.12],'boneLight',n=18)
    # Long neck passes over the central cross aisle, with >2.8m head clearance.
    for j in range(19):
        t=j/18;y=-3.8+t*15.0;z=4.83+1.22*math.sin(t*PI*.55);r=.19*(1-.55*t)
        vertebra(m,(0,y,z),r,.65,.12)
        for s in (-1,1):m.curve('cervical_rib',[(s*r,y,z),(s*r*1.6,y-.36,z-.23),(s*r*.9,y-1.1,z-.28)],[.035,.024,.009],'boneLight',n=8)
    old=m.scope((0,11.5,5.90),.72);skull(m,'sauropod');m.restore(old)
    for j in range(34):
        t=j/33;y=-7.6-5.8*t;z=4.55-.90*t+.38*math.sin(t*PI);r=.18*(1-t)+.018
        vertebra(m,(.20*math.sin(t*PI),y,z),r,.14,.18*(1-t))
        if j<22:m.tube('haemal_arch',[(.20*math.sin(t*PI),y,z-.1),(.20*math.sin(t*PI),y-.08,z-.42*(1-t))],[r*.28,.015],'bone',8)
    for y in (-7.0,-4.15):
        m.tube('mount_upright',[(0,y,.02),(0,y,4.60)],.035,'steel',12)
        m.tube('mount_crossbar',[(-.74,y,4.36),(.74,y,4.36)],.025,'steel',10)

def theropod(m):
    ribcage(m,.12,1.95,3.55,.67,1.27,13)
    for s in (-1,1):
        m.curve('ilium',[(s*.52,-.80,3.8),(s*.65,-.40,3.93),(s*.59,.25,3.68)],[.14,.19,.12],'bone',n=18)
        for j in range(5):m.bone('sacral_rib',(s*.08,-.70+j*.15,3.56),(s*.57,-.70+j*.15,3.78),.060)
        m.bone('pubis',(s*.40,-.5,3.35),(s*.28,.20,2.1),.085)
        m.bone('ischium',(s*.4,-.5,3.35),(s*.27,-1.12,2.4),.065)
        leg(m,(s*.59,-.40,3.48),(s*.79,.37,2.35),(s*.77,-.23,.60),.16,1.5,False)
        m.bone('metatarsus',(s*.77,-.23,.6),(s*.80,.12,.13),.075)
        digits(m,(s*.80,.12,.04),1.55,3)
        m.curve('scapula',[(s*.55,.62,3.35),(s*.50,1.05,2.88),(s*.37,.92,2.58)],[.10,.08,.05],'boneLight',n=14)
        m.bone('humerus',(s*.44,.96,2.85),(s*.57,1.30,2.50),.055)
        m.bone('forearm',(s*.57,1.30,2.50),(s*.52,1.57,2.53),.038)
        for j in range(2):m.curve('manual_ungual',[(s*(.49+j*.08),1.53,2.53),(s*(.49+j*.08),1.77,2.56),(s*(.49+j*.08),1.80,2.44)],[.028,.023,.001],'bone',n=10)
    for j in range(10):
        t=j/9;vertebra(m,(0,1.08+t*.88,3.53+t*.55),.13,.11,.13)
    old=m.scope((0,1.98,3.99),1.14);skull(m);m.restore(old)
    for j in range(39):
        t=j/38;vertebra(m,(.33*math.sin(t*PI),-1.05-4.0*t,3.5-1.15*t),.16*(1-t)+.012,.115,.24*(1-t))
        if j<26:m.bone('chevron',(.33*math.sin(t*PI),-1.05-4*t,3.4-1.15*t),(.33*math.sin(t*PI),-1.1-4*t,3.0-1.15*t),.025*(1-t)+.006)
    m.tube('mount_upright',[(0,-.5,.02),(0,-.5,3.5)],.026,'steel',12)

def ceratopsian(m,small=False):
    scale=.27 if small else 1
    old=m.scope((0,0,0),scale)
    ribcage(m,-.35,2.65,2.70,.87,1.33,16)
    for s in (-1,1):
        for y,front in [(-1.37,False),(.66,True)]:
            hip=(s*.70,y,2.50);knee=(s*(.90 if front else .78),y+(.30 if front else .05),1.30);ankle=(s*.86,y+.12,.13)
            leg(m,hip,knee,ankle,.19 if not front else .15,1)
            m.curve('girdle',[(s*.28,y-.3,2.78),(s*.69,y,2.46),(s*.84,y+.35,2.0)],[.10,.17,.09],'boneLight',n=16)
    for j in range(6):vertebra(m,(0,1.00+j*.14,2.63-j*.025),.13,.12,.12)
    old2=m.scope((0,1.55,1.99),1.38);skull(m,'protoceratops' if small else 'triceratops');m.restore(old2)
    for j in range(30):
        t=j/29;vertebra(m,(.17*math.sin(t*PI),-1.80-2.5*t,2.5-.6*t),.14*(1-t)+.014,.085,.22*(1-t))
    m.tube('mount_upright',[(0,-.8,.01),(0,-.8,2.50)],.025,'steel',12)
    m.restore(old)

def armoured(m):
    # Compact nodosaur-like interpretive mount with ossified dermal armour.
    ribcage(m,-.20,1.65,1.54,.78,.83,13)
    for s in (-1,1):
        for y in (-.87,.55):leg(m,(s*.57,y,1.36),(s*.75,y+.08,.73),(s*.73,y+.12,.07),.11,.6)
    for j in range(12):
        y=-1+j*.17
        for k in range(5):
            a=(k-2)*.43;x=.78*math.sin(a);z=1.3+.50*math.cos(a)
            m.ellipsoid('osteoderm',(x,y,z),(.17,.11,.08),'bone',18,12,.10)
            m.tube('osteoderm_keel',[(x,y,z),(x*1.13,y-.015,z+.14)],[.07,.002],'boneLight',10)
    for s in (-1,1):
        for j in range(4):m.curve('lateral_spike',[(s*.70,.3-j*.30,1.39),(s*1.02,.25-j*.30,1.49),(s*1.24,.22-j*.30,1.54)],[.105,.06,.001],'boneLight',n=14)
    old=m.scope((0,.85,1.13),.63);skull(m,'herbivore');m.restore(old)
    for j in range(18):vertebra(m,(0,-1.16-j*.065,1.43-j*.025),.095*(1-j/20),.06,.09)

def pterosaur(m):
    ribcage(m,0,.62,.60,.16,.26,9)
    for j in range(7):vertebra(m,(0,.35+j*.06,.63+j*.045),.04,.045,.04)
    m.curve('elongate_beak',[(0,.74,.86),(0,1.13,.85),(0,1.71,.80)],[.10,.063,.001],'boneLight',n=16)
    m.curve('lower_jaw',[(0,.76,.78),(0,1.15,.70),(0,1.69,.78)],[.04,.028,.001],'bone',n=12)
    for s in (-1,1):
        joints=[(s*.12,.19,.63),(s*.51,.37,.68),(s*1.08,.53,.68),(s*1.80,.14,.64),(s*2.52,-.12,.58),(s*3.0,-.45,.47)]
        for j in range(5):m.bone('wing_digit' if j>1 else 'wing_arm',joints[j],joints[j+1],.042-j*.006)
        m.bone('hindlimb',(s*.10,-.25,.48),(s*.32,-.63,.30),.027)
        m.bone('hind_tibia',(s*.32,-.63,.30),(s*.45,-.96,.20),.019)
        digits(m,(s*.45,-.96,.17),.28,4)
        for j in range(3):m.curve('manual_claw',[(s*1.08,.53,.68),(s*(1.08+j*.09),.70,.71),(s*(1.1+j*.09),.77,.66)],[.018,.012,.001],'bone',n=8)
        m.tube('suspension_cable',[(s*1.05,.5,.7),(s*1.05,.5,2.30)],.003,'steel',8)

def diprotodon(m):
    ribcage(m,0,1.35,1.74,.60,.86,14)
    for s in (-1,1):
        for y in (-.53,.58):leg(m,(s*.46,y,1.60),(s*.56,y+.1,.86),(s*.55,y+.13,.10),.12,.64)
    m.ellipsoid('cranium',(0,.94,1.8),(.35,.36,.30),'bone',36,24,.05)
    for s in (-1,1):
        m.curve('zygomatic_arch',[(s*.28,.71,1.8),(s*.40,1.02,1.68),(s*.22,1.32,1.62)],.052,'boneLight',n=14)
        m.curve('dentary',[(s*.26,.77,1.55),(s*.25,1.14,1.38),(s*.09,1.46,1.47)],.057,'bone',n=14)
        m.curve('incisor',[(s*.07,1.34,1.58),(s*.07,1.55,1.55),(s*.07,1.61,1.46)],[.045,.035,.010],'ivory',n=14)
        m.ellipsoid('orbit',(s*.30,.89,1.91),(.023,.09,.085),'chitin',24,16)
    m.tube('mount_upright',[(0,-.3,.02),(0,-.3,1.63)],.018,'steel',10)

def fossil_slab(m,w=2.6,d=1.6,tracks=False):
    # A triangulated irregular stone surface; shallow carved tridactyl tracks.
    n=55;vs=[];fs=[]
    def track_depth(x,y):
        dep=0
        for cx,cy in [(-.52,-.40),(.35,.16),(-.48,.57)]:
            for angle in (-.55,0,.55):
                a=Vector((cx,cy));b=a+Vector((math.sin(angle)*.36,math.cos(angle)*.38))
                p=Vector((x,y));t=max(0,min(1,(p-a).dot(b-a)/(b-a).length_squared));dist=(p-(a+(b-a)*t)).length
                dep=max(dep,.036*math.exp(-(dist/.045)**2))
        return dep
    for j in range(n):
        y=-d/2+j*d/(n-1)
        for i in range(n):
            x=-w/2+i*w/(n-1)
            z=.07+.012*math.sin(x*19+y*11)*math.sin(y*21-x*7)
            if tracks:z-=track_depth(x,y)
            vs.append((x,y,z))
    for j in range(n-1):
        for i in range(n-1):a=j*n+i;fs.extend([(a,a+1,a+n),(a+1,a+n+1,a+n)])
    m.mesh('weathered_matrix',vs,fs,'stone')
    if not tracks:
        for x in (-.7,.35):
            old=m.scope((x,0,.025),.8);ammonite(m);m.restore(old)
        for j in range(9):m.bone('fossil_rib_fragment',(-.8+j*.18,.38,.07),(-.68+j*.18,.60,.08),.024,'bone')

def palaeo_build(id):
    m=Model(id)
    if id=='D01':sauropod(m)
    elif id=='D02':theropod(m)
    elif id=='D03':armoured(m)
    elif id=='D04':ceratopsian(m,True)
    elif id=='D05':fossil_slab(m,2.6,1.6,True)
    elif id=='D06':
        # Side-facing wall case: original tooth teaching casts.
        for j in range(5):
            y=-.95+j*.47
            m.curve('root_and_crown',[(0,y,.12),(0,y,.42),(0,y+.06,.75)],[.10,.075,.001],'ivory',n=24)
            for k in range(16):m.tube('serration',[(0,y+.065,.35+k*.019),(0,y+.085,.36+k*.019)],[.008,.001],'bone',6)
    elif id=='D07':diprotodon(m)
    elif id=='D08':pterosaur(m)
    elif id=='D09':
        for j in range(4):
            old=m.scope((-1.48+j*.95,0,.015),.8);ammonite(m,.36);m.restore(old)
    elif id=='F01':
        source=bpy.data.objects.get('Smithsonian_Triceratops_source')
        if source:
            rotation=Matrix.Rotation(PI,3,'Z')@Matrix.Rotation(-PI/2,3,'Y')
            vs=[rotation@v.co for v in source.data.vertices]
            low=Vector(tuple(min(p[i] for p in vs) for i in range(3)))
            high=Vector(tuple(max(p[i] for p in vs) for i in range(3)))
            centre=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
            m.mesh('Smithsonian_Triceratops',[v-centre for v in vs],[tuple(p.vertices) for p in source.data.polygons],'boneLight')
            for y,z in [(-1.25,1.6),(.35,1.18),(1.92,.60)]:
                m.tube('museum_mount',[(0,y,.015),(0,y,z)],.018,'steel',12)
                m.curve('support_yoke',[(-.21,y,z+.04),(0,y,z-.04),(.21,y,z+.04)],.014,'steel',n=10)
            m.source='Smithsonian Institution Triceratops, CC0; reoriented and materialised'
        else:ceratopsian(m)
    elif id=='F02':
        old=m.scope((-.75,0,.75),1,Matrix.Rotation(PI/2,3,'X'));fossil_slab(m,2.6,1.25);m.restore(old)
        for j in range(3):
            m.tube('preparation_tool',[(1.0+j*.42,0,.24),(1.0+j*.42,0,1.04)],[.025,.032],'bark',14)
            m.tube('steel_pick',[(1.0+j*.42,0,1.04),(1.0+j*.42,0,1.26)],[.013,.002],'steel',12)
    else:return None
    return m
