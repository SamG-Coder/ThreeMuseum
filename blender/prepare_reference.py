"""Build and save the museum reference in a fresh Blender MCP session."""
import bpy
import runpy
from pathlib import Path

PROJECT = Path('D:/ThreeMuseum')
if bpy.data.filepath:
    raise RuntimeError('Use a fresh Blender session; an existing file is open.')
# Preserve startup objects in an excluded collection, outside the museum model.
for col in bpy.context.scene.collection.children:
    col.hide_render = True
    col.hide_viewport = True
runpy.run_path(str(PROJECT / 'blender/build_shell.py'), run_name='__main__')
target = PROJECT / 'blender/ThreeMuseum_Collection.blend'
if target.exists():
    raise FileExistsError(target)
bpy.ops.wm.save_as_mainfile(filepath=str(target))
result = {'file': str(target), 'objects': len(bpy.data.objects),
          'slots': len([c for c in bpy.data.collections if c.name.startswith('MODEL_')]),
          'blender': bpy.app.version_string}
