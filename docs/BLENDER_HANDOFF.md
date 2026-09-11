# Blender handoff

## Two supported authoring workflows

**World-space static authoring:** run `blender/build_shell.py` in Blender's Scripting workspace. It rebuilds the architecture from `public/architecture.json`, using real metre units, and adds wireframe installation volumes. The roof collection starts hidden. Add your specimen geometry to `MODEL_D01`, `MODEL_B05` or another named collection while keeping it in the right position in the reference building. Set `EXHIBIT_ID` in `export_static_exhibit.py` and run the exporter. It evaluates static meshes, converts their world-space positions to the chosen origin and writes `public/models/<ID>.glb`. The building and wire guides are not exported.

**Local-space animated authoring:** use a separate scene, or a clean asset collection near the origin, to author your insect, rig or skeletal reconstruction. Place the asset's bottom-centre at the origin and export selected content as an ordinary embedded GLB. Include its own armature and animation clips as appropriate. Do not use the static exporter for rigs or animated objects. The runtime plays imported animation clips; select/export a compatible set rather than unrelated actions that fight over the same joints.

The reference builder preserves existing `MODEL_*` collections when rerun; it replaces only its `ThreeMuseum_Reference` collection. It does not save over an existing `.blend`. Use Save As yourself. The static exporter writes the chosen `public/models/<ID>.glb`, replacing a file of the same name, so keep source assets under version control.

## Coordinate and unit contract

Three.js is Y-up. The plan's north is -Z. The Blender reference uses this proper rotation, not a mirror:

```text
Three point (x, y, z)  ->  Blender point (x, -z, y)
Blender point (x, y, z) -> Three point (x, z, -y)
```

Both sides use metres. Blender's glTF exporter performs the usual Z-up to Y-up conversion with `export_yup=True`; do not add another manual 90-degree rotation after using the supplied exporter.

An exhibit's `position` is its **bottom-centre origin**, not its geometric centre. `envelope` is width along X, height along Y, and depth along Z. Long dinosaur bays run north/south along Z. UI offsets are metres, UI rotations are degrees in XYZ order, and scale is a positive uniform multiplier. The corresponding Three.js transform applies local scale/rotation, then offset, under the translated exhibit anchor.

Examples:

- D01: origin `(-24, 0.30, -16)`, envelope `7 × 8.5 × 28 m`.
- B05: origin `(28.5, 0.65, -0.5)`, envelope `3.5 × 2.4 × 3 m`.
- D08: suspended origin `(-18, 7, -5)`; do not drop it to the floor.
- D09: origin `(-16, 3.28, -39.5)` because the display is on the +2.40 m overlook.

## Runtime installation

Open the museum, press B and select an ID. Choose a self-contained `.glb` no larger than the preview's 128 MB limit. Embedded PNG/JPEG textures are the simplest baseline. External texture references in a locally selected GLB are not resolved automatically. Draco meshes and KTX2 textures require decoder integration that is not included.

A loaded model receives the slot's offset, rotation and scale. Envelope warnings compare its world bounds against the reserved installation volume. The warning is advisory, not an automatic barrier, scientific scale validator, skinned-animation swept-volume test or structural check.

The Fit button resets transforms, computes a uniform fit and aligns the base. Use it for rough installation only. A dinosaur that ought to be 25 metres long should not be arbitrarily shrunk because a bay is wrong: adjust the plan or choose the correct asset.

A file preview is session-only. Persist it explicitly:

```json
{
  "id": "B05",
  "url": "models/B05.glb",
  "offset": [0, 0, 0],
  "rotation": [0, 0, 0],
  "scale": 1
}
```

Place the actual file in `public/models/B05.glb`. Export the full manifest using the panel button and replace `public/exhibits.json`. Model paths in that manifest are relative to `public/`. Keep the other entries in the manifest; unfilled entries retain `url: null`.

The geometry records in `architecture.json` are generated, not your model registry. Running `npm run plans` updates them but preserves an existing exhibit manifest. Never run `--reset` over your installed manifest without a backup.

## What to leave out of your specimen GLB

The shell already contains the floor, pedestal or table, cabinet frame, glass, reading-label fixture, lighting fixture and room architecture. Do not duplicate those in an exhibit export. Leave out cameras, sun lights, debug wires, the reference building and anchor empties unless an intentional local rig requires its own named root.

For habitat bays, the empty enclosure is provided. You supply animals, branches, litter, rocks, nest structures, water and any other dressing. For C01, you supply trees and planting; the stone bed is already built. For L02, the table is supplied, but the microscope is not.

## Keep circulation honest

The runtime does not turn arbitrary imported triangles into collision. Pedestal/case solids and building geometry already block walking. Large overhanging animals, doors or interactive features need deliberately authored extra collision boxes in `architecture.js` when required.

D01's split supports leave a seven-metre cross-passage. Keep its final belly and supports above the specified 2.8 m head-clear zone in that passage. Do not interpret the enclosing box as permission to fill every cubic metre. Check tails and suspended wings from both the floor and overlook.

Check animation extremes, not just the rest pose. A wing, antenna or tail must not swing through glass, a neighbouring exhibit or a walkway. Avoid layered transparent materials inside already glazed cases where possible.

## Practical content budgets — proposed, not measured performance claims

Start with a small test GLB before importing a detailed skeleton. Use material sharing, texture atlases and sensible geometry decimation; keep separate bones separate only when that separation is useful. Use original baked specimen atlases for distant pinned collections and closer geometry only where needed. A reasonable initial authoring target is 2K textures for most exhibits, with larger atlases reserved for demonstrable close-up needs. Profile the actual final scene and target devices rather than relying on a blanket polygon budget.

The supplied Blender scripts were Python-syntax checked, but Blender itself was unavailable in the creation environment. Verify the builder and a small static export locally before depending on the workflow for a large animated asset library.
