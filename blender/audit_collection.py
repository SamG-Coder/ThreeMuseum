"""Measure every installed collection in the current Blender MCP session."""
import bpy, json
from pathlib import Path
from mathutils import Vector
P=Path('D:/ThreeMuseum')
entries=json.loads((P/'public/architecture.json').read_text())['exhibits']
report=[]
for e in entries:
    id=e['id']; obs=list(bpy.data.collections['MODEL_'+id].objects)
    pp=[ob.matrix_world@Vector(v) for ob in obs for v in ob.bound_box]
    lo=[min(v[i] for v in pp) for i in range(3)]
    hi=[max(v[i] for v in pp) for i in range(3)]
    x,y,z=e['position']; w,h,d=e['envelope']
    within=lo[0]>=x-w/2-.02 and hi[0]<=x+w/2+.02 and lo[1]>=-z-d/2-.02 and hi[1]<=-z+d/2+.02 and lo[2]>=y-.02 and hi[2]<=y+h+.02
    assert within, id
    report.append({'id':id,'dimensions_xyz':[hi[0]-lo[0],hi[2]-lo[2],hi[1]-lo[1]],'within_envelope':within,'vertices':sum(len(ob.data.vertices) for ob in obs),'bytes':(P/'public/models'/f'{id}.glb').stat().st_size})
(P/'docs/validation/specimen-build.json').write_text(json.dumps(report,indent=2))
result={'audited':len(report),'all_within_envelope':all(e['within_envelope'] for e in report)}
