import runpy
for name,view in [('side',(2,0,0)),('top',(0,0,2)),('front',(0,2,0))]:
    runpy.run_path('D:/ThreeMuseum/blender/render_specimen.py',init_globals={'ID':'F01','VIEW':view,'SUFFIX':'-'+name})
result={'rendered':['side','top','front']}
