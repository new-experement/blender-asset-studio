# Geometry, hidden surfaces and contacts

Use during blockout, construction and production, and after any change to topology, modifiers or allowed views. Project rules and this asset's actual use override the numerical starting points below. These rules apply to clean products, characters and architecture as well as game props; they do not prescribe a genre or engine.

## Establish what can become visible

Record closest viewing distance, image resolution/FOV or orthographic span, allowed camera elevations/azimuths, visible openings, ground or mounting surfaces, and required states. Opening, lifting, turning over, deformation, destruction, reflections and cast shadows can expose or depend on otherwise hidden parts. Reuse known answers; clarify only a consequential unresolved use. A surface hidden in one beauty view is not necessarily removable.

Use an actual compatible object or ruler as a scale reference; a human-sized dummy is useful for human-scale objects, not mandatory for every asset. Keep presentation helpers outside the exported collection.

## Make geometry earn its cost

Geometry is justified by a visible silhouette/profile, bevel highlight, curved shading, shadow, reflection, deformation or required interface/function. Decide representation before adding repeated detail.

- Estimate projected size at the closest allowed view. For a near-centre perspective estimate, pixels/metre is `image_height / (2 * distance * tan(vertical_FOV/2))`; for orthographic use image height divided by vertical world span. Use actual projection measurements near frame edges or for oblique surfaces.
- A bolt, weld, crack or panel line below roughly **4–6 pixels** is normally a map/decal/bake candidate. This is a heuristic, not a hard rejection: silhouette, strong shadows, motion or interactions can justify geometry even when small. Record that reason. Do not substitute a map for a visible hole, thickness or broken silhouette.
- Flat surfaces need only topology that supports their shape, UVs and intended deformation. Avoid evenly distributed loops and delivered subdivision that has no requested purpose; an editable high-detail source and a reduced runtime mesh can be separate deliverables.
- Choose cylinder sides, arc steps and bevel segments from visible curvature. **1–2 bevel segments** are a useful non-focal starting point, not a universal cap. Weighted/custom normals can improve shading but cannot repair a faceted silhouette or missing physical thickness. Inspect under neutral light and at the nearest permitted view.
- Allocate detail to focal/silhouette regions, then regularly visible surfaces, then occasional views; hidden regions receive only what their indirect or functional contribution requires.
- Use linked duplicates/instances for identical repeated parts when compatible with editing, UVs, export and individual condition. Vary wear or UV phase deliberately where identical repetition would be visible; do not solve it by duplicating all geometry or applying arbitrary random damage.
- Count **evaluated/exported triangles and placed instances**, including Array, Bevel, Screw, Remesh and subdivision results. Edit-mode polygon counts are not the cost of the delivered asset.

Material richness still needs large/medium/small structure, localized condition and roughness variation. More geometry, generic noise or extra mechanisms do not compensate for weak visible form. Preserve real surface scale and verify UV density with a checker when parts disagree.

## Hidden-surface decisions

| Situation | Economical representation and protected contribution |
|---|---|
| Parts embedded in terrain or another surface | Keep an overlap sufficient for the actual terrain/placement tolerance. **5–15 cm for an ordinary prop** is only a starting example; derive larger structures or fine products from their scale. Remove deeper geometry, bevels and UV allocation only when no state, shadow, reflection, collider or fabrication contract needs them. Keep a cap if closure or shading requires it. |
| Underside never shown | Retain a simple volume and the visible low-angle outline/shadow; omit unseen small pipes, fasteners and internal assemblies. Preserve wheel arches, exposed supports and parts visible through damage/openings. A lift/flip/wreck state changes this decision. |
| Building interior never entered | Omit inaccessible interior detail. Windows/doorways may need a dark backing, shallow room box or target-supported interior material to avoid an empty shell. Model the depth actually visible through openings. |
| Back against a wall, touching faces, closed containers | Remove/collapse concealed faces only after checking viewing range, opening/replacement states, lighting and required mesh closure. Do not delete an attachment surface needed by another variant. |
| Reflection, shadow or functional geometry | Keep a suitable simplified representation even when no camera directly sees it. Visibility rays alone do not assess indirect contribution, collisions or manufacturing. |

Before committing a substantial removal, inspect a low-angle/opposing view and relevant states; when contribution is uncertain, compare a temporary hidden/not-hidden render under the actual light or reflection. Preserve the best source. Record what was removed and the views/states that justify it. Do not silently reduce an unrestricted asset to the one current camera.

## Contacts and surface integrity

Every part that should be supported must contact a support, declared anchor, or a part connected to one. Hanging, airborne, rig-controlled, deliberately separated and exploded-view parts use their actual brief; do not invent rods or ground contact to silence a diagnostic.

- Set contact tolerance from scale and purpose. **3 mm** is an ordinary metre-scale diagnostic starting point, not a universal assembly tolerance or a collider guarantee. Check visible joints directly and measure in world metres.
- Grounded parts meet the actual support surface. A minimum Z below a plane does not prove contact: a fully buried fragment, a beam over a ravine and an object outside a finite platform need different interpretation. For uneven terrain or a mount, use the actual declared support geometry rather than an arbitrary global plane.
- Recheck adjacent parts **after** bevel, subdivision, deformation and reduction: shrinkage can open a gap absent in the blockout. A small intentional hidden overlap is acceptable if it causes no z-fighting or visible poke-through.
- Contact and penetration are different findings. An intersection can connect two islands in the support graph while being an unacceptable assembly defect. Check both; a supported part is not necessarily correctly placed.
- Inspect for duplicate/coplanar surfaces, flipped normals, zero-area faces and accidental loose vertices/edges. Distinguish requested openings and intentional one-sided cards from accidental holes. Do not close a damaged opening to make a topology counter look better.
- Apply transforms as required by the export/rig contract; keep origins, custom normals, negative-scale handling and baked tangent convention consistent. Flat static ngons can be valid; curved or deforming regions need controlled topology.

## Unwanted interpenetration and working clearances

Check three separate questions: **does it contact its support**, **does solid geometry enter something it should not**, and **is the required gap free throughout the intended motion**? AABB overlap is only a search filter. Triangle crossings alone miss full containment; no crossings alone does not prove an object outside another solid.

Inspect the assembled asset and its relevant surroundings: a character's hand versus the wall, chair versus tabletop, door versus frame, wheel versus body, clothing versus skin. Include the interacting asset in the diagnostic scope; inspecting only a hand in an otherwise empty scene cannot establish wall clearance. Exclude review helpers and unrelated scenery deliberately, rather than treating all scene overlaps as defects.

- Forbidden penetration: visible poke-through or impossible occupation of another solid without a construction/use reason. It can be major/blocking even when no pixels overlap in the one current camera. Inspect an opposing/side view, section, wireframe or x-ray as needed.
- Designed overlap: a footing embedded in soil, a pin in a socket, a welded or joined hidden seam. Record the **exact pair**, permitted region/extent, depth limit in metres, reason and applicable states. Derive these from construction/project evidence; do not ask permission for every ordinary joint. An allowance for a footing must not hide a hand-wall defect or permit arbitrary deeper penetration of the same pair.
- Required clearance: a moving door, seated pose or suspension may need a nonzero gap. Record that functional dimension separately from a diagnostic numerical tolerance. A penetration-free static frame does not certify clearance or motion.
- Check after modifiers, skinning/pose changes, assembled placement, optimization and export. For moving parts/characters inspect required poses, extremes and useful intermediate frames; sampling frames is not continuous collision detection. Self-intersection of a connected body/clothing mesh needs separate visual/pose or appropriate self-collision analysis.
- Do not fix a penetration by enlarging tolerance, globally shrinking the model, deleting the contacted structure or weakening the pose/interface contract. Repair the actual placement, joint/pose, local shape or topology while preserving scale, silhouette, support and attachment requirements. Record pair, region, saved frame/state, observed/estimated depth, specific operation and fresh verification.

Default tolerances are diagnostic hypotheses. Visible poke-through still fails the visual gate below a numerical threshold. Open shells, cards, alpha cutouts, nonmanifold surfaces, disconnected cavity shells and intended containment can make a simple solid-volume interpretation ambiguous; classify and inspect them instead of declaring them clean or automatically deleting geometry.

## Reusable contact and visibility diagnostics

`scripts/audit_geometry.py` is a separate **background-Blender** diagnostic. It opens an explicit saved `.blend`, `.glb` or `.gltf`; it never connects to live MCP, saves an asset, deletes geometry or awards artistic acceptance. Keep the existing general asset audit as well: this helper examines different claims.

Run from the skill directory, substituting the actual Blender executable, input and a new output path:

```bash
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/audit_geometry.py -- --input model.blend --collection Asset --output contacts-r03.json --check contacts --tolerance-m 0.003 --anchor mounting_wall
```

An anchor/occluder is a named object present in the input; add its flag again for more than one. An explicit `--ground-z-m 0` represents an infinite horizontal support plane in world metres; use it only when that matches the task. Without declared ground/anchors, the report identifies unanchored components rather than certifying physical support. `--occluder terrain` supplies visual occlusion, **not** implicit contact support; a terrain that supports the asset must be declared as an anchor too.

```bash
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/audit_geometry.py -- --input model.blend --collection Asset --output visibility-r03.json --check visibility --elevations=20,40,60,80 --azimuths=0,45,90,135,180,225,270,315 --samples-per-face 7 --max-work 2000000 --occluder terrain
```

Set angles from the recorded camera/state contract. The default directions include below-horizontal views, suitable only when such views are allowed. `--check both` runs both diagnostics. `--ray-epsilon-m` adjusts the ray offset when scene scale demands it; `--backface-cull` is optional, and must match the material/visibility assumption. Animated or changed states need their own saved inputs; one state never certifies all poses.

Interpret the JSON and then inspect the flagged regions:

- Contact islands and their paths to supports are geometric approximations. Vertex/BVH sampling can miss thin gaps, nesting or near tangencies; it does not prove load-bearing construction, watertightness, collision or physical stability.
- Visibility samples several points per face along discrete directions. **Candidate unseen** means no sampled direct view was found, not that the whole face can never be seen. Partly exposed faces, alpha materials, occlusion, concavity and indirect effects need visual checks. Do not delete from this label alone.
- `--max-work` bounds diagnostic operations per check, not memory or elapsed time. A capped check reports incomplete/unclassified work; untested geometry must not become hidden or unsupported by default.
- Scope is evaluated viewport geometry at the saved state, with placed instances and explicit context. Render-only differences, materials and required alternate states still need inspection. Read settings, exclusions and limitations even if the process exits normally; report completion is not a modeling-quality pass.

Use findings to prioritize an executable repair or a reasoned exception in the ledger. A large unseen candidate group calls for investigation; a supported/visible result never proves that the target appearance is good.

## Separate intersection diagnostic

`scripts/audit_intersections.py` runs only in an isolated background Blender process and never fixes/saves the input. It checks evaluated world-space geometry at the saved frame, within the asset scope and explicit interacting context. It reports geometric evidence and uncertainty; it is not a physics engine, continuous motion check or universal self-intersection proof.

```bash
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/audit_intersections.py -- --input assembly.blend --collection Character --against Wall --output intersections-r03.json --tolerance-m 0.003 --max-work 2000000
```

Repeat `--against` for other named objects, or use `--against-collection Furniture` for another assembled asset. Objects must exist in the saved input; a standalone GLB cannot prove compatibility with an absent house/table. In-scope asset pairs are checked too. The examples' 3 mm tolerance is not an automatic allowance for visible clipping.

For intentional construction overlaps, an optional `--allowances allowances.json` supplies exact-name pairs and a threshold on the helper's **sampled interior-distance metric**:

```json
{"pairs":[{"objects":["Footing","Soil"],"max_interior_distance_m":0.12,"reason":"Designed lower-footing embed; separately measure physical embed extent and confirm region in side view"}]}
```

The metric is a witness point's distance to the nearest enclosing surface, **not** axial embed depth, overlap thickness or the translation needed to separate two objects. A thin slab can have a small interior distance while a post protrudes far through it. Measure the actual project-required embed/clearance along the relevant axis separately.

The allowance is a candidate exception, not an unconditional ignore or spatial region mask. No observed sample beyond its threshold proves neither a true maximum nor compliance of the permitted region. An observed threshold exceedance remains a finding even when below the general diagnostic tolerance. If one original object name has several evaluated placements, the allowance remains ambiguous/incomplete rather than silently applying to every instance; inspect IDs/parents and distinguish the actual assembly members.

Explicit context collections containing unsupported geometry (for example, Curve tabletops) are rejected rather than silently omitting it. Unsupported geometry in the asset scope makes coverage incomplete. A named mesh context still needs the intended solid/alpha interpretation; raw render geometry is not automatically a collision proxy.

Review surface crossings, containment candidates, uncertain open/degenerate or nested-shell geometry, untested connected-mesh self-intersection and capped/incomplete work separately. Preserve input hashes and capture the same pair in the actual reopened export before closing its defect. None of these diagnostic states certifies the entire assembly or motion collision-free.
