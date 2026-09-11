import bpy
import math
import sys
import runpy
from pathlib import Path
from mathutils import Vector,Matrix
P=Path('D:/ThreeMuseum');sys.path.insert(0,str(P/'blender'))
from specimen_geometry import Model
source=bpy.data.objects['Smithsonian_Triceratops_source']
col=bpy.data.collections.get('MODEL_SCAN_QA') or bpy.data.collections.new('MODEL_SCAN_QA')
if col.name not in bpy.context.scene.collection.children:bpy.context.scene.collection.children.link(col)
for ob in list(col.objects):bpy.data.objects.remove(ob,do_unlink=True)
rotation=Matrix.Rotation(math.pi/2,3,'Y')
vs=[rotation@v.co for v in source.data.vertices]
low=Vector(tuple(min(p[i] for p in vs) for i in range(3)))
high=Vector(tuple(max(p[i] for p in vs) for i in range(3)))
centre=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
m=Model('SCAN_QA')
m.mesh('Triceratops',[v-centre for v in vs],[tuple(p.vertices) for p in source.data.polygons],'boneLight')
m.finish(col,Vector((0,0,0)))
runpy.run_path(str(P/'blender/render_specimen.py'),init_globals={'ID':'SCAN_QA'})
result={'render':'D:/ThreeMuseum/docs/validation/specimen-SCAN_QA.png'}
