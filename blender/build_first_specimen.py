import bpy
import sys
import runpy
from pathlib import Path
from mathutils import Vector
P=Path('D:/ThreeMuseum')
sys.path.insert(0,str(P/'blender'))
from specimen_geometry import Model, beetle
col=bpy.data.collections['MODEL_B09']
if len(col.objects): raise RuntimeError('B09 already contains authored content.')
m=Model('B09_Beetle_anatomy')
beetle(m,opened=True)
objects=m.finish(col,Vector((12.6,16,.3)))
runpy.run_path(str(P/'blender/export_static_exhibit.py'),init_globals={'EXHIBIT_ID':'B09'})
bpy.ops.wm.save_as_mainfile(filepath=str(P/'blender/ThreeMuseum_Collection.blend'))
result={'objects':len(objects),'vertices':sum(len(o.data.vertices) for o in objects),
        'glb_bytes':(P/'public/models/B09.glb').stat().st_size}
