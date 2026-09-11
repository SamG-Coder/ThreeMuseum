# Collection validation — 11 September 2026

This report supplements the original architectural-edition test report.

## Executed

- Actual Blender 5.2.1 LTS reference generation via Blender Lab MCP: 1,031 shell pieces and 30 exhibit origins.
- Actual static GLB export and saved editable master.
- All 30 installed GLBs parsed through Three.js GLTFLoader. Embedded resources, finite geometry, vertex colours and installation envelopes checked.
- Triangle-level sauropod cross-passage clearance: approximately **3.998 m**, above the design minimum of 2.8 m. This is a static geometry check, not an animation sweep.
- Blender renders of every exhibit; selected large specimens also inspected from additional orthographic directions.
- Browser smoke test: all **30 of 30** installations reported loaded. The arrival viewpoint displayed **60 fps** on the current machine. This is a momentary local observation, not a hardware-independent benchmark.
- No captured browser console errors or warnings during the initial live smoke check.

Raw geometry measurements and final collection size are in `validation/glb-collection.json`. Blender build measurements are in `validation/specimen-build.json`. MCP requests and responses are in `validation/blender-mcp.jsonl`. Per-exhibit rendered PNGs are named `validation/specimen-<ID>.png`.

## Scope and limits

The original procedural specimens retain simplified anatomical surfaces and approximate proportions. Scientific accuracy has not been independently reviewed. F01 uses the credited Smithsonian model; its source pose and dimensions were preserved. The collection is static. Imported meshes do not add automatic collision; existing display fixtures provide the walking barriers. The original passage/navigation checks do not constitute an accessibility or structural certification.

No phone, physical touch device, Safari or low-end GPU performance test was performed. No public deployment was made. No skeleton rigging or animation sweep was tested because no specimen animations were authored.

## Final handoff checks

- Architecture/navigation suite: 22 tests passed.
- Static website build: completed successfully.
- Final exported assets: 95,138,920 bytes and 3,424,206 triangles across 30 GLBs.
- Complete Blender collection audit: all 30 MODEL collections remain within their assigned envelopes.
- Live feature-gallery inspection confirmed the Triceratops, mounting supports and nearby exhibit prompt render together.

