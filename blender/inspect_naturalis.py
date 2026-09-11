import bpy
import zipfile
from pathlib import Path
from mathutils import Vector
P=Path('D:/ThreeMuseum/blender/sources')
with zipfile.ZipFile(P/'naturalis-triceratops.zip') as z:
    for name in z.namelist():
        if name.lower().endswith('.stl'):
            target=P/Path(name).name
            if not target.exists(): target.write_bytes(z.read(name))
col=bpy.data.collections.new('SOURCE_Naturalis_Triceratops_print_parts')
bpy.context.scene.collection.children.link(col)
records=[]
for path in P.glob('*.stl'):
    bpy.ops.wm.stl_import(filepath=str(path))
    obj=bpy.context.object
    for c in list(obj.users_collection): c.objects.unlink(obj)
    col.objects.link(obj)
    points=[obj.matrix_world@Vector(c) for c in obj.bound_box]
    records.append({'name':obj.name,'vertices':len(obj.data.vertices),
      'bounds': [[min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)]]})
col.hide_render=True
col.hide_viewport=True
result={'parts':records}
