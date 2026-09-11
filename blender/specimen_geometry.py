"""Original specimen modelling helpers. Coordinates are Blender metres (Z up).

Surface detail is actual geometry or vertex colour so embedded GLBs do not
depend on Blender-only procedural shaders. Every exhibit stays editable.
"""
import bpy
import math
import random
from mathutils import Vector, Matrix
from collections import defaultdict

PI=math.pi
RNG=random.Random(711)

def material(name, color, metallic=0, rough=.5):
    m=bpy.data.materials.get('SPEC_'+name) or bpy.data.materials.new('SPEC_'+name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=rough
    return m

M={
 'chitin':material('Chitin',(0.018,.028,.024),.25,.29),
 'green':material('Iridescent jade',(.045,.26,.15),.65,.25),
 'blue':material('Iridescent blue',(.025,.17,.32),.6,.26),
 'gold':material('Iridescent bronze',(.38,.22,.055),.6,.3),
 'ivory':material('Ivory',(.72,.62,.42),0,.54),
 'bone':material('Fossil umber',(.24,.145,.075),0,.7),
 'boneLight':material('Fossil ridge',(.39,.28,.16),0,.65),
 'eye':material('Eyes',(.008,.012,.009),.05,.16),
 'leaf':material('Leaf jade',(.10,.25,.035),0,.57),
 'leafLight':material('Leaf new growth',(.25,.4,.055),0,.52),
 'bark':material('Bark',(.16,.082,.032),0,.9),
 'earth':material('Substrate',(.10,.060,.031),0,1),
 'stone':material('Matrix sandstone',(.40,.30,.18),0,.97),
 'silk':material('Silk',(.74,.67,.42),.1,.47),
 'orange':material('Ochre scales',(.63,.20,.025),0,.68),
 'cream':material('Pale scales',(.83,.77,.59),0,.65),
 'membrane':material('Wing membrane',(.23,.26,.20),0,.58),
 'steel':material('Mount steel',(.035,.043,.046),.7,.38),
 'white':material('Instrument enamel',(.79,.79,.72),.15,.32),
 'red':material('Internal anatomy',(.43,.055,.034),0,.6),
 'water':material('Water surface',(.018,.15,.16),.25,.22),
}

class Model:
    def __init__(self, name):
        self.name=name
        self.source=None
        self.parts=[]
        self.transform=Matrix.Identity(4)
    def mesh(self,name,vs,fs,mat='chitin',smooth=True):
        mesh=bpy.data.meshes.new(self.name+'_'+name)
        mesh.from_pydata([self.transform@Vector(v) for v in vs],[],fs)
        mesh.materials.append(M[mat])
        mesh.update()
        for p in mesh.polygons:p.use_smooth=smooth
        obj=bpy.data.objects.new(mesh.name,mesh)
        self.parts.append(obj)
        return obj
    def ellipsoid(self,name,c,r,mat='chitin',nu=32,nv=18,grain=0):
        vs=[];fs=[]
        for j in range(nv+1):
            phi=PI*j/nv
            for i in range(nu):
                a=2*PI*i/nu
                noise=1+grain*(math.sin(a*11+phi*9)*math.sin(phi*23+a*3))
                vs.append((c[0]+r[0]*math.sin(phi)*math.cos(a)*noise,
                           c[1]+r[1]*math.sin(phi)*math.sin(a)*noise,
                           c[2]+r[2]*math.cos(phi)*noise))
        for j in range(nv):
            for i in range(nu):
                a=j*nu+i;b=j*nu+(i+1)%nu
                fs.append((a,a+nu,b+nu,b))
        return self.mesh(name,vs,fs,mat)
    def tube(self,name,points,radii,mat='chitin',n=10):
        points=[Vector(p) for p in points]
        if isinstance(radii,(float,int)):radii=[radii]*len(points)
        vs=[];fs=[]
        for j,p in enumerate(points):
            tangent=points[min(j+1,len(points)-1)]-points[max(j-1,0)]
            tangent.normalize()
            ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((1,0,0))
            u=tangent.cross(ref).normalized();v=tangent.cross(u).normalized()
            for i in range(n):vs.append(p+radii[j]*(u*math.cos(2*PI*i/n)+v*math.sin(2*PI*i/n)))
        for j in range(len(points)-1):
            for i in range(n):
                a=j*n+i;b=j*n+(i+1)%n
                fs.append((a,b,b+n,a+n))
        fs.extend([tuple(reversed(range(n))),tuple(range((len(points)-1)*n,len(points)*n))])
        return self.mesh(name,vs,fs,mat)
    def curve(self,name,points,radii,mat='chitin',steps=5,n=10):
        # Catmull-Rom with clamped end conditions, varying radius.
        pp=[Vector(points[0])]+[Vector(p) for p in points]+[Vector(points[-1])]
        rr=[radii]*len(points) if isinstance(radii,(float,int)) else radii
        vs=[];rs=[]
        for j in range(len(points)-1):
            p0,p1,p2,p3=pp[j:j+4]
            for k in range(steps):
                t=k/steps
                vs.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
                rs.append(rr[j]*(1-t)+rr[j+1]*t)
        vs.append(Vector(points[-1]));rs.append(rr[-1])
        return self.tube(name,vs,rs,mat,n)
    def bone(self,name,a,b,r,mat='bone'):
        a=Vector(a);b=Vector(b);d=b-a
        points=[a+d*t for t in (0,.06,.18,.40,.65,.83,.95,1)]
        return self.tube(name,points,[r*x for x in (.78,1.16,.82,.55,.58,.76,1.12,.8)],mat,16)
    def leaf(self,name,a,b,width,mat='leaf'):
        a=Vector(a);b=Vector(b);axis=b-a
        side=axis.cross(Vector((0,0,1)))
        if side.length<.01:side=Vector((1,0,0))
        side.normalize()
        vs=[];fs=[]
        for j in range(13):
            t=j/12;centre=a+axis*t+Vector((0,0,.13*axis.length*math.sin(PI*t)))
            for k in (-1,0,1):
                vs.append(centre+side*(k*width*math.sin(PI*t)**.8)+Vector((0,0,-abs(k)*width*.16*math.sin(PI*t))))
        for j in range(12):
            for k in range(2):i=j*3+k;fs.append((i,i+3,i+4,i+1))
        obj=self.mesh(name,vs,fs,mat)
        self.curve(name+'_midrib',[a,a+axis*.5+Vector((0,0,.13*axis.length)),b],.004,'leafLight',n=6)
        return obj
    def scope(self,position=(0,0,0),scale=1,rotation=None):
        old=self.transform.copy()
        self.transform=old@Matrix.Translation(Vector(position))@(rotation.to_4x4() if rotation else Matrix.Identity(4))@Matrix.Scale(scale,4)
        return old
    def restore(self,old):self.transform=old
    def finish(self,col,origin):
        # Merge by material for a small number of web draw calls, preserving named
        # source components in the generator instead of exporting thousands of nodes.
        bymat=defaultdict(list)
        for o in self.parts:bymat[o.data.materials[0].name].append(o)
        merged=[]
        for mat,parts in bymat.items():
            vs=[];fs=[]
            for p in parts:
                start=len(vs);vs.extend([v.co[:] for v in p.data.vertices])
                fs.extend([tuple(i+start for i in f.vertices) for f in p.data.polygons])
            mesh=bpy.data.meshes.new(self.name+'_'+mat)
            mesh.from_pydata(vs,[],fs);mesh.materials.append(bpy.data.materials[mat]);mesh.update()
            for p in mesh.polygons:p.use_smooth=True
            # Portable per-vertex mottling: exported as COLOR_0, no external maps.
            attr=mesh.color_attributes.new(name='SpecimenColor',type='FLOAT_COLOR',domain='POINT')
            base=bpy.data.materials[mat].diffuse_color
            earthy=any(k in mat for k in ('Fossil','Bark','Matrix','Substrate'))
            for i,v in enumerate(mesh.vertices):
                x,y,z=v.co
                n=(math.sin(x*41+y*29+z*37)*math.sin(x*13-y*23+z*17)+math.sin(x*5+y*7+z*3))*.5
                factor=(.78+.20*n) if earthy else (.95+.05*n)
                attr.data[i].color=(base[0]*factor,base[1]*factor,base[2]*factor,1)
            matdata=bpy.data.materials[mat]
            node=matdata.node_tree.nodes.get('Specimen vertex colour')
            if node is None:
                node=matdata.node_tree.nodes.new('ShaderNodeVertexColor');node.name='Specimen vertex colour';node.layer_name='SpecimenColor'
                matdata.node_tree.links.new(node.outputs['Color'],matdata.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
            obj=bpy.data.objects.new(mesh.name,mesh);col.objects.link(obj);obj.location=origin
            obj['specimen_authoring']=self.source or 'Original interpretive model; not a specimen scan'
            merged.append(obj)
            for p in parts:
                me=p.data;bpy.data.objects.remove(p)
                bpy.data.meshes.remove(me)
        self.parts=[]
        return merged

def beetle(m,kind='scarab',color='green',opened=False):
    m.ellipsoid('ventral_abdomen',(0,-.36,.39),(.42,.70,.25),'chitin')
    # Seven visible ventral sclerites.
    for j in range(7):
        y=-.83+j*.16
        m.curve('abdominal_sclerite', [(-.31,y,.32),(0,y-.045,.19),(.31,y,.32)],.018,'gold',n=8)
    for s in (-1,1):
        old=m.scope(rotation=Matrix.Rotation(s*.58 if opened else 0,3,'Y'))
        m.ellipsoid('left_elytron' if s<0 else 'right_elytron',(s*.213,-.34,.53),(.216,.73,.285),color,48,28,.008)
        for j in range(1,8):
            x=s*(.035+j*.047)
            rr=math.sqrt(max(0,1-(x/.45)**2))
            pts=[]
            for k in range(20):
                t=-1.22+k*2.44/19
                pts.append((x,-.34+.7*math.sin(t)*rr,.54+.28*math.cos(t)*rr))
            m.tube('elytral_stria',pts,.0035,'chitin',6)
        m.restore(old)
    m.ellipsoid('pronotum',(0,.45,.52),(.39,.31,.26),color,40,22,.01)
    m.ellipsoid('head',(0,.85,.44),(.265,.255,.19),'chitin',36,20,.015)
    for s in (-1,1):
        m.ellipsoid('compound_eye',(s*.238,.89,.51),(.043,.075,.053),'eye',24,16)
        for j in range(8):
            phi=.15+j*PI/9
            for k in range(12):
                a=k*2*PI/12+(j%2)*PI/12
                m.ellipsoid('ommatidium',(s*.238+.044*math.sin(phi)*math.cos(a),.89+.076*math.sin(phi)*math.sin(a),.51+.054*math.cos(phi)),(.0038,.004,.0038),'eye',6,4)
        for j in range(3):
            y=.4-j*.39
            pts=[(s*.27,y,.38),(s*.65,y+.13-j*.1,.47),(s*.85,y+.4-j*.3,.20),(s*1.02,y+.51-j*.36,.11)]
            for k in range(3):m.bone('coxa_femur_tibia',pts[k],pts[k+1],(.065,.045,.023)[k],'chitin')
            for k in range(5):
                p=Vector(pts[2]).lerp(Vector(pts[3]),k/5)
                m.tube('tibial_spine',[p,p+Vector((s*.075,-.04,.025))],[.012,.001],'chitin',6)
            end=Vector(pts[-1])
            for k in range(4):
                dest=end+Vector((s*.045,.035-j*.03,-.014))
                m.bone('tarsomere',end,dest,.014-k*.002,'chitin');end=dest
            for d in (-1,1):m.curve('paired_tarsal_claw',[end,end+Vector((s*.055,d*.035,.025)),end+Vector((s*.068,d*.04,0))],[.009,.007,.001],n=6)
        m.curve('antenna',[(s*.19,1.0,.46),(s*.38,1.18,.48),(s*.49,1.36,.50)],[.02,.015,.012],n=8)
        if kind=='longhorn':
            m.curve('long_antenna',[(s*.49,1.36,.5),(s*.9,1.4,.62),(s*1.2,.5,.5),(s*1.15,-.7,.3)],[.014,.012,.008,.002],n=8)
        else:
            for j in range(3):m.ellipsoid('antennal_club',(s*(.46+j*.035),1.38+j*.025,.5),(.03,.075,.027),'gold',16,10)
        mand=[(s*.16,1.04,.42),(s*.24,1.22,.43),(s*.10,1.34,.44)]
        if kind=='stag':mand=[(s*.17,1.02,.46),(s*.35,1.44,.50),(s*.28,1.83,.52),(s*.08,1.94,.52)]
        m.curve('mandible',mand,[.05]*(len(mand)-1)+[.003],'chitin',n=12)
        if kind=='stag':
            for j in range(4):m.tube('mandibular_tooth',[(s*.3,1.32+j*.13,.51),(s*.15,1.37+j*.13,.51)],[.038,.001],n=8)
    if opened:
        for s in (-1,1):
            outline=[(.21,.18,.6),(.55,.12,.68),(1.12,-.07,.75),(1.45,-.5,.78),(1.46,-.80,.76),(1.3,-.98,.73),(.87,-.99,.65),(.39,-.58,.59)]
            outline=[(s*x,y,z) for x,y,z in outline]
            centre=(s*.77,-.41,.69)
            m.mesh('unfolded_hindwing',[centre]+outline,[(0,i+1,(i+1)%8+1) for i in range(8)],'membrane')
            m.tube('costal_margin',outline+[outline[0]],.006,'chitin',6)
            root=outline[0]
            for j in range(2,8):
                end=outline[j]
                mid=Vector(root).lerp(Vector(end),.55)+Vector((0,0,.008))
                m.curve('radial_wing_vein',[root,mid,end],.004,'chitin',n=6)
                if j<6:
                    cross=Vector(root).lerp(Vector(outline[j+1]),.68)+Vector((0,0,.009))
                    m.tube('wing_crossvein',[mid,cross],.0025,'gold',6)

def ant(m):
    m.ellipsoid('gaster',(0,-.4,.25),(.15,.24,.15),'green',24,16)
    m.ellipsoid('petiole',(0,-.10,.29),(.065,.065,.09),'orange',20,12)
    m.ellipsoid('mesosoma',(0,.12,.3),(.10,.19,.105),'orange',24,16)
    m.ellipsoid('head',(0,.4,.34),(.14,.16,.115),'orange',24,16)
    for s in (-1,1):
        m.ellipsoid('eye',(s*.125,.43,.38),(.025,.038,.025),'eye',12,8)
        for j in range(3):
            m.tube('six_jointed_legs',[(s*.08,.22-j*.1,.3),(s*.27,.37-j*.2,.37),(s*.43,.44-j*.32,.035)],[.017,.012,.003],n=8)
        m.tube('elbowed_antenna',[(s*.08,.51,.37),(s*.23,.70,.44),(s*.11,.84,.48)],[.012,.008,.002],n=8)
        m.curve('mandibles',[(s*.06,.52,.3),(s*.09,.62,.3),(0,.65,.3)],[.025,.014,.001],n=8)

def spider(m,hairy=False):
    m.ellipsoid('abdomen',(0,-.31,.35),(.27,.39,.26),'bark' if hairy else 'gold',32,20,.015)
    m.ellipsoid('cephalothorax',(0,.19,.34),(.22,.25,.17),'chitin',32,20)
    for s in (-1,1):
        for j in range(4):
            y=.32-j*.11
            pts=[(s*.16,y,.34),(s*.40,.72-j*.40,.49),(s*(.63+.10*math.sin(j)),.80-j*.51,.32),(s*.82,.87-j*.57,.025)]
            m.tube('walking_leg',pts,[.048,.043,.03,.009],'bark' if hairy else 'chitin',12)
            if hairy:
                for k in range(24):
                    t=RNG.random();p=Vector(pts[1]).lerp(Vector(pts[3]),t)
                    m.tube('seta',[p,p+Vector((s*RNG.uniform(.03,.065),RNG.uniform(-.02,.02),.04))],[.0025,.0003],'ivory',5)
        m.curve('pedipalp',[(s*.1,.39,.30),(s*.18,.56,.22),(s*.12,.61,.12)],[.037,.03,.015],'bark',n=10)
        m.curve('chelicera',[(s*.06,.41,.31),(s*.075,.52,.19),(s*.04,.51,.12)],[.035,.025,.002],n=10)
    for i in range(8):
        a=PI*(i/7-.5)
        m.ellipsoid('ocellus',(.11*math.sin(a),.405,.41+.028*math.cos(a)),(.014,.015,.014),'eye',12,8)
    if hairy:
        for j in range(180):
            a=RNG.random()*2*PI;t=RNG.uniform(.15,1.45)
            p=Vector((.27*math.sin(t)*math.cos(a),-.31+.39*math.sin(t)*math.sin(a),.35+.26*math.cos(t)))
            m.tube('abdominal_seta',[p,p+Vector((.045*math.cos(a),.045*math.sin(a),.05))],[.002,.0003],'ivory',5)

def butterfly(m,color='blue',swallow=False):
    m.ellipsoid('thorax',(0,.08,.035),(.038,.105,.043),'chitin',24,14)
    m.ellipsoid('abdomen',(0,-.10,.027),(.033,.13,.028),'chitin',24,14)
    m.ellipsoid('head',(0,.20,.04),(.042,.038,.034),'chitin',24,14)
    for s in (-1,1):
        m.curve('clubbed_antenna',[(s*.02,.22,.04),(s*.06,.34,.04),(s*.11,.40,.04)],[.005,.003,.003],n=6)
        m.ellipsoid('antenna_club',(s*.11,.40,.04),(.009,.019,.009),'chitin',12,8)
        for j in range(3):m.tube('folded_leg',[(s*.02,.12-j*.035,.01),(s*.06,.12-j*.07,-.01),(s*.09,.08-j*.07,0)],.003,n=6)
        for upper in (True,False):
            if upper: outline=[(.03,.1),(.13,.28),(.40,.54),(.60,.55),(.67,.40),(.65,.21),(.54,.07),(.22,-.08),(.04,-.07)]
            else: outline=[(.035,-.015),(.26,.03),(.51,-.07),(.52,-.22),(.42,-.40),(.25,-.47),(.10,-.36),(.04,-.17)]
            if swallow and not upper:outline[5:5]=[(.38,-.47),(.30,-.65),(.29,-.43)]
            raw=[Vector((s*x,y,.017+.022*abs(x))) for x,y in outline]
            outline=[]
            for j in range(len(raw)):
                p0,p1,p2,p3=[raw[k%len(raw)] for k in (j-1,j,j+1,j+2)]
                for k in range(4):
                    t=k/4
                    outline.append(.5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
            root=outline[0];n=len(outline)
            # Concentric perimeter rings form dark margins, coloured wing fields,
            # and irregular pale submarginal patches, without image dependencies.
            centre=sum(outline,Vector())/n
            for a,b,mat in [(0,.72,color),(.72,.82,'chitin'),(.82,.91,color),(.91,1,'chitin')]:
                inner=[centre+(v-centre)*a for v in outline];outer=[centre+(v-centre)*b for v in outline]
                m.mesh('wing_scale_field',inner+outer,[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],mat)
            for j in range(1,n,3):
                p=outline[j]
                mid=centre*.5+p*.5+Vector((0,0,.002))
                m.curve('wing_vein',[root,mid,p],.0025,'chitin',n=5)
                spot=centre+(p-centre)*.86+Vector((0,0,.003))
                m.ellipsoid('submarginal_spot',spot,(.012,.018,.0015),'cream',12,6)
            if not upper:
                for rad,mat in [(.068,'chitin'),(.046,'orange'),(.022,'eye'),(.008,'cream')]:
                    m.ellipsoid('eyespot',(s*.33,-.23,.043),(rad,rad,.0012),mat,24,8)

def mantid(m):
    m.ellipsoid('abdomen',(0,-.38,.48),(.13,.45,.095),'leaf',32,18)
    for i in range(7):m.curve('abdominal_segment',[(-.10,-.7+i*.08,.5),(0,-.72+i*.08,.58),(.10,-.7+i*.08,.5)],.008,'leafLight',n=6)
    m.tube('elongate_prothorax',[(0,.02,.48),(0,.48,.67),(0,.73,.83)],[.075,.055,.065],'leaf',18)
    m.mesh('triangular_head',[(-.19,.72,.90),(.19,.72,.90),(0,.86,.72),(-.14,.77,.98),(.14,.77,.98),(0,.90,.82)],[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],'leaf')
    for s in (-1,1):
        m.ellipsoid('compound_eye',(s*.16,.77,.92),(.065,.065,.074),'leafLight',24,16)
        m.curve('filiform_antenna',[(s*.055,.8,.98),(s*.13,1.18,1.11),(s*.18,1.52,1.1)],[.008,.004,.001],n=6)
        # Raptorial forelegs: long coxa, thick spined femur, folded tibia.
        a=(s*.055,.51,.68);b=(s*.20,.83,.58);c=(s*.25,1.02,.83);d=(s*.18,.79,.73)
        m.bone('fore_coxa',a,b,.028,'leaf');m.bone('raptorial_femur',b,c,.050,'leaf');m.bone('folded_tibia',c,d,.021,'leaf')
        for j in range(9):
            p=Vector(b).lerp(Vector(c),j/9)
            m.tube('femoral_spine',[p,p+Vector((-s*.03,.025,.038))],[.012,.001],'chitin',6)
        for j in range(2):
            m.tube('walking_leg',[(s*.06,.1-j*.25,.49),(s*.35,.20-j*.56,.48),(s*.51,.29-j*.65,.05),(s*.57,.36-j*.65,.015)],[.025,.023,.009,.002],'leaf',10)
        m.leaf('folded_forewing',(s*.035,.07,.59),(s*.06,-.79,.54),.07,'leafLight')

def scorpion(m):
    for j in range(7):m.ellipsoid('mesosomal_tergite',(0,.10-j*.085,.20),(.18-.008*j,.061,.10),'bark',24,12,.04)
    m.ellipsoid('prosoma',(0,.30,.2),(.17,.16,.1),'bark',28,16,.04)
    tail=[(0,-.42,.2),(0,-.60,.3),(0,-.72,.51),(0,-.65,.77),(0,-.43,.88),(0,-.25,.78)]
    for j in range(5):m.bone('metasomal_segment',tail[j],tail[j+1],.055-j*.004,'bark')
    m.ellipsoid('telson',(0,-.24,.77),(.055,.08,.054),'bark',20,14)
    m.curve('sting',[(0,-.20,.77),(0,-.13,.68),(0,-.15,.62)],[.025,.014,.001],'chitin',n=10)
    for s in (-1,1):
        for j in range(4):m.tube('walking_leg',[(s*.12,.29-j*.12,.2),(s*.31,.43-j*.2,.23),(s*.46,.4-j*.22,.015)],[.021,.016,.003],'bark',8)
        m.bone('pedipalp', (s*.13,.38,.22),(s*.32,.64,.2),.04,'bark')
        m.ellipsoid('chela_hand',(s*.33,.72,.2),(.105,.15,.075),'bark',24,14)
        for d in (-1,1):m.curve('chela_finger',[(s*.33+d*.065,.78,.2),(s*.33+d*.065,.98,.2),(s*.33,1.01,.2)],[.034,.019,.001],'bark',n=10)

def ammonite(m,r=.35):
    pts=[];rs=[]
    for i in range(300):
        t=i/299;angle=t*PI*5.1;radius=r*(.08+.92*t*t)
        pts.append((radius*math.cos(angle),radius*math.sin(angle),.12))
        rs.append(radius*.22+.008)
    m.tube('planispiral_shell',pts,rs,'boneLight',14)
    for i in range(18,299,4):
        c=Vector(pts[i]);tangent=(Vector(pts[i+1])-Vector(pts[i-1])).normalized()
        side=tangent.cross(Vector((0,0,1)))
        m.tube('shell_rib',[c+side*rs[i]*math.cos(a)+Vector((0,0,rs[i]*math.sin(a))) for a in [k*2*PI/16 for k in range(17)]],.004,'bone',6)

def millipede(m):
    for j in range(26):
        x=.12*math.sin(j*.10);y=.48-j*.039;z=.075
        m.ellipsoid('diplosegment',(x,y,z),(.07,.034,.058),'bark',18,10)
        for s in (-1,1):
            for d in (-1,1):m.tube('paired_segment_legs',[(x+s*.05,y+d*.009,z),(x+s*.085,y-.02+d*.009,.028),(x+s*.11,y-.03+d*.009,.012)],[.006,.004,.001],'orange',5)
    m.ellipsoid('head',(0,.54,.075),(.061,.055,.055),'chitin',20,12)
    for s in (-1,1):m.curve('antenna',[(s*.035,.57,.08),(s*.065,.64,.08),(s*.09,.66,.06)],[.006,.004,.001],n=6)

def fern(m,centre=(0,0,0),scale=1):
    old=m.scope(centre,scale)
    for i in range(9):
        a=i*2*PI/9
        end=Vector((math.cos(a)*.56,math.sin(a)*.56,.34+RNG.random()*.2))
        m.curve('fern_rachis',[(0,0,0),end*.45+Vector((0,0,.35)),end],.012,'leafLight',n=6)
        side=Vector((-math.sin(a),math.cos(a),0))
        for j in range(1,12):
            t=j/12;p=end*t+Vector((0,0,.32*math.sin(PI*t)))
            for s in (-1,1):m.leaf('fern_pinna',p,p+side*s*.15*math.sin(PI*t)+end*.08,.019,'leaf')
    m.restore(old)

def habitat(m,w,d,style='forest'):
    # Sculpted substrate stays inside the shell-provided enclosure.
    m.ellipsoid('substrate',(0,0,.055),(w*.47,d*.47,.045),'earth',56,24,.015)
    for i in range(18):
        x=RNG.uniform(-w*.42,w*.42);y=RNG.uniform(-d*.42,d*.42)
        m.ellipsoid('pebble',(x,y,.06),(RNG.uniform(.025,.10),.06,.045),'stone',14,10,.12)
    for i in range(23):
        x=RNG.uniform(-w*.42,w*.42);y=RNG.uniform(-d*.42,d*.42)
        m.leaf('fallen_leaf',(x,y,.06),(x+.16,y+.13,.07),.045,'bark' if i%3 else 'leaf')
    if style!='aquatic':
        m.curve('fallen_branch',[(-w*.35,-d*.23,.08),(0,0,.17),(w*.31,d*.32,.28)],[.095,.075,.04],'bark',n=18)
        for i in range(5):
            t=i/5;m.curve('bark_ridge',[(-w*.33,-d*.20+t*.1,.1),(0,t*.08,.22),(w*.29,d*.30+t*.06,.3)],.007,'stone',n=5)
    if style=='forest':
        fern(m,(-w*.25,d*.22,.05),.5)
        fern(m,(w*.25,-d*.22,.05),.4)

def microscope(m):
    m.ellipsoid('cast_base',(0,0,.04),(.22,.28,.045),'white',40,20)
    m.curve('cast_arm',[(0,-.14,.07),(0,-.19,.32),(0,-.11,.55),(0,.04,.61)],[.07,.06,.05,.055],'white',n=20)
    m.tube('body_tube',[(0,.04,.55),(0,.13,.71)],[.055,.045],'white',24)
    m.tube('eyepiece',[(0,.13,.71),(0,.16,.77)],[.039,.041],'chitin',24)
    m.tube('eyepiece_glass',[(0,.16,.771),(0,.16,.773)],[.030,.030],'blue',24)
    for x in (-.035,0,.035):m.tube('objective_lens',[(x,.04,.54),(x,.055,.43)],[.017,.014],'steel',18)
    m.mesh('stage',[(-.13,-.10,.28),(.13,-.10,.28),(.13,.17,.28),(-.13,.17,.28),(-.13,-.10,.30),(.13,-.10,.30),(.13,.17,.30),(-.13,.17,.30)],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'chitin')
    for s in (-1,1):
        m.tube('focus_knob',[(s*.05,-.13,.37),(s*.12,-.13,.37)],[.037,.037],'chitin',24)
        m.tube('stage_clip',[(s*.07,-.03,.312),(s*.07,.10,.312)],[.009,.009],'steel',8)
    m.ellipsoid('illuminator',(0,.06,.095),(.05,.05,.025),'steel',24,12)
    m.ellipsoid('condenser',(0,.06,.23),(.045,.045,.032),'steel',24,12)
    m.mesh('glass_slide',[(-.055,-.035,.314),(.055,-.035,.314),(.055,.07,.314),(-.055,.07,.314)],[(0,1,2,3)],'membrane')

def snail(m):
    m.ellipsoid('muscular_foot',(0,.04,.025),(.10,.20,.027),'bark',24,14)
    pts=[];rs=[]
    for j in range(220):
        t=j/219;a=t*PI*6;rad=.012+.075*t
        pts.append((rad*math.cos(a),rad*math.sin(a),.21-.15*t))
        rs.append(.009+.033*t)
    m.tube('helical_gastropod_shell',pts,rs,'gold',14)
    for s in (-1,1):m.curve('tentacle',[(s*.035,.19,.04),(s*.065,.25,.09),(s*.085,.28,.12)],[.008,.005,.002],'bark',n=6)
