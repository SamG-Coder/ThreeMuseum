# ThreeMuseum validation report

Delivery: 11 September 2026. This report separates implemented code, successful checks and checks that were not possible in the creation environment.

## Successful checks

| Check | Result |
|---|---|
| Dependency-free Node test suite | **22 passed, 0 failed** |
| Deterministic architectural compiler | Same inputs produce the same geometry records |
| Architecture data | 1,031 pieces, 311 collision solids, 30 empty model origins, 11 room records |
| Main entry and bug-gallery front portals | Tested for continuous clear passage |
| Entire suggested visitor loop | All sequential segments reached without blocked movement |
| Room entrances | All 11 spawn positions are unobstructed |
| Reading points | All 30 proposed points have clear standing volumes |
| Wall and display collision | Plinth blocking, facade blocking, sliding, and high-displacement subdivision checked |
| Ramp and overlook | Ascent, descent, landings, deck continuity and front guardrail checked |
| Teleport validation | Invalid, non-finite, out-of-bounds and excessively elevated points rejected |
| JavaScript syntax | All authored JS/MJS modules checked with Node |
| Blender Python syntax | Both Blender scripts compile under Python; no Blender execution implied |
| Static build | `npm run build` generated the relative-path `dist/` site successfully |
| HTTP server | Main HTML, modules, manifests, plan SVG and PDF returned 200 |
| Missing resources and hidden files | Missing GLB/runtime returned 404; hidden path returned 403; POST returned 405 |
| Static plan atlas | 30 exhibit cards, 11 room rows and 3 SVGs rendered; no horizontal overflow at 1440 or 390 px viewport width |
| Design booklet | 11 PDF pages rendered and visually inspected; text bounds checked for page overflow |

The static atlas browser check embedded its own HTML/SVG bytes rather than navigating over HTTP. The environment's managed browser blocks network navigation, including localhost. HTTP serving was checked separately using direct local requests. This is not described as an end-to-end 3D application test.

The first navigation pass detected an obstructed F02 reading point; it was moved behind the feature plinth. Additional portal checks led to adjusting the diversity wall cabinets so they do not obstruct the bug-gallery entrance. The overlook table was also checked to begin at the deck rather than extending its base down to ground level.

Raw results are under `docs/validation/`.

## Not run — do not interpret as passes

**Live Three.js/WebGL rendering:** the runtime could not be downloaded in the creation environment, and the managed browser blocks network navigation. Shader compilation, actual shadow quality, transparency ordering, camera composition and visual polish require a local browser run.

**Live GLB installation:** the code is present, but a real model was not loaded through the browser here. Decoder errors, animation playback, complex skin bounds, model fitting and exported-manifest persistence should be verified with the user's actual assets. The deliberately empty shipped scene makes no scientific-content claim.

**Blender execution:** Blender was unavailable. Reference generation and static GLB export were Python-syntax checked only. Test a small static exhibit before authoring a large collection against this workflow.

**Device and hardware performance:** no verified FPS results, mobile GPU budget, Safari test, physical touch-device test, WebGPU support or ray-tracing claim. The HUD displays actual current FPS when the local app runs; it is not a prerecorded benchmark.

**GitHub Pages deployment:** the workflow is supplied but was not run, and no repository was created or published.

## Local acceptance checklist

Run `npm install`, `npm test`, then `npm start`. Enter the museum in a current WebGL 2-capable desktop browser.

1. Check browser console/network panels for exceptions and unexpected missing resources. Empty model slots should not make requests for nonexistent GLBs.
2. Walk from the forecourt through arrival, into both subject wings and back through the court. Check signs at standing and lower eye heights.
3. Walk the full ramp up and down, cross both landings, approach the guardrail and inspect the comparison table on the overlook.
4. Press V to inspect the roof-off plan. Return to the visitor view and confirm the walking position was preserved.
5. Press B, preview a small self-contained GLB, exercise each transform, test envelope warnings and remove/reload the model.
6. Copy that GLB into `public/models`, export/replace the manifest and reload. Confirm the persisted installation uses the same transform.
7. Generate a Blender reference scene. Author/export a small static model to one slot and check its metre scale, handedness and bottom-centred origin.
8. Test the mobile layout, two simultaneous touch pointers, field of view and low graphics setting on the intended phone.
9. Recheck the complete walking route after adding large or animated exhibits. The initial envelope warning is not an animation sweep or accessibility audit.

The project is an editable architectural starting point, not a fully validated shipped exhibition.
