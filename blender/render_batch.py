import runpy
IDS=globals().get('IDS',['B01','B02','B05','B06','B09','B13','B14','C01','D01','D02','D04','D07','D08','F01','L02'])
for id in IDS:
    runpy.run_path('D:/ThreeMuseum/blender/render_specimen.py',init_globals={'ID':id})
result={'rendered':IDS}
