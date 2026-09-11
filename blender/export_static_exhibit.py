"""Export one STATIC exhibit collection from the world-space Blender reference scene.
Set EXHIBIT_ID below, place only its specimen meshes under MODEL_<ID>, then run.
Supports static mesh/curve/text objects. For animated or skinned GLBs, use Blender's
normal glTF export workflow described in docs/BLENDER_HANDOFF.md instead.
Does not export the museum shell, envelope guides, label fixtures or camera.
"""
import bpy
import json
from pathlib import Path
from mathutils import Matrix, Vector
EXHIBIT_ID = globals().get('EXHIBIT_ID', 'D01')
PROJECT = Path(__file__).resolve().parent.parent
DATA = json.loads((PROJECT/'public'/'architecture.json').read_text(encoding='utf-8'))
entry = next((e for e in DATA['exhibits'] if e['id']==EXHIBIT_ID),None)
if entry is None:
    raise ValueError('Unknown EXHIBIT_ID: '+EXHIBIT_ID)
source=bpy.data.collections.get('MODEL_'+EXHIBIT_ID)
if not source:
    raise ValueError('Build the reference scene and populate MODEL_'+EXHIBIT_ID+' first.')
objects=[o for o in source.all_objects if o.type in {'MESH','CURVE','FONT','SURFACE','META'}]
if not objects:
    raise ValueError('The exhibit collection contains no static geometry.')
for o in objects:
    if o.animation_data or any(m.type=='ARMATURE' for m in o.modifiers):
        raise ValueError('Animated/skinned content requires the manual GLB workflow, not this static exporter.')
if bpy.context.object and bpy.context.object.mode!='OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
old_selected=list(bpy.context.selected_objects);old_active=bpy.context.view_layer.objects.active
x,y,z=entry['position'];origin=Vector((x,-z,y));translate=Matrix.Translation(-origin)
temporary=bpy.data.collections.new('TM_TEMP_EXPORT');bpy.context.scene.collection.children.link(temporary)
copies=[]
try:
    bpy.ops.object.select_all(action='DESELECT')
    deps=bpy.context.evaluated_depsgraph_get()
    for obj in objects:
        evaluated=obj.evaluated_get(deps)
        mesh=bpy.data.meshes.new_from_object(evaluated,depsgraph=deps)
        duplicate=bpy.data.objects.new(obj.name+'_export',mesh);temporary.objects.link(duplicate)
        duplicate.matrix_world=translate@obj.matrix_world;duplicate.select_set(True);copies.append(duplicate)
    bpy.context.view_layer.objects.active=copies[0]
    target=PROJECT/'public'/'models'/(EXHIBIT_ID+'.glb');target.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=str(target),export_format='GLB',use_selection=True,export_yup=True,export_animations=False)
    print('Wrote '+str(target)+'. Set this slot URL to models/'+EXHIBIT_ID+'.glb in public/exhibits.json.')
finally:
    for obj in copies:
        mesh=obj.data;bpy.data.objects.remove(obj,do_unlink=True)
        if mesh.users==0:bpy.data.meshes.remove(mesh)
    bpy.data.collections.remove(temporary)
    for obj in old_selected:
        if obj.name in bpy.data.objects:obj.select_set(True)
    if old_active and old_active.name in bpy.data.objects:bpy.context.view_layer.objects.active=old_active
