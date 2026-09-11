"""ThreeMuseum reference scene builder. Run from Blender's Scripting workspace.

Save this script in its supplied blender/ folder. It reads ../public/architecture.json.
Only the collection named ThreeMuseum_Reference is replaced on rerun. User MODEL_*
collections are preserved. No specimen, animal, fossil or botanical models are created.
Blender execution was not available in the delivery environment; see TEST_REPORT.md.
"""
import bpy
import json
import math
from pathlib import Path
from mathutils import Vector

PROJECT = Path(__file__).resolve().parent.parent
DATA = json.loads((PROJECT / 'public' / 'architecture.json').read_text(encoding='utf-8'))
REFERENCE_NAME = 'ThreeMuseum_Reference'
# Proper rotation: Three (X,Y,Z) -> Blender (X,-Z,Y), metre for metre.
def point(p):
    return Vector((p[0], -p[2], p[1]))

def collection(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent.children if parent else bpy.context.scene.collection.children).link(c)
    return c

def remove_collection(c):
    for child in list(c.children):
        remove_collection(child)
    for obj in list(c.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(c)

old = bpy.data.collections.get(REFERENCE_NAME)
if old:
    remove_collection(old)
root = collection(REFERENCE_NAME)
geometry = collection('Building_and_fixtures', root)
roof = collection('Ceilings_and_roofs', root)
anchors = collection('Exhibit_origins', root)
guides = collection('Exhibit_envelopes_DO_NOT_EXPORT', root)
content = bpy.data.collections.get('ThreeMuseum_Exhibit_Content')
if not content:
    content = collection('ThreeMuseum_Exhibit_Content')

PALETTE = {
    'plaster':'eee9dc','concrete':'969f9b','paving':'a2aaa6','joint':'737d77',
    'terrazzo':'c7c4b7','limestone':'d4c6ae','sand':'b7a78e','oak':'ad8b62',
    'oakDark':'776448','charcoal':'282f31','bronze':'bc9360','linen':'e2dcc9',
    'soil':'433e33','carpet':'4d5a5c','glass':'c1e1d9','skylight':'d6e6e2',
    'light':'fff1cd','screen':'172527'
}
materials = {}
for name, value in PALETTE.items():
    material = bpy.data.materials.get('TM_' + name) or bpy.data.materials.new('TM_' + name)
    rgb = tuple(int(value[i:i+2], 16)/255 for i in (0,2,4))
    material.diffuse_color = (*rgb, .16 if name in ('glass','skylight') else 1)
    material.use_nodes = True
    shader = material.node_tree.nodes.get('Principled BSDF')
    if shader:
        shader.inputs['Base Color'].default_value = (*rgb, 1)
        shader.inputs['Roughness'].default_value = .3 if name=='bronze' else .65
        shader.inputs['Metallic'].default_value = .7 if name=='bronze' else 0
        if name in ('glass','skylight'):
            shader.inputs['Alpha'].default_value = .16
            if hasattr(material, 'surface_render_method'):
                material.surface_render_method = 'DITHERED'
            elif hasattr(material, 'blend_method'):
                material.blend_method = 'BLEND'
    materials[name] = material

def mesh_object(name, vertices, faces, target, mat=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([point(v) for v in vertices], [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    target.objects.link(obj)
    if mat:
        mesh.materials.append(materials[mat])
    return obj

RAMP_FACES = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
BOX_FACES = [tuple(reversed(face)) for face in RAMP_FACES]
def box_vertices(p, size, yaw=0):
    x,y,z=p;w,h,d=(v/2 for v in size);c,s=math.cos(yaw),math.sin(yaw)
    vs=[]
    for vx,vy,vz in [(-w,-h,-d),(w,-h,-d),(w,-h,d),(-w,-h,d),(-w,h,-d),(w,h,-d),(w,h,d),(-w,h,d)]:
        vs.append((x+c*vx+s*vz,y+vy,z-s*vx+c*vz))
    return vs

for item in DATA['pieces']:
    name = item['id'];kind = item['kind'];p=item['position'];size=item['size']
    target=roof if item.get('section')=='roof' else geometry
    if kind=='ramp':
        x1,x2,z1,z2,y1,y2=(item[k] for k in ('x1','x2','z1','z2','y1','y2'))
        vertices=[(x1,y1-.2,z1),(x2,y1-.2,z1),(x2,y2-.2,z2),(x1,y2-.2,z2),
                  (x1,y1,z1),(x2,y1,z1),(x2,y2,z2),(x1,y2,z2)]
        obj=mesh_object(name,vertices,RAMP_FACES,target,item['material'])
    elif kind in ('cylinder','beam'):
        if kind=='beam':
            start,end=Vector(p),Vector(item['end']);radius=size[0]
        else:
            start=Vector((p[0],p[1]-size[1]/2,p[2]));end=Vector((p[0],p[1]+size[1]/2,p[2]));radius=size[0]/2
        axis=(end-start).normalized();other=Vector((0,1,0)) if abs(axis.y)<.9 else Vector((1,0,0))
        u=axis.cross(other).normalized();v=axis.cross(u);n=12
        vertices=[tuple(c+radius*(math.cos(t*2*math.pi/n)*u+math.sin(t*2*math.pi/n)*v)) for c in (start,end) for t in range(n)]
        faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        obj=mesh_object(name,vertices,faces,target,item['material'])
    else:
        obj=mesh_object(name,box_vertices(p,size,item.get('yaw',0)),BOX_FACES,target,item['material'])
    obj['three_museum_piece_id']=name

for e in DATA['exhibits']:
    empty=bpy.data.objects.new('ANCHOR_'+e['id'],None);anchors.objects.link(empty)
    empty.location=point(e['position']);empty.empty_display_type='PLAIN_AXES';empty.empty_display_size=.6
    empty['exhibit_id']=e['id'];empty['subject']=e['subject'];empty['width_height_depth_m']=e['envelope']
    empty['export_path']='public/models/'+e['id']+'.glb'
    w,h,d=e['envelope'];centre=[e['position'][0],e['position'][1]+h/2,e['position'][2]]
    guide=mesh_object('ENVELOPE_'+e['id'],box_vertices(centre,(w,h,d)),BOX_FACES,guides)
    guide.display_type='WIRE';guide.hide_render=True;guide.hide_select=True
    if not bpy.data.collections.get('MODEL_'+e['id']):
        collection('MODEL_'+e['id'],content)

scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene['ThreeMuseum']='Original Melbourne Museum-inspired shell; not an as-built replica.'
scene['ThreeMuseum_source']=str(PROJECT)
# Leave the roof hidden so the entire reference layout can be worked on immediately.
roof.hide_viewport=True
for area in bpy.context.screen.areas if bpy.context.screen else []:
    if area.type=='VIEW_3D':
        area.spaces.active.clip_end=500
        area.spaces.active.region_3d.view_distance=105
        area.spaces.active.region_3d.view_location=Vector((0,8,0))
print('ThreeMuseum reference built: %s pieces, %s origins. Save As a new .blend file.' % (len(DATA['pieces']),len(DATA['exhibits'])))
