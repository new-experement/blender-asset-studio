---
name: "blender-asset-studio"
description: "Build or refine a high-quality editable 3D model in Blender via Blender MCP from a brief, references and clarifications: staged blockout→pilot→finish, strict visual self-review against a target, executable repairs, export checks."
---

# Blender Asset Studio

Produce an editable model that survives close comparison with its target at the intended viewing conditions. Own the work from brief to delivery, including the critical review the user would otherwise have to request again and again. The result is judged by how it looks, not by how the process is reported.

Applies to props, vehicles, buildings, characters and asset families. Not for: a concept image alone, a plain export of an approved model (just export and check it), or engine programming.

## Non-negotiable rules

- Preserve the user's scope, primary references and protected features. Explicit user/project rules override the fallback choices here.
- At the start of modeling/refinement, resolve how and where the asset will be used. Ask the required opening question with relevant example answers unless the request or accepted brief already explicitly answers it; record the use contract before choosing detail, simplification or moving parts.
- Look at actual pixels: references, and fresh renders of the current model. A filename, a summary or your own description of what you built is not visual evidence.
- Separate maker and reviewer. A script that ran, a low triangle count or a confident narrative never passes the visual gate.
- Artistic quality is judged against the visual target. Export fidelity is judged against the source. A perfect export of a weak model is still a weak model.
- Every criticism becomes an executable repair: object/region, observed evidence, measurable target, operation, what must not change, how it will be verified.
- A repair counts only after fresh evidence of the changed model. Old screenshots never certify a new revision.
- Keep the best checkpoint. Running out of budget means delivering as incomplete with named defects, never relabeling a visible major defect as minor.
- Spend geometry only where it can be seen and changes what is seen; nothing floats, nothing has visible gaps (see Modeling discipline).
- Nothing grows into anything it shouldn't: no part of the asset passes through another part or through the objects it is used with (a hand through a wall, a chair leg through a tabletop, a wheel through the body). Touching is checked separately from penetration: parts that intersect look "connected" to a contact check and are still a defect. Only designed embeds with a recorded pair and depth are allowed.
- Do not expand scope to hide weak execution: more props, more random damage, more polygons are not improvements by themselves.

## Tools in this environment

| Need | Tool / approach |
|---|---|
| Start | `get_addon_status` once: Blender version, enabled asset libraries and generators. |
| Scene facts | `get_scene_info` with `fields` such as `size`, `ground` (floating/below), `topology` (ngons, non-manifold, loose verts), `materials`, `modifiers`, `settings`. Use it for measurements; don't estimate sizes from pictures. |
| Seeing | `look`: `mode="angles"` with `views` (front/back/left/right/top/three_quarter or `[x,y,z]`), `mode="camera"` for a fixed review camera, `shading` solid / material / rendered / wireframe, `distance` for close-ups, `max_size` (small for quick checks, larger for fine detail), `image=` to show a saved render or reference file. |
| Building, measuring, rendering to files, saving checkpoints, writing the ledger | `execute_blender_code` in small steps that print what you need. |
| Materials and lighting | `search_assets` / `import_asset`: Poly Haven CC0 textures and HDRIs first (use `previews` before importing). Sketchfab/Poly Pizza models only as reference or with an explicit license check. A library texture is a starting point, not a finished material. |
| Generated base mesh | `generate_3d` costs the user money or quota: use only with explicit permission. Its output arrives at arbitrary scale/facing and is a base or reference, never a finished asset; it goes through the same gates. |
| References | User attachments first; web image search for missing real-world references (record source and role). |
| Independent review | Render evidence to files, then a separate reviewer agent (Agent tool) gets only the brief, the references and the renders, not the maker's notes. If a reviewer agent is not available, run a distinct sequential review pass and don't call it independent. |

There is no image generation here. If a painted concept would help, offer: user-supplied art (e.g. made in another tool), a reference board assembled from search, or a quick 3D blockout shown as the concept checkpoint.

If Blender MCP is not reachable, finish the brief/reference work and say the modeling stage is not executed. Never deliver an illustration as a 3D model.

## 1. Intake: the brief

Read what's already available: the user's message, attachments, earlier answers, existing files and assets in the scene. Then ask one compact batch of only the questions that are actually open (usually 2-5). Never ask what was already answered; never pad the count.

### Required opening question: intended use

At the start of a modeling or refinement task, explicitly ask in the user's language: **"How and where will this model be used? What will the viewer or user be able to do with it, and from which sides will it be seen?"** Include two short, relevant example answers so the user understands the kind of context needed. Choose from these or adapt them to the asset:

- **Building:** "A background exterior, never entered" versus "An explorable building with an interior and opening doors."
- **Vehicle:** "Driven normally; the underside is never visible" versus "May overturn and remain upside down, exposing the underside."
- **Weapon:** "Carried by distant enemies" versus "Inspected close up in a weapon rack or a rotating selection-menu view, with moving parts shown."

Reuse an explicit answer already present in the request or accepted brief instead of asking again; record its source. An asset category, genre, engine name or size alone is not an intended-use answer. If the user explicitly delegates this choice, record the selected scenario and its assumptions. For a narrow edit, preserve an established use contract and reopen only affected states. An export-only task does not need a new modeling interview.

Translate the answer into a **use contract** before substantial modeling:

- Placement/context, user interaction and closest relevant view, including gameplay, display or menu views when applicable.
- Required visible sides/interiors and states: normal use, opening, lifting, overturning, damage, disassembly or other stated actions; note explicit exclusions.
- A visibility/detail plan for those views and states: where geometry and texture detail matter and what can safely be simplified while preserving silhouette, shadows, reflections and function.
- Static versus separate/moving parts; required pivots, articulation/deformation and operating clearance. Plan these before detailing, but do not invent mechanisms or require rigging for a static asset.

If the reply is too broad to decide a consequential interior, underside or motion requirement, ask a targeted follow-up with concrete alternatives. Continue independent preparation while it is pending; do not assume such a requirement is absent or simplify away geometry needed by an unresolved use. Review the final source and export in the agreed views and required states.

Topics the brief must resolve:

| Topic | Must resolve |
|---|---|
| Intended use (required) | Ask the opening question above with relevant examples; record placement, interaction, exposed sides/interiors and states, and their detail/simplification and moving-part implications. |
| Subject and function | What it is, key dimensions and variants. |
| References | Explicitly ask for 1-3 examples and what to take from each: form, materials, condition, overall quality. "No examples" is a valid answer; record it. |
| Style and condition | Stylized/realistic; new, maintained, aged, damaged; where and how much. A genre word does not define the amount of damage. |
| Viewing and use | Closest camera distance and screen size; allowed camera range (can it ever be seen from below, from behind, from inside?); does it stand on ground, set into it or mount on something; can it move, open, tip over, be entered or destroyed. These answers decide what may be simplified or removed. Which other objects it touches or is used with (wall, table, terrain, a character), and which poses/states must work. |
| Direction mode | Show a concept/blockout for approval first, or decide autonomously and deliver. |
| Limits | Required formats, triangle/material/texture limits if any, effort budget. |

A natural reference request: "Please share 1-3 examples of the desired appearance or quality and explain what to take from each: shape, materials, or condition. If you have no examples, say so."

Record each topic as answered / delegated / pending. A reply about size closes only the size question. While waiting, do useful independent work: inspect references, check capabilities, measure, search materials, draft the brief. Don't build the detailed model on assumptions.

If the user says "decide yourself", record the delegation and proceed. If the request is a narrow edit of an approved asset, ask only about the change.

Write the brief once (keep it in the work folder, see section 3):

- Asset ID, purpose, deliverables.
- Intended-use answer/source or explicit delegation; use contract with placement, interaction, closest views, required/excluded visible sides/interiors/states, detail/simplification plan and static/separate/moving-part requirements.
- References with roles (primary shape / material / condition / quality benchmark / scale) and what must NOT transfer from each.
- Visual target and quality benchmark (see section 2).
- 3-6 observable success criteria and the main ways a simplistic result would fail.
- Protected features, allowed freedom, inferred hidden parts.
- Dimensions, units, axes, origin, closest view.
- Visibility map: focal / often visible / occasional / hidden, with the allowed camera elevation and azimuth range and the ground/embed rule.
- Interaction contract: objects the asset must coexist with (keep them, or stand-ins at the real size, in the scene as context), designed embeds as exact pair + max depth + reason (post into terrain 0.15 m, pin into socket 0.02 m), required clearances (door swing, seat), poses/frames to check.
- Technical limits and where each came from; separate hard limits from your own planning estimates.
- Budget (section 6).

## 2. Visual target and quality bar

Keep three anchors separate:

1. **Design target**: shape, proportions, construction, material distribution, condition, from the selected references or approved blockout.
2. **Quality benchmark**: a visible example of the intended finish and detail hierarchy (user example, an accepted existing asset, or a reference you found and show). State which qualities transfer.
3. **Constraints**: function, camera, scale, budgets.

"AAA" or "high quality" is not a target until translated into observable criteria, e.g.: intentional readable silhouette; believable thickness, joins and supports; distinct material response (metal vs paint vs rubber vs concrete); wear that has a cause and a location; coherent large/medium/small detail; no visible repetition at the intended view.

Don't impose a taste: a clean stylized product should stay clean; weathering is used only when the target calls for it.

For each reference, inventory: silhouette, primary masses and ratios, component count and placement, openings and negative spaces, construction and attachments, material regions, condition, signature details. Mark every fact as observed / measured / inferred / provisional. Never invent exact millimetres from an unscaled photo; write ratios with tolerances ("post width ≈ 0.08-0.10 of opening width, inferred").

For damage, reason from material: wood splits along fibers and joints; concrete loses cover, shows aggregate, fractures through volume; thin metal bends, tears and dents; paint chips at edges and contact points. Shape, exposed interior, edge shading and dirt must agree.

## 3. Workspace and review stage

- Discover the open file and scene first. Never reset the user's scene, delete other objects or overwrite unrelated files.
- Put the asset in its own collection (e.g. `ASSET_<id>`) and helpers in `REVIEW_<id>`, excluded from export.
- Work folder next to the .blend (or a folder the user chose): `<id>_work/` with `brief.md`, `ledger.md`, `refs/`, `review/rNN/`, `checkpoints/`, `export/`. Write files through `execute_blender_code`.
- Units: metres, +Z up in Blender, identity root transform, origin at the support/attachment point unless specified. Record the forward axis.
- Build a fixed **review stage** once and reuse it for every revision so comparisons are fair:
  - neutral grey ground plane; a neutral studio HDRI or a 3-light rig with fixed exposure; Standard or AgX view transform, recorded;
  - fixed cameras: one matching the primary reference view, three-quarter, an opposing view, top or underside if relevant, plus the intended-use camera (real distance/angle/FOV);
  - a scale reference (1.8 m human-sized dummy) placed beside the asset in a dedicated view.
- Render evidence to files `review/rNN/<view>.png` with EEVEE (or Cycles at low samples for materials), and look at them with `look(image=...)`. For quick checks `look` alone is fine.
- Prefer parameterized, re-runnable builder steps with stable object names. After a timeout, inspect the scene before retrying: the step may already have run. Save a checkpoint (`checkpoints/rNN.blend` via `bpy.ops.wm.save_as_mainfile(copy=True)`) at each accepted stage.

## 4. Build in gated stages

Advance only when the current gate passes. A blocking or major defect keeps the asset at its stage.

| Stage | Work | Gate evidence | Keep working if |
|---|---|---|---|
| 1. Blockout | Proportions, silhouette, scale, openings, contact with ground, major parts | Primary-reference view + opposing view, silhouette render, scale dummy | Proportions, ratios, silhouette or scale are off. |
| (Concept checkpoint) | If the user chose to approve direction: show blockout renders from 2-3 angles + the reference board, wait for their choice | User's answer | Direction not approved. Skip if delegated. |
| 2. Construction | Thickness, supports, joins, bevels, negative spaces, moving parts and pivots, attachment points | Close views of joins; wireframe | Paper-thin parts, floating parts, gaps at joins, intersections, impossible connections, detail spent on hidden areas. |
| 3. Pilot | The hardest visible section fully finished (geometry + material + condition), e.g. a damaged edge with its cross-section, a curved panel and its join, a face | Matched target/candidate crops under neutral light and at the intended view | Looks like a blockout with a texture, stencil-cut damage, generic/plastic material. Fix the method before scaling it to the whole asset. |
| 4. Materials and detail | Apply the proven method to the whole asset; geometry where it changes silhouette, maps where it doesn't | Full review set (section 5) | Good local details don't add up to a convincing whole; a large blank or wrongly conditioned area dominates. |
| 5. Production | UVs, baking if useful, material consolidation, topology reduction | Same views re-rendered after optimization | Optimization destroyed protected shapes or visible detail; hidden geometry still carries significant triangles. |
| 6. Delivery | Export and verification (section 7) | Reimported export inspected | Export differs from source. |

For a family: accept one representative pilot first, then build the others, then review every materially different member and the whole family side by side.

Material practice:
- Build materials in layers: base material, then large-scale variation (value/hue shifts across the surface), then localized condition (edge wear, dirt in cavities, streaks under fixtures, sun fading on top surfaces), then fine surface detail. Wear needs a cause.
- Roughness variation sells materials more than color noise does. Uniform noise over everything is a failure, not detail.
- Check texel density visually (a checker texture pass) so detail scale is consistent between parts.
- Colors: identify encoding. Blender node values are scene-linear: c_lin = c/12.92 if c ≤ 0.04045 else ((c+0.055)/1.055)^2.4. Don't sample a lit reference pixel and use it as albedo.
- A numeric material change is a hypothesis: confirm its visual effect in a render.

### Modeling discipline: economy and integrity

These are standing professional rules, applied at every stage, not only in production.

**Every polygon must earn its place.** Geometry is justified only if it changes, at an allowed view: the silhouette, a visible profile or bevel highlight, shading of a curved form, a cast shadow, deformation, or a required function (opening, pivot, collision shape). Everything else goes into normals, textures, decals or nothing.

- Estimate on-screen size before modeling a detail: projected size in px ≈ size in m × pixels-per-metre at the closest allowed view. A bolt, rivet, weld seam, crack or small panel line smaller than roughly 4-6 px at the closest view is a normal/texture/decal, not geometry.
- Flat areas get the minimum topology that holds their shape and UVs; no evenly spread loops, no support loops or subdivision left in the delivered mesh unless the brief asks for a subdivision-ready source.
- Curvature density follows screen size: cylinder sides, bevel segments and arc steps are chosen so the silhouette reads smooth at the closest allowed view and no denser. Small cylinders don't get as many sides as large ones; bevels on non-focal edges get 1-2 segments; hard-surface shading is fixed with weighted/custom normals rather than extra loops.
- Density goes where the eye goes: focal regions and silhouette edges get the most; regularly visible areas less; occasional areas little; hidden areas near zero.
- Repeated parts are linked duplicates or instances, not unique copies. Watch modifier stacks (Subdivision, Bevel, Array, Screw, Remesh): judge the evaluated triangle count, not the edit-mode count.
- Don't add mechanisms, interior parts, props or decoration the brief doesn't need to make the model "feel detailed". Complexity is not quality.

**Hidden-surface policy.** Decide visibility from the brief's allowed camera range and use, then remove or collapse what can never be seen:

- Parts set into the ground or into another object (posts, foundations, pipes into walls, rocks, debris): keep a short embed below the contact surface so uneven terrain or slight offsets never show a gap, typically 5-15 cm for props and more for large structures; delete everything deeper and don't cap it. No detail, bevels or UV space below the contact line.
- Vehicle and object undersides that the camera can't see: a simple closed underside with the readable low-angle silhouette (wheel arches, axles, a few large masses) and a dark simple material; no modeled chassis, exhaust runs or suspension detail unless low views, lifting, flipping or wrecking make them visible.
- Building interiors that are never entered: no interior. Windows and doorways get a backing (dark card, simple room box, or interior-mapped texture) deep enough to stop see-through and empty-shell reads from the allowed views. If an interior is visible through openings, model only the depth visible through them.
- Backs of objects that always stand against a wall, faces pressed against another part, the inside of closed boxes and tanks: delete or collapse them.
- Keep geometry that is hidden from direct view but still affects what you see: shadow-casting volume, silhouette at the lowest allowed angle, reflections, see-through gaps, collision or physics shape, and any state where the object moves, opens, tips over or is destroyed. When the brief is silent on these, ask in intake.
- Verify with the hidden-geometry audit (section 7): the share of never-visible triangles should be small and explained; a large never-visible share on a finished asset is a defect to fix, not a statistic.

**Integrity: nothing floats, nothing is broken.**

- No floating parts: every piece touches the ground, a declared anchor (wall, ceiling, pole) or a part that does. Pieces that should touch must touch within a few millimetres; visible gaps at joins are defects. Check after every modifier change: subdivision and bevels shrink shapes and open gaps that weren't there in the blockout.
- Objects rest on their support: no hovering above the ground, no sinking deeper than the intended embed.
- A small hidden overlap at an ordinary joint (a welded seam, a board end into a post) is acceptable if it never shows, causes no z-fighting and stays within a few millimetres; anything deeper or visible is penetration (below).
- No coplanar overlapping faces, duplicate surfaces, zero-area faces, loose vertices/edges, flipped normals or open holes visible from allowed views.
- Applied scale (1,1,1) and rotation on delivered meshes, origin per the brief, no accidental negative scale.
- Ngons are fine on flat static surfaces; avoid them where shading curves or the mesh deforms.
- Verify with the floating-parts audit (section 7) plus close views of every join. That audit counts intersecting parts as connected, so a clean result there says nothing about penetration.

**No unwanted interpenetration.** Answer three separate questions for every assembly: does each part contact its support; does any solid enter something it shouldn't; is every required gap free in every required state.

- Check the assembled asset together with what it touches or is used with: hand vs wall, chair vs table, door vs frame, wheel vs body and wheel arch, clothing vs body, prop vs terrain. An isolated part in an empty scene can't prove it fits its surroundings; bring the context objects (or real-size stand-ins) into the scene and declare them as context.
- Forbidden penetration: visible poke-through, or one solid occupying another without a construction reason. It is a major or blocking defect even if the current camera happens not to show it; inspect opposing views, a section, wireframe or x-ray.
- Designed embed: footing into soil, post into ground, pin into socket, pipe into wall. Record the exact pair, maximum depth in metres and the reason. An allowance for one pair never excuses another pair or a deeper intrusion of the same pair. Ordinary joints don't need the user's permission, just the record.
- Required clearance: moving doors, lids, wheels under suspension travel, seated poses need a real gap. Record it as a functional dimension; one static frame without penetration doesn't prove the motion is clear.
- Re-check after modifiers, posing/skinning, placement in the assembly, optimization and export. For moving parts check required poses, extremes and a few intermediate frames (set the frame, re-run); sampled frames are not continuous collision detection.
- Self-intersection within one connected mesh (a limb folded through its own body, cloth through itself) is not covered by the audit; inspect those poses visually.
- Fix the actual cause: move or re-pose the part, reshape the local region, adjust the joint. Never fix penetration by raising the tolerance, shrinking the whole model, deleting the contacted structure or weakening the pose/interface. A visible poke-through fails the visual gate even if its measured depth is below the tolerance.
- Verify with the penetration audit (section 7) plus close views of each flagged pair.

## 5. Review protocol

Run for every meaningful revision. The reviewer looks at the brief, references and fresh renders before reading any maker explanation.

### 5.1 Capture

Save a new revision ID `rNN`; never overwrite evidence of an earlier revision. Render the fixed review set: primary-matched view, three-quarter, opposing, top/underside if relevant, intended-use camera, close-ups of focal regions, any functional poses. Same lights, exposure and cameras as before.

### 5.2 Whole-object judgment first

Before any local crop, answer honestly: at the intended viewing size, does the whole thing reach the target and the benchmark, or does it read as a placeholder? Then run these quick tests:

- **Silhouette test**: flat black silhouette from 2-3 angles. Is it readable and recognizable? Are signature shapes and negative spaces present?
- **Value test**: grayscale, slightly blurred (squint). Is there a clear large / medium / small hierarchy, or is it uniform mush?
- **Thumbnail test**: downscale to the real screen size. What still reads? What is wasted detail? What is lost that matters?
- **Scale test**: next to the human dummy. Do doors, steps, handles, bolts match human scale?
- **Contact test**: floating-parts audit (section 7), `get_scene_info(fields=["ground"])` and close views of joins. No floating parts, no gaps where parts should meet, believable contact with the ground.
- **Penetration test**: penetration audit (section 7) on the assembled asset with its context objects, in every required pose/state; x-ray/section views of flagged pairs. No forbidden penetration, designed embeds within their recorded depth, required clearances free.
- **Wireframe test**: density follows silhouette and focal areas; flat areas are light; hidden-geometry audit (section 7) shows no significant never-visible triangles.
- **Neutral-light test**: materials still read without dramatic lighting. A hero render that relies on darkness, distance or props to hide problems does not count.

### 5.3 Region-by-region comparison

Build a semantic region map suited to the object (structure: roof, openings, supports, joins; vehicle: body, wheels, cabin, equipment; character: face, torso, limbs, clothing). Compare corresponding parts even if they sit in different places in the two images; don't compare by grid cell.

For each region write a paired observation: **target appearance → candidate appearance → difference → repair ID or reason it passes.** Describe contour, material response, local variation and finish, not just counts. A geometric pass is not a material pass. For regions unseen in the reference, check consistency with the inferred design; don't invent an observation. Mark unreviewed regions explicitly.

| Layer | Questions |
|---|---|
| Identity, silhouette | Right component count, mass ratios, contour, negative spaces, signature details? |
| Construction | Plausible thickness, loads, supports, joins, attachments? |
| Materials | Right assignment, scale, hue/value, roughness, metalness, transparency? |
| Condition | Matches the chosen age/use; wear has causes and location; not pristine, not uniformly noisy? |
| Detail | Important features present; small details help at target scale; no intersections, floating bits, stray fragments? |
| Interactions | No part passes through another part or through the context objects; designed embeds bounded and recorded; clearances survive poses, modifiers and assembly? |
| Function | Pivots, gaps, clearances, extreme poses work? |
| Production | Budget, topology, UVs, export appearance preserved? |

### 5.4 Reject weak results concretely

Reject when a target-relative mismatch like these is visible:
- unshaped primitives with uniform bevels where the target has specific contours and transitions;
- flat or uniformly noisy materials where the target has readable layers, roughness variation and localized wear;
- repetition at identical intervals, mirrored damage, equally sized holes;
- cracks drawn as dark lines with no volumetric breakup; clean planar cuts where material should splinter, crumble or bend;
- inconsistent detail scale: giant grain, tiny stones, paper-thin members;
- detail that only exists in one dramatic render.

Don't apply these blindly to deliberately simple styles. Don't excuse a major mismatch as "subtle at game distance" if it's still visible at the agreed view.

### 5.5 Defect ledger

Keep `ledger.md` updated during review, not reconstructed at the end. Each defect:

- ID, severity, object/material/region, view, revision.
- Target evidence and observed candidate evidence.
- Measurement origin: measured / estimated ratio / artistic choice, with uncertainty.
- Current value → target value with unit and tolerance.
- Operation and layer (geometry, topology, UV, material, texture, lighting).
- What must not change; how it will be verified.
- Status: open → applied → verified (with the evidence path and revision); failed verification goes back to open.
- For penetration/clearance: both objects, the region, the frame/pose and context used, the sampled depth or gap, the allowed depth if it's a designed embed. A clean contact audit never closes a penetration defect.

Severity: **blocking** (identity/silhouette wrong, required part missing, unusable export, broken function), **major** (clearly visible mismatch with target/style/construction at the intended view), **minor** (local imperfection that doesn't weaken the target). No score can cancel a blocking or major defect.

Write repairs that can be executed:
- Bad: "make the roof thicker". Good: "roof_panel thickness 0.018 → 0.036 m (±0.002); move the lower shell −Z 0.018 m, keep upper surface, pitch and eave outline; verify by cross-section measurement and the right-side render."
- Bad: "make the concrete less white". Good: "base color sRGB #D6D3C8 → #A9A393, roughness 0.50 → 0.82, metallic 0; keep the stain mask; re-render with the same exposure, then check at the intended view."
- Bad: "improve the broken corner". Good: "cut the upper outer corner along the annotated 3-point contour; keep the lower support and attachment face; expose the cross-section with 30-50 mm irregular chips concentrated at the break, not on every edge; support must still touch the upper beam."

Use landmarks, ratios, vectors, angles, profiles and annotated contours when one number isn't enough, but don't claim precision the reference doesn't have.

## 6. Repair loop and budget

Loop: review → fix the highest-impact coherent group of defects → fresh renders → recheck the changed regions, their neighbours and protected features → keep the new revision or restore the better checkpoint → update the ledger.

Each pass must produce a changed artifact or a real new observation; a rephrased self-critique is not progress. If a fix creates a worse defect, revert and change approach.

Two consecutive failed attempts on the same important defect: diagnose the cause (form, material, lighting, projection, export) and switch to one different method (e.g. modelled geometry instead of a normal-map fake, a better source texture, local masks/decals, a sculpt-and-bake, a different topology approach). Don't keep nudging the same parameter.

Default budget unless the user sets one, announced at the start: up to 4 full repair cycles after the first candidate, plus 2 targeted passes. `generate_3d` calls: 0 unless the user authorizes them. These limits are task-wide and don't reset per stage. Unused cycles needn't be spent.

Work autonomously within the brief. Ask the user only for: a consequential identity/function conflict, a missing essential reference, a scope change, new cost, or a real quality-vs-budget tradeoff. Never ask which obvious defect to fix or whether to keep inspecting. Keep updates short: stage, key finding, next fix.

User corrections become constraints and regression checks; reopen only the affected decisions.

Stop as **done** when the required regions are inspected, no blocking/major defects remain, technical checks pass and minor deviations are listed. Stop as **incomplete** when the budget or capabilities run out: deliver the best checkpoint and name what remains and the next method.

## 7. Technical checks and export

Limits, in priority: explicit user requirements → the target application's rules if given → disclosed provisional defaults. Without given limits, pick a planning estimate from actual use (screen size, distance, instance count) and label it yours; don't use a low invented cap to excuse visible faceting. For standalone visualization, don't force game budgets.

Read-only audit in the live session (counts evaluated triangles, materials, UVs, unapplied transforms):

```python
import bpy
col = bpy.data.collections["ASSET_id"]
dg = bpy.context.evaluated_depsgraph_get()
tris, mats, no_uv, xf = 0, set(), [], []
for o in col.all_objects:
    if o.type != 'MESH' or o.hide_render:
        continue
    e = o.evaluated_get(dg); m = e.to_mesh(); m.calc_loop_triangles()
    tris += len(m.loop_triangles)
    mats |= {s.material.name for s in o.material_slots if s.material}
    if not m.uv_layers: no_uv.append(o.name)
    if any(abs(v - 1) > 1e-4 for v in o.scale): xf.append(o.name)
    e.to_mesh_clear()
print("tris", tris, "materials", sorted(mats), "no_uv", no_uv, "unapplied_scale", xf)
```

Also check with `get_scene_info(fields=["topology","ground","materials","modifiers"])`: ngons/non-manifold where they matter, loose verts, normals (face orientation view), duplicate surfaces, z-fighting.

Hidden-geometry audit (read-only; casts rays from every face toward the allowed view directions, with the ground as an occluder). Set `ELEVATIONS`/`AZIMUTHS` from the brief's camera range; for a standalone asset with no restriction, include negative elevations. Faces only partly buried count as visible. Runs in about a second for ~50k triangles.

```python
# Hidden-geometry audit: which triangles can never be seen from the allowed views.
import bpy, math
from mathutils import Vector, geometry
from mathutils.bvhtree import BVHTree

COLLECTION = "ASSET_id"
ELEVATIONS = [10, 30, 55, 80]   # camera angles above the horizon that can really occur; add negatives if it can be seen from below
AZIMUTH_STEP = 30               # degrees around the object; restrict AZIMUTHS if only some sides are ever seen
AZIMUTHS = None                 # e.g. [180, 210, 240] for a wall-mounted asset seen only from the front
GROUND_Z = 0.0                  # set to None if the asset does not stand on ground
MAX_FACES = 30000               # faces above this are sampled to keep the check fast

col = bpy.data.collections[COLLECTION]
members = set(col.all_objects)
dg = bpy.context.evaluated_depsgraph_get()
verts, polys, owner = [], [], []
for inst in dg.object_instances:
    src = inst.object.original
    par = inst.parent.original if inst.parent else None
    if (src not in members and par not in members) or inst.object.type != 'MESH' or src.hide_render:
        continue
    m = inst.object.to_mesh(); mw = inst.matrix_world.copy(); base = len(verts)
    verts += [mw @ v.co for v in m.vertices]
    for p in m.polygons:
        polys.append([base + i for i in p.vertices]); owner.append((src.name, len(p.vertices) - 2))
    inst.object.to_mesh_clear()

lo = Vector([min(v[i] for v in verts) for i in range(3)])
hi = Vector([max(v[i] for v in verts) for i in range(3)])
center, radius = (lo + hi) / 2, max((hi - lo).length / 2, 0.01)
occ_v, occ_p = list(verts), list(polys)
if GROUND_Z is not None:
    s = radius * 50; b = len(occ_v)
    occ_v += [Vector((center.x + x * s, center.y + y * s, GROUND_Z)) for x, y in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    occ_p.append([b, b + 1, b + 2, b + 3])
bvh = BVHTree.FromPolygons(occ_v, occ_p)

azs = AZIMUTHS if AZIMUTHS is not None else list(range(0, 360, AZIMUTH_STEP))
dirs = [Vector((math.cos(math.radians(e)) * math.cos(math.radians(a)),
                math.cos(math.radians(e)) * math.sin(math.radians(a)),
                math.sin(math.radians(e)))) for e in ELEVATIONS for a in azs]
eps, dist = max(radius * 1e-4, 1e-4), radius * 6
step = max(1, len(polys) // MAX_FACES)
seen_t, total_t, hidden = 0, 0, {}
for idx in range(0, len(polys), step):
    pts = [verts[i] for i in polys[idx]]
    n = geometry.normal(pts)
    c = sum(pts, Vector()) / len(pts)
    name, t = owner[idx]; total_t += t
    vis = any(n.dot(d) > 0.02 and bvh.ray_cast(c + n * eps + d * eps, d, dist)[0] is None for d in dirs)
    if vis:
        seen_t += t
    else:
        hidden[name] = hidden.get(name, 0) + t
hid = total_t - seen_t
print(f"tris checked {total_t} (every {step}), never visible {hid} = {100 * hid / max(total_t, 1):.1f}%")
for name, t in sorted(hidden.items(), key=lambda kv: -kv[1])[:12]:
    print(f"  {name}: {t * step} hidden tris (est.)")
```

Floating-parts audit (read-only; splits the evaluated meshes into connected pieces and checks that each is linked to the ground or a declared anchor through a chain of contacts). It works on evaluated geometry, so it also catches gaps opened by subdivision or bevel modifiers.

```python
# Integrity audit: loose pieces that touch neither the ground nor anything attached to it.
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

COLLECTION = "ASSET_id"
TOL = 0.003            # metres: closer than this counts as touching
GROUND_Z = 0.0         # None if the asset hangs from or mounts on something instead
ANCHORS = []           # names of objects outside the asset it legitimately attaches to (wall, ceiling, pole)

col = bpy.data.collections[COLLECTION]
dg = bpy.context.evaluated_depsgraph_get()
isl = []  # (label, points, bvh, lo, hi)
def add_islands(obj, label_prefix):
    bm = bmesh.new(); bm.from_object(obj, dg); bm.transform(obj.matrix_world)
    seen = set()
    for f in bm.faces:
        if f in seen: continue
        stack, group = [f], []; seen.add(f)
        while stack:
            g = stack.pop(); group.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h not in seen: seen.add(h); stack.append(h)
        vs = list({v for g in group for v in g.verts}); vi = {v: i for i, v in enumerate(vs)}
        co = [v.co.copy() for v in vs]
        bvh = BVHTree.FromPolygons(co, [[vi[v] for v in g.verts] for g in group])
        lo = Vector([min(c[i] for c in co) for i in range(3)]); hi = Vector([max(c[i] for c in co) for i in range(3)])
        isl.append((f"{label_prefix}#{len(isl)}", co, bvh, lo, hi))
    bm.free()
for o in col.all_objects:
    if o.type == 'MESH' and not o.hide_render:
        add_islands(o, o.name)
n_asset = len(isl)
for a in ANCHORS:
    add_islands(bpy.data.objects[a], "ANCHOR:" + a)

parent = list(range(len(isl)))
def find(i):
    while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
    return i
def near(a, b):
    if any(a[3][k] > b[4][k] + TOL or b[3][k] > a[4][k] + TOL for k in range(3)): return False
    for src, dst in ((a, b), (b, a)):
        pts = src[1][::max(1, len(src[1]) // 300)]
        if any(dst[2].find_nearest(p, TOL)[0] is not None for p in pts): return True
    return bool(a[2].overlap(b[2]))
for i in range(len(isl)):
    for j in range(i + 1, len(isl)):
        if find(i) != find(j) and near(isl[i], isl[j]): parent[find(i)] = find(j)
grounded = {find(i) for i in range(len(isl))
            if i >= n_asset or (GROUND_Z is not None and isl[i][3].z <= GROUND_Z + TOL)}
floating = [isl[i][0] for i in range(n_asset) if find(i) not in grounded]
below = [isl[i][0] for i in range(n_asset) if GROUND_Z is not None and isl[i][4].z < GROUND_Z - TOL]
print(f"islands {n_asset}, floating {len(floating)}: {floating[:20]}")
print(f"entirely below ground {len(below)}: {below[:20]}")
```

Penetration audit (read-only; checks every pair of connected pieces in the asset, and each asset piece against the declared context objects, at the current frame on evaluated geometry). It finds surface crossings with BVH overlap, splits crossing edges, and tests sample points with ray parity to measure how deep one closed solid goes into another; it also catches full containment and coincident duplicates. Tested on: touching stack (clean), beam 5 cm into a wall, small cube hidden inside a big one, thin crossed slabs, coincident duplicates, a card through a box, a post 10 cm into terrain under a 0.15 m allowance; ~0.5 s for two 25k-triangle meshes.

```python
# Penetration audit: solid parts entering each other or their surroundings. Separate from contact/support.
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

COLLECTION = "ASSET_id"
CONTEXT = []    # objects the asset must coexist with in its assembled state: wall, table, terrain mesh, a character...
TOL = 0.003     # metres: deeper than this is penetration, shallower counts as touching
ALLOW = {}      # designed embeds by exact object names, max depth in m: {("Post", "Terrain"): 0.15, ("Pin", "Socket"): 0.02}
EPS = 1e-5

dg = bpy.context.evaluated_depsgraph_get()
pieces = []
def add(obj):
    bm = bmesh.new(); bm.from_object(obj, dg); bm.transform(obj.matrix_world)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    seen = set()
    for f in bm.faces:
        if f in seen: continue
        stack, group = [f], []; seen.add(f)
        while stack:
            g = stack.pop(); group.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h not in seen: seen.add(h); stack.append(h)
        vs = list({v for g in group for v in g.verts}); vi = {v: i for i, v in enumerate(vs)}
        co = [v.co.copy() for v in vs]; tris = [tuple(vi[v] for v in g.verts) for g in group]
        edges = {}
        for t in tris:
            for k in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
                k = tuple(sorted(k)); edges[k] = edges.get(k, 0) + 1
        pieces.append(dict(name=obj.name, label=f"{obj.name}#{len(pieces)}", co=co, tris=tris,
                           closed=all(n == 2 for n in edges.values()), bvh=BVHTree.FromPolygons(co, tris),
                           lo=Vector([min(c[i] for c in co) for i in range(3)]),
                           hi=Vector([max(c[i] for c in co) for i in range(3)])))
    bm.free()

DIRS = [Vector(d).normalized() for d in ((0.577, 0.578, 0.576), (-0.31, 0.83, -0.46), (0.71, -0.21, -0.67))]
def n_hits(p, point, d):
    n, o, far = 0, point.copy(), (p["hi"] - p["lo"]).length * 3 + 1
    for _ in range(512):
        loc = p["bvh"].ray_cast(o, d, far)[0]
        if loc is None: return n
        n += 1; o = loc + d * EPS * 10
    return n
def depth_inside(p, point):
    """Distance to the nearest surface if the point is inside closed piece p (3 parity rays agree), else 0."""
    if not p["closed"] or any(point[k] < p["lo"][k] or point[k] > p["hi"][k] for k in range(3)): return 0.0
    if {n_hits(p, point, d) % 2 for d in DIRS} != {1}: return 0.0
    return p["bvh"].find_nearest(point)[3]
def centroid(p): return sum(p["co"], Vector()) / len(p["co"])

def check(a, b):
    pairs = a["bvh"].overlap(b["bvh"])
    pts = []
    for src, dst, side in ((a, b, 0), (b, a, 1)):
        pts.append((dst, src["co"][0]))                       # full containment without surface crossing
        c = centroid(src)
        if depth_inside(src, c) > 0: pts.append((dst, c))     # coincident or nested duplicates
        for fi in {pr[side] for pr in pairs}:
            t = [src["co"][i] for i in src["tris"][fi]]
            pts += [(dst, v) for v in t] + [(dst, sum(t, Vector()) / 3)]
            for u, w in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):   # split edges where they cross dst
                L = (w - u).length
                if L < EPS * 40: continue
                d, cuts, trav = (w - u) / L, [0.0], 0.0
                while trav < L:
                    hit = dst["bvh"].ray_cast(u + d * trav, d, L - trav)
                    if hit[0] is None: break
                    trav += hit[3] + EPS * 10; cuts.append(trav)
                cuts.append(L)
                pts += [(dst, u + d * ((x + y) / 2)) for x, y in zip(cuts, cuts[1:]) if y - x > EPS * 20]
    return len(pairs), max((depth_inside(dst, p) for dst, p in pts), default=0.0)

for o in bpy.data.collections[COLLECTION].all_objects:
    if o.type == 'MESH' and not o.hide_render: add(o)
n_asset = len(pieces)
for name in CONTEXT: add(bpy.data.objects[name])
found = []
for i in range(n_asset):
    for j in range(i + 1, len(pieces)):
        a, b = pieces[i], pieces[j]
        if any(a["lo"][k] > b["hi"][k] + TOL or b["lo"][k] > a["hi"][k] + TOL for k in range(3)): continue
        crossings, deep = check(a, b)
        allow = ALLOW.get(tuple(sorted((a["name"], b["name"]))))
        if deep > max(TOL, allow or 0): status = "PENETRATION"
        elif deep > TOL: status = f"designed embed within {allow} m"
        elif crossings and not (a["closed"] and b["closed"]): status = "CROSSING, open/non-manifold mesh: depth unknown, inspect"
        else: continue
        found.append((deep, status, a["label"], b["label"]))
for deep, status, x, y in sorted(found, reverse=True):
    print(f"{status}: {x} <-> {y}, sampled depth {deep:.3f} m")
print(f"pieces {n_asset} (+{len(pieces) - n_asset} context), findings {len(found)}")
```

Reading the penetration result:
- The depth is the largest sampled distance from a point inside one solid to the other solid's nearest surface. It is not the axial embed length: measure a designed embed along its axis separately. Sampling can miss very small intrusions.
- "CROSSING, open/non-manifold mesh" means inside/outside can't be decided (cards, planes, open shells): inspect visually. Close the mesh or judge it by eye; never treat it as clean.
- Self-intersection inside one connected mesh is not tested. Other poses and frames need their own run.

Interpret results, don't just print them: every floating piece is fixed or justified in the ledger (e.g. a deliberately hanging part with its wire); every large never-visible group is removed or justified by the hidden-surface policy; every penetration is repaired or recorded as a designed embed with its pair and depth.

Export and verify:
- Export only the asset collection (exclude review stage, cameras, lights). Keep a source checkpoint before destructive optimization.
- Reimport the actual exported file into a separate temporary scene; compare dimensions, orientation, part count, triangles, materials and textures with the source; render the same review views and look at them. Then remove the temporary scene.
- Re-run affected visual checks after any optimization, bake or export setting change, and re-run the penetration audit on the reimported export with the same context objects.
- Don't claim runtime performance or in-engine appearance without testing in that application; if the user wants an application check, do it as a separate step.

## 8. Delivery

Deliver: editable .blend, the builder/recipe if used, requested exports and textures, the reference board, a few representative before/after and target/candidate comparison images, and a short status:

- Artistic acceptance against the target: pass / candidate / incomplete, with remaining defects.
- Source technical checks.
- Export verification.
- Application verification: done / not requested / not verified.
- What was inferred (hidden sides, unseen parts) and what was deliberately simplified or removed as never visible, with the camera range that justifies it.
- Interactions: context objects and poses checked, designed embeds with their depths, anything not covered (self-intersection, untested poses).

Never claim user approval, "AAA" or performance from internal review alone. Label intermediates honestly: concept, blockout, pilot, candidate, final.