# ThreeMuseum collection edition

Built and installed on 11 September 2026 using Blender 5.2.1 LTS and the official Blender Lab MCP server. The local authoring session used MCP/stdio through `tools/blender-mcp-client.py`, connected to the installed Blender Lab add-on on `127.0.0.1:9876`. This did not use ThreeBrowser Studio.

## Delivered collection

All 30 model slots are populated. The editable master is `blender/ThreeMuseum_Collection.blend`; installed assets are the embedded GLBs under `public/models/`. `public/exhibits.json` persists the installation. The master contains the shell reference, 30 `MODEL_*` collections, and hidden source/design-study collections.

The original authored models are **interpretive reconstructions with approximate anatomy and proportions**. They are not photogrammetric scans, voucher specimens or scientifically validated skeletal reconstructions. The invertebrate cabinets and anatomy displays deliberately use enlarged models. All displays are static; there are no live animals, skeletal animations, working microscopes or interactive dissection simulations. The visitor cards identify these limits instead of presenting arbitrary display scale as a measured biological size.

The original model geometry, vertex colours and authoring scripts are covered by the project's MIT licence. These include D01–D09, B01–B16, F02, L01, L02 and C01. The F01 source below has its own public-domain dedication. Original shells, fixtures and scientific-reference photographs were not copied into the specimen exports.

## F01 — Smithsonian Triceratops

- Creator: **Smithsonian Institution**.
- Work: **Triceratops horridus Marsh, 1889**, 150k model.
- Download and licence record: [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Triceratops_horridus_Marsh_1889-150k_(Smithsonian_Institute).stl).
- Original collection record: [Smithsonian 3D](https://3d.si.edu/object/3d/triceratops-horridus-marsh-1889:d8c623be-4ebc-11ea-b77f-2e728ce88125).
- Licence: **CC0 1.0**, as documented on the file page. [CC0 dedication](https://creativecommons.org/publicdomain/zero/1.0/).
- Local source: `blender/sources/smithsonian-triceratops-150k.stl`.
- Changes: rigid coordinate rotation, bottom-centred translation, smooth shading, original fossil-coloured vertex material, and discrete museum mounting supports. No scaling or skeletal reposing was applied. The source pose is preserved. This model is not Melbourne Museum's Horridus specimen.

## References used for original studies

References informed the subject and broad external structures; they do not certify the generated meshes. No reference images were embedded in the exported assets.

- [Australian Museum — Beetles: Order Coleoptera](https://australian.museum/learn/animals/insects/beetles-order-coleoptera/): wing cases, appendages and external body-plan vocabulary.
- [Australian Museum — Garden Mantid](https://australian.museum/learn/animals/insects/garden-mantid/): mantid subject and reference appearance.
- [Australian Museum — Golden Orb Weaving Spiders](https://australian.museum/learn/animals/spiders/golden-orb-weaving-spiders/): web-study context. The installed spider is not assigned a local species identity.
- [Museums Victoria — Mamenchisaurus hochuanensis](https://collections.museumsvictoria.com.au/specimens/1046740): long-necked skeletal-display reference.
- [Natural History Museum — Protoceratops](https://www.nhm.ac.uk/discover/dino-directory/protoceratops.html): small ceratopsian context.
- [Blender Lab MCP source](https://projects.blender.org/lab/blender_mcp): server revision `ff54e4d8f6b09502f2f466189cca0e52b4a91643`, package 1.0.2, used with MCP Python SDK 1.30.0.

## Unused research download

The [Naturalis Triceratops printing package](https://www.naturalis.nl/en/education/primary_education/groups-5-to-8-3d-print-your-own-dinosaur) was downloaded and inspected as a possible source. It contains separated print-oriented parts. It was **not used in any installed GLB**, and no redistribution licence was established for it during this work. It remains under `blender/sources/` for local research, including `Naturalis_Print_Study.blend`; it is outside the website build. Do not describe it as an MIT or CC0 asset.

## Reproducible authoring

1. Open the master in Blender with the Blender Lab MCP add-on active. Alternatively, a fresh background session can be launched with `D:/Blender/blender.exe --background --online-mode --addons bl_ext.user_default.mcp --command blender_mcp --host 127.0.0.1 --port 9876`.
2. Use a Python environment containing the official Blender Lab `blender-mcp` package and its MCP dependency. The environment used here is `D:/tmp/threemuseum-blender-mcp-venv/Scripts/python.exe`.
3. The client accepts a tool name and structured JSON arguments; `--code-file` supplies a Python authoring file to the `execute_blender_code` MCP tool. It records requests and responses under `docs/validation/blender-mcp.jsonl`.
4. `blender/build_collection.py` rebuilds the generated specimen collections in a loaded master. It refuses to remove unrecognised user content. It uses the retained Smithsonian source object for F01. Keep that source object; a fresh build without it falls back to the original procedural study.
5. `node tools/validate-collection.mjs` parses all exported GLBs through Three.js, verifies embedded resources, finite geometry, vertex colours, envelope bounds and sauropod passage clearance. Add `--install` to persist the model URLs in the manifest.
6. `npm test` validates architecture/navigation; `npm run build` creates the static website in `dist/`.

The generator operates on the named collections and saves the master. Keep a saved copy before making substantial manual specimen edits and rerunning the generator. `prepare_reference.py` is for a fresh session only; it deliberately refuses to overwrite an existing saved master.
