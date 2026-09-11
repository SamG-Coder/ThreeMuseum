import bpy
import runpy
from pathlib import Path
P=Path('D:/ThreeMuseum')
runpy.run_path(str(P/'blender/build_collection.py'),init_globals={'IDS':['B01','B04','B11','B12','F01']})
for id in ['B01','B03','B04','B07','B08','B10','B11','B12','B15','B16','D03','D05','D06','D09','F01','F02','L01']:
    runpy.run_path(str(P/'blender/render_specimen.py'),init_globals={'ID':id,'VIEW':(1.6,2.2,1.0) if id=='F01' else (1.35,1.8,1.45)})
# The master opens on the reference scene; QA uses a separate scene.
scene=bpy.data.scenes['Scene']
bpy.context.window.scene=scene
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.clip_end=500
bpy.ops.wm.save_as_mainfile(filepath=str(P/'blender/ThreeMuseum_Collection.blend'))
result={'saved':str(P/'blender/ThreeMuseum_Collection.blend'),'rendered_remaining':17}
