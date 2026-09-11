import runpy
runpy.run_path('D:/ThreeMuseum/blender/build_collection.py',init_globals={'IDS':['C01']+[f'D{i:02}' for i in range(1,10)]+['F01','F02']})
result={'batch':'palaeontology and courtyard'}
