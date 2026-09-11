"""Render a named exhibit without changing its source placement."""
import bpy
import math
from pathlib import Path
from mathutils import Vector
P=Path('D:/ThreeMuseum')
ID=globals().get('ID','B09')
source=bpy.data.collections['MODEL_'+ID]
scene=bpy.data.scenes.get('Specimen_QA') or bpy.data.scenes.new('Specimen_QA')
for ob in list(scene.objects):bpy.data.objects.remove(ob,do_unlink=True)
points=[]
for ob in source.objects:
    points.extend([ob.matrix_world@Vector(c) for c in ob.bound_box])
low=Vector(tuple(min(p[i] for p in points) for i in range(3)))
high=Vector(tuple(max(p[i] for p in points) for i in range(3)))
centre=(low+high)/2
size=max(high-low)
for ob in source.objects:
    dup=ob.copy();scene.collection.objects.link(dup);dup.location-=centre
world=bpy.data.worlds.get('Specimen_Studio') or bpy.data.worlds.new('Specimen_Studio')
world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.07,.085,.10,1)
world.node_tree.nodes['Background'].inputs[1].default_value=.4;scene.world=world
camera=bpy.data.cameras.new('QA_Camera');cam=bpy.data.objects.new('QA_Camera',camera);scene.collection.objects.link(cam)
cam.location=Vector(globals().get('VIEW',(1.35,1.8,1.45)))*size
cam.rotation_euler=(-cam.location).to_track_quat('-Z','Y').to_euler()
camera.type='ORTHO';camera.ortho_scale=size*1.3;scene.camera=cam
for name,p,energy,color in [('Key',(1,1,2),1600,(1,.85,.68)),('Fill',(-1,.5,.8),1100,(.62,.79,1)),('Rim',(.2,-1,1.5),1800,(.8,1,.88))]:
    light=bpy.data.lights.new('QA_'+name,'AREA');light.energy=energy*size*size/35;light.shape='DISK';light.size=size
    ob=bpy.data.objects.new('QA_'+name,light);scene.collection.objects.link(ob);ob.location=Vector(p)*size
    ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler();light.color=color
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(P/'docs/validation'/('specimen-'+ID+globals().get('SUFFIX','')+'.png'))
bpy.ops.render.render(write_still=True,scene=scene.name)
result={'render':scene.render.filepath,'dimensions':list(high-low)}
