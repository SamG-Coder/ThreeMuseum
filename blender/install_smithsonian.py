import bpy
import runpy
from pathlib import Path
P=Path('D:/ThreeMuseum')
# Preserve the replaced reconstruction as a hidden design study.
archive=bpy.data.collections.new('STUDY_Original_Triceratops')
bpy.context.scene.collection.children.link(archive)
for ob in list(bpy.data.collections['MODEL_F01'].objects):
    bpy.data.collections['MODEL_F01'].objects.unlink(ob);archive.objects.link(ob)
archive.hide_render=True;archive.hide_viewport=True
runpy.run_path(str(P/'blender/build_collection.py'),init_globals={'IDS':['F01']})
runpy.run_path(str(P/'blender/render_specimen.py'),init_globals={'ID':'F01'})
qa=bpy.data.collections.get('MODEL_SCAN_QA')
if qa:
    qa.name='STUDY_Scan_orientation';qa.hide_render=True;qa.hide_viewport=True
# Keep the downloaded print study in its own source file, outside the main museum.
study=bpy.data.collections.get('SOURCE_Naturalis_Triceratops_print_parts')
if study:
    target=P/'blender/sources/Naturalis_Print_Study.blend'
    if not target.exists():bpy.data.libraries.write(str(target),{study},fake_user=True)
    for ob in list(study.objects):
        me=ob.data;bpy.data.objects.remove(ob,do_unlink=True)
        if me.users==0:bpy.data.meshes.remove(me)
    bpy.data.collections.remove(study)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'blender/ThreeMuseum_Collection.blend'))
result={'installed':'F01','source':'Smithsonian Institution, CC0','source_units_preserved':True}
