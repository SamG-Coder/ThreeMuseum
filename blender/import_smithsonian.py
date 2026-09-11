import bpy
from mathutils import Vector
bpy.ops.wm.stl_import(filepath='D:/ThreeMuseum/blender/sources/smithsonian-triceratops-150k.stl')
ob=bpy.context.object
col=bpy.data.collections.new('SOURCE_Smithsonian_CC0')
bpy.context.scene.collection.children.link(col)
for c in list(ob.users_collection):c.objects.unlink(ob)
col.objects.link(ob)
ob.name='Smithsonian_Triceratops_source'
pp=[ob.matrix_world@Vector(c) for c in ob.bound_box]
result={'name':ob.name,'vertices':len(ob.data.vertices),'bounds':[[min(p[i] for p in pp) for i in range(3)],[max(p[i] for p in pp) for i in range(3)]]}
col.hide_render=True;col.hide_viewport=True
