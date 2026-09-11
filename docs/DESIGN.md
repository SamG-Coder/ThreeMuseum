# ThreeMuseum — architectural design brief

## Intent

Create the experience of entering a thoughtfully designed natural-history museum, not an empty warehouse with rows of placeholder cubes. The design should be recognisable as a museum before a single skeleton or insect is installed: its entrance, sightlines, material changes, human-scale reading positions, changing ceiling heights and coherent display furniture provide that identity.

The user will supply specimen models in Blender. The architectural edition therefore excludes not only animals and skeletons, but also plant dressing, dioramas, water, microscopes, fossils, rocks and interpretive animations. Empty cases are intentional. The goal is an attractive, understandable framework for a collection rather than fake finished exhibits.

## Research and adaptation

The primary reference is Melbourne Museum. Its official Bugs Alive! description combines pinned collections, living enclosures, enlarged anatomy and a theatre [S1]. Dinosaur Walk emphasises moving around and under prehistoric mounts [S2-S3]. The separate Triceratops exhibition suggests giving one major specimen its own spatial identity [S4]. The official visitor map establishes a relationship between the natural-history areas and broader circulation [S5]. Denton Corker Marshall describes the building as a campus of elements [S6]. The museum's access information also makes sensory comfort a relevant design consideration [S7].

ThreeMuseum uses these ideas, not their exact geometry. No architectural survey, laser scan, dimensioned as-built plan or permission to reproduce proprietary exhibits was supplied. Every room dimension, window, roof, doorway, plinth and mounting allowance in this project is an original proposal. References establish the museum programme, not the authenticity of the new building.

## Spatial organisation

The main footprint is 76 × 72 m, running from X -38 to +38 and Z -43 to +29. A forecourt extends south toward Z +48. North is negative Z. Ground is Y=0. Deep Time Hall occupies the west side, a bright Light Court forms the central route, and smaller insect rooms occupy the east. A broad arrival hall sits to the south, with a lounge and teaching studio at its ends.

There are eleven named rooms. The smaller portions of Gallery Street connect the side spaces without being counted as additional rooms. The overlook is a raised part of Deep Time Hall rather than an independent exhibit room. The large footprint is deliberately easy to understand from the map; room teleport destinations prevent a visitor from having to traverse every metre to inspect the design.

The central court is 8 m wide before walls, rails and the planting-bed allowance. Its empty bed leaves walking routes on both sides. Doors connect it to the dinosaur and bug galleries at several points, so the museum offers choices rather than a single enforced sequence. Flush bronze route inlays identify circulation without becoming raised trip-like collision geometry.

## Arrival and orientation

The forecourt has paving joints, seating, bollards, glazing and a broad projecting canopy. The main opening is 8 m wide. Inside, reception is placed to one side of the walking line. A timber feature wall frames the desk; it is collision-bearing rather than a surface visitors can walk through. Strong room names sit above the entrances, and the Light Court is visible ahead.

A visitor can choose dinosaurs to the left, insects to the right, or the central route ahead. The application begins with a restrained welcome composition and moves to a standing visitor viewpoint when entered. The scene contains no reception staff, crowds or animated guides.

## Deep Time Hall

The hall is 34 × 52 m with an 11.8 m roof datum. A long northlight and exposed beams establish its larger scale. Oak floor finishes contrast with the pale circulation floors, while limestone display islands keep the future bones visually distinct from their supports.

D01 is the principal long-necked mount allowance. Its envelope is 7 × 8.5 × 28 m. That is a design allocation, not a claim about a particular specimen. Two low support islands leave a 7 m cross-passage. A future asset must retain head clearance above 2.8 m in that passage; its neck, belly, rigging and tail cannot simply fill the whole box.

A separate predator bay, an armoured-dinosaur position, a smaller dinosaur mount, comparison tables and a later-megafauna position provide changes in viewing distance and scale. A suspended pterosaur allowance sits well above floor circulation. This does not make pterosaurs dinosaurs, and the future scientific labels must distinguish the subjects and their time periods.

The western ramp rises 2.4 m through three 12 m slopes, each at 1:15, separated by two 3 m landings. Its total run is 42 m and design width is 3.3 m. The overlook lets the final installation be read across the hall without adding a mandatory staircase. It has benches, a comparison table and guardrails. These proportions are virtual-world design choices, not a declaration of code compliance.

## Four bug galleries

**Cabinet of Diversity** begins with shallow framed collection displays and island comparison furniture. Wall cabinets are positioned beside, not across, the arrival opening. They are physically hollow so a future model can be installed inside them. A large record-breaker vitrine becomes the central object without occupying the entrance.

**Living Habitats** uses more enclosure-like fixtures and a central colony position. The visual narrative should become ecological once populated, but the architectural build contains no nest, foliage, litter, water or living organisms. Its cases are not intended to describe working animal husbandry or containment systems.

**Small Worlds Lab** is the teaching-oriented anatomy room. A central enlarged-body allowance is supported by smaller comparison furniture and a wall sequence. Enlarged models should be labelled with their presentation scale. The room is intended to explain structure and change without relying on dense walls of text.

**The Eight-legged Room** gives arachnids their own clear interpretive identity. The visual approach is calm observation rather than horror. The tarantula-themed enclosure is not represented as a certified quarantine facility. Any local-species claims, risk information or scientific statements must be checked when actual labels are written.

All four rooms use a 5.6 m ceiling datum, warm case illumination and timber acoustic-fin imagery. Actual sound absorption is not simulated. Doors link the rooms into a loop and back to the central court.

## Last Giants, learning and rest

Last Giants is a 17 × 20 m feature room with an 8 m roof datum. It has a 6.5 × 5 × 11 m main model allowance and a second shallow preparation/evidence position. The intention is to give a future Triceratops model a calmer walk-around setting. The design is not a reproduction of Horridus or the museum's immersive media.

Big Questions Theatre is a level-floor shell with bench rows, aisles and an empty screen. No film or audio is supplied. Discovery Studio contains a handling table, a microscope-table allowance and spare working space; the scientific equipment is still a modelling task. The lounge supplies a break from viewing, not a decorative waiting area filled with inaccessible furniture.

C01 is an empty planting installation in the Light Court. It provides the possibility of a living visual centre later without including placeholder trees. This is a light-court interpretation, not a model of the actual Forest Gallery.

## Fixture grammar

The building uses a small family of fixtures: low plinths, split support islands, horizontal tables, framed wall cabinets, island vitrines, habitat enclosures and suspended mounting allowances. Their scale, material and label treatment are consistent across rooms. The complete fixture and model-envelope schedule is provided as CSV and in the design atlas.

The cabinet frame, pedestal, table, glass, signs and architectural lights stay in the shell. A specimen GLB should normally contain only the exhibit. Duplicating the furniture inside the GLB creates z-fighting, mismatched scales and unnecessary geometry. The installation panel makes origin, bounds and intended content visible before an asset is imported.

## Material and lighting approach

Use matte plaster, pale terrazzo and limestone as the quiet background. Oak provides warmth in the deep-time spaces and ceiling fins. Bronze details provide a consistent family of rails, tracks and frames without making the entire museum metallic. Glass is tinted and deliberately understated.

The baseline renderer uses WebGL 2, a procedural environment, one shadow-casting directional sun, hemisphere lighting and four nearby fill lights. Most architectural geometry is merged by material to avoid a draw call per primitive. Sign panels remain individually readable. Ground contact decals are a visual aid, not global illumination. The glass is a low-cost transparent approximation, not physically traced transmission.

No bloom, heavy fog, cinematic dirt, film grain or automatic soundtrack is required for the design to read. There is no claim of verified photorealism, RTX or hardware performance. Final lighting and reflection tuning must be checked in the actual browser after installing the runtime.

## Visitor controller and interaction

The controller uses a vertical body-radius collision approximation against authored axis-aligned solids. Movement is subdivided to limit wall tunnelling, and separated X/Z movement supports wall sliding. Ramps use an analytic ground-height function; the player is not suddenly snapped from ground level onto the upper deck. There is no jumping, combat movement or mandatory camera sway.

WASD and a touch joystick move; mouse capture, drag-to-look and arrow keys provide alternative ways to orient the view. Settings change field of view, walking speed, sensitivity and eye height. A lower viewpoint and map destinations help inspect the design from different positions. These features do not constitute a full accessibility certification or an equivalent screen-reader experience for a 3D world.

Nearby exhibit briefs are readable HTML dialogs, rather than only small text in the 3D view. The same data drives the installation panel. Architect view removes the roof group and uses an orbiting camera; it does not change the visitor's saved walking position. Installation envelopes can be shown or hidden independently.

## Content, persistence and authoring

The authoritative room/origin data lives in `src/world/layout.js`. Architecture and collision records are compiled in `architecture.js`. The renderer, tests, JSON handoff, SVG plans and Blender reference use that same model instead of independently guessed coordinates.

Each slot has an ID, subject, fixture type, origin, envelope and safe reading point. GLBs attach to the origin with optional offset, rotation and uniform scale. The browser can preview a local file, but cannot silently copy it into the user's project. Persistence requires the user to save the GLB under `public/models` and replace the exported manifest explicitly.

Imported specimen meshes do not generate physics automatically. The existing fixtures block walking where appropriate. An unusually large or interactive specimen may require explicit collision edits; any such edit should be followed by the navigation tests and a fresh walking review. Animation envelopes and anatomical accuracy are additional responsibilities at installation time.

## Validation and exclusions

The delivery has 22 passing dependency-free geometry/navigation tests, including the full suggested loop, front portal clearance, ramp/deck movement and safe viewing points. Syntax checks and PDF/plan inspection are additional checks. Because the Three.js library could not be fetched in the creation environment, live rendering and actual browser GLB loading are not claimed as tested. Blender scripts were syntax-checked but not run inside Blender.

There is no structural model, detailed services layout, fire-engineering package, accessible toilet design, real collection storage system, operational biosecurity facility, ticketing backend, museum staff, crowd simulation or final educational programme. The output is an editable virtual architectural world, not a licensed construction set or an official museum digital twin.

## Primary references

Reference titles and URLs are listed in `src/world/layout.js`, the standalone plan atlas and the PDF. Reviewed 11 September 2026.

[S1] Museums Victoria, Bugs Alive! — https://museumsvictoria.com.au/melbournemuseum/whats-on/bugs-alive/

[S2] Museums Victoria, Dinosaur Walk — https://museumsvictoria.com.au/melbournemuseum/whats-on/dinosaur-walk/

[S3] Museums Victoria, Dinosaur Walk learning resources — https://museumsvictoria.com.au/melbournemuseum/resources/dinosaur-walk/

[S4] Museums Victoria, Triceratops: Fate of the Dinosaurs — https://museumsvictoria.com.au/melbournemuseum/whats-on/triceratops-fate-of-the-dinosaurs/

[S5] Museums Victoria, Visitor map dated 27 July 2026 — https://museumsvictoria.com.au/media/ux5heeeh/melbourne-museum-map-27072026.pdf

[S6] Denton Corker Marshall, Melbourne Museum — https://dentoncorkermarshall.com/projects/melbourne-museum/

[S7] Museums Victoria, Accessibility — https://museumsvictoria.com.au/melbournemuseum/plan-your-visit/accessibility/

[S8] Three.js, GLTFLoader documentation — https://threejs.org/docs/pages/GLTFLoader.html
