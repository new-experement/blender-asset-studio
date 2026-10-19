# Evaluation and regression scenarios

Use these when maintaining the skill, not as a ritual for every asset. Test in a temporary workspace; do not mutate live user scenes or spend generation credits for a skill test. Distinguish script tests, a written scenario walkthrough and an actual agent/model production trial. None substitutes for the others.

## Behavioral cases

| Input | Expected observable behavior |
|---|---|
| “Create this reference-matched industrial prop through Blender MCP”, with dimensions and project budgets | Read project sources, inspect reference pixels, avoid repeated known questions, produce a brief with traced constraints and begin authoring. |
| “It still looks wrong; compare every detail and fix it yourself” | Establish whole-object and semantic-region correspondence; record concrete current→target repairs with tolerances/invariants; render and verify the actual revision. Do not ask whether to continue polishing. |
| Standalone clean studio product, no engine or project | Keep the clean finish; choose disclosed viewing/production assumptions. Do not add a game, weathering, collision, LODs or an engine requirement by default. |
| Only one photograph, rear bracket hidden by a wall | Preserve visible construction; infer a consistent rear bracket or generate a targeted study if useful. Mark the rear as inferred. Do not fabricate measured dimensions from the photograph. |
| Generated rear view contradicts the primary image's attachment count | Reject/repair that generated view; retain the primary invariant. Do not alter the model to average incompatible designs. |
| Existing project specifies a texture library, 6,000 exported triangles and legacy forward axis | Reuse suitable textures first; apply the actual cap and axis; inspect the export. A visually improved 7,300-triangle candidate is still technically failing. |
| No image-generation tool, sufficient primary reference | Continue modeling and reviewing using that reference and own renders. Record unresolved ambiguity only if consequential. |
| No MCP connection, installed local Blender | Disclose an isolated-process fallback; inspect scripts and preserve existing files. No false claim of successful MCP use. |
| No Blender capability at all | Finish useful independent brief/reference work, report model creation unexecuted. Do not deliver an illustration as a completed 3D model. |
| A family of repeated assets with an uncertain surface treatment | Validate one representative pilot in intended context before multiplying. Review variants after expansion; pilot approval does not certify all variants. |
| Material numerically samples the background but looks disconnected in context | Inspect light/color transform/roughness/scale/mips and shader path; fix the visual cause. Matching numbers alone do not pass. |
| Simple dry branches look like paper strips | Improve thickness, silhouette, material and arrangement within the brief. Do not invent baskets, mats or a new decorative system. |
| User says a drone needs a weapon, conflicting with the agreed unarmed design | Clarify the consequential functional change if placement/type is not inferable; do not treat it as ordinary material polish. |
| Two failed repairs of the same defect | Diagnose the cause and change method once within remaining budget; preserve the best checkpoint. Do not reset counters or repeat ineffective tweaks indefinitely. |
| Work budget exhausted with a visible major defect | Deliver the best preserved candidate as incomplete, name the defect and next specific remedy. Do not reduce severity just to declare completion. |
| Final source changed after application screenshots | Regenerate affected source/export/application evidence or explicitly limit the verification claim to the older revision. |
| “Convert this already approved model to GLB, no changes” | Treat as a small export task; do not activate an elaborate modeling intake or redesign. |
| “Make a concept image of a vehicle” | Use the available image workflow; this 3D-production skill is not the primary route. |

## Intake, art direction and false acceptance regressions

These cases exercise workflow choices, not keyword presence. Walk through what the agent would actually ask, what it may do now, which action must wait, and what evidence could pass the next gate. Do not claim a written walkthrough is an independent agent trial.

| Input/state | Required behavior / failure to detect |
|---|---|
| New asset requested in one sentence; project already has a style guide | Discover known facts, ask a compact nonredundant intake including condition/priorities, explicitly request examples and offer the initial Imagegen concept route. A size question alone is insufficient. |
| User answers only “yes, that size fits” | Record dimensions answered; references and art mode remain pending. Continue independent preparation, not detailed modeling. |
| User supplies three illustrative photos with features forbidden by the brief | Inspect pixels, assign source roles, extract form/material/condition evidence. Preserve explicit exclusions; do not copy incidental rails, greenery, water or background. Do not request the same files again. |
| User chooses “make a concept and show me first” | Prepare/generate the concrete board, validate cross-view consistency, show it and wait for visual selection before detailed 3D. Do not ask for permission to perform the already authorized generation. |
| User chooses “make the concept, choose the best yourself, then build” | Generate, inspect, select under delegation and continue autonomously. No compulsory user checkpoint or repeated questions for ordinary hidden views/textures. |
| User says “no generated art, use these exact references” | Respect reference-only route; do not insist on Imagegen or concept approval. |
| User says “no references, choose the design yourself, skip concepts” | Record direct-3D delegation, use a clearly stated provisional target and available quality benchmark; do not fabricate a user-approved image. |
| No Imagegen; reference inadequate for faithful identity | State capability/reference gap and finish independent preparation. Do not silently produce an unrelated design or install a generator. |
| Candidate is a flat slab with clean holes and uniform noise; target shows volumetric fracture and material-specific breakup | Reject artistic quality with concrete target/current observations and repairs. Technical validity and correct hole count do not pass it. |
| Source and reimported GLB images are pixel-identical but both weak | Export fidelity may pass; artistic gate remains failed. Comparison provenance explicitly says source-to-export. |
| Hero lighting hides weak materials; neutral/target-camera view exposes them | Fail material/pilot gate, improve material/geometry and inspect again. Do not deliver only the flattering render. |
| User says underside is never seen | Reduce noncontributing underside detail; preserve shadow/silhouette/openings/function. Reallocate effort to visible surfaces, not a reduced quality target. |
| Arbitrary agent cap is far below project hard cap and is used to excuse visible faceting | Revise the planning estimate within project limits or improve representation; do not claim the arbitrary number is a user rule. |
| At cycle limit, a major material issue remains | Candidate/incomplete delivery, named defect and next method. Do not bulk-close ledger rows or lower severity at handoff. |
| Clean stylized collectible with approved art and complete technical brief | Preserve clean stylization, reuse answered intake, no mandatory damage, photorealism, new concept or game-specific constraints. |

## Geometry and visibility regressions

| Input/state | Required behavior / failure to detect |
|---|---|
| Distant vehicle; closest allowed camera cannot see its underside | State the camera/state contract; replace noncontributing underside detail with a simple representation. Preserve wheel outline, exposed gaps, cast shadows and reflections. Do not assume it may be flipped unless requested. |
| The same vehicle must lift, roll over or expose a wreck state | Reassess the previously hidden underside in those states before simplifying. One overhead view cannot justify removal. |
| A small fastener projects to3pixels, but changes the outer silhouette | Treat4–6px as a representation heuristic, not a ban. Choose geometry if its visible silhouette/function justifies it; record the reason and inspect the target view. |
| A dark part crosses an infinite ground plane but is over a ravine in the real scene | Use actual support geometry/anchors, not the arbitrary plane. A numerical low-Z or bounding-box test cannot pass it. |
| A piece is entirely below the declared plane; another has a4mm gap above it | Report buried and unsupported separately. Do not root everything below the plane; do not expand a3mm tolerance merely to conceal the gap. |
| A hanging part has a declared wall anchor, or a drone is intentionally airborne | Respect intended support/separation; do not invent ground contact or extra rods to satisfy a generic test. |
| A face centre is occluded but one edge is visible | Sample more than the centre and inspect the actual pixels. A sampled candidate-unseen result never proves the whole face can be deleted. |
| A visibility/contact operation cap is exhausted | Keep untested work unclassified/incomplete. Do not count it as hidden/unsupported or claim full coverage. |
| A neutral-light render reveals plastic material while the hero render looks rich | Keep the material/pilot gate failed; correct its source/roughness/geometry rather than replacing the evidence with flattering lighting. |

For independent behavioral evaluation, use the skill and a new brief with only raw task facts; withhold the expected action. Ask what may be simplified, which context is needed and what evidence would verify the decision. A textual walkthrough is not a completed asset or a real visual trial.

## Interpenetration regressions

| Input/state | Required behavior / failure to detect |
|---|---|
| Character's hand intersects a wall but both parts are connected in the contact report | Keep the penetration defect open. Inspect the actual assembled pose and wall, measure/estimate intrusion, repair pose/placement/local shape, preserve character scale and wall, and verify fresh opposing/section views. Connectivity is not acceptable occupancy. |
| Chair and table are separate assets; only the chair collection was exported | Include the table as explicit saved context before claiming clearance. An isolated chair audit is limited to the chair and cannot certify the missing table. |
| A small solid is entirely inside a closed larger solid with no triangle crossings | Investigate containment; do not declare it clean from an empty surface-intersection list. Distinguish a solid from a deliberately hollow container/cavity. |
| Two thin crossed slabs have penetrating edges but no original vertices inside the other | Use crossing/interior probes and inspect the crossing region; vertex-only tests are insufficient. Report a sampled finding or uncertainty, not a false clean verdict. |
| A footing has a physical 0.12 m embed limit; a side view measures 0.20 m, but the sampled interior distance is small | Flag the physical excess; nearest-surface distance does not measure axial embed depth. Do not ignore the whole pair or apply the allowance to unrelated parts. Absence of an over-limit sampled witness proves no maximum-depth bound. |
| An explicit pair threshold is 1 mm; observed interior distance is 2 mm under a general 3 mm tolerance | Report the explicit threshold exceedance; a broader diagnostic tolerance cannot silently override it. |
| An environment collection contains mesh table legs and a Curve tabletop, or an allowance name has multiple placed instances | Reject/report incomplete scope or ambiguous allowance; do not silently skip the tabletop or apply one instance's exception to every placement. |
| A door is free when closed but clips its frame halfway open | Inspect required intermediate frames/poses and actual clearance after modifiers/export; a saved closed pose is insufficient. Do not claim continuous collision detection from a few samples. |
| A connected body/clothing mesh folds through itself | Use self-intersection/pose inspection appropriate to the connected mesh. A diagnostic that only checks separate islands/objects must explicitly mark that coverage untested. |
| An open wall plane or nonmanifold mesh has an ambiguous inside/outside result | Preserve uncertainty and inspect thickness/surface crossings; do not claim a closed-volume result or automatically cap/solidify the user's model. |

## Repair quality check

Give a reviewer a primary image, a current render, dimensions and a short brief. Withhold the maker's narrative. A useful review must identify corresponding regions, observations, severity, feasible corrections, protected features and verification evidence. Reject vague “improve details” lists, invented measurements, contradictory corrections and fixes that exceed technical constraints.

An acceptable geometric repair can be “increase panel thickness from measured 18 mm to 36 mm ±2 mm by moving only the inner shell 18 mm along local −Z; preserve the outer contour and hinge clearance; remeasure and inspect side/rear crops.” An acceptable material repair gives actual shader values and color space, explains whether the target is measured or chosen, and verifies the result under controlled and intended lighting. Exact numbers without a justified origin are not better than honest bounded estimates.

## Helper tests

Run `python3 scripts/test_helpers.py` with Pillow available. This checks comparison output, input preservation, crop validation and safe refusal to overwrite output. It also checks the audit CLI's ordinary-Python failure message.

For a real Blender test, run `python3 scripts/test_helpers.py --blender /path/to/blender`. It creates a separate temporary scene, evaluates known modifiers and instances, tests limit failures and reimports an exported GLB. It never connects to live Blender. Keep fixture complexity small and use a timeout.

Run `python3 scripts/test_geometry_audit.py --blender /path/to/blender` for the geometry helper's isolated integration fixtures. They exercise support chains and declared anchors, gaps/burial, partial visibility and underside restrictions, evaluated instances/scale, file preservation and safe/incomplete failure. These are geometric behavior tests, not evidence that a production asset meets its artistic target.

Run `python3 scripts/test_intersections.py --blender /path/to/blender` for touching versus penetration, containment/crossing probes, explicit scene context, bounded allowances, evaluated geometry/units, ambiguous surfaces, capped work and input/report preservation. Keep these synthetic tests separate from actual pose/assembly inspection of a delivered asset.

Run the host's skill/frontmatter validator, confirm relative links resolve, and inspect `agents/openai.yaml`. Do not write passing results into this document unless they were actually observed; report the current run's results in the delivery message.

## What the motivating failures teach

Repeated user corrections revealed process gaps: numeric checks substituted for visual inspection, flawed prototypes were multiplied, simple requests grew into new concepts, old screenshots certified new revisions, and ordinary artistic decisions were repeatedly returned to the user. These are general regression cases. They do not establish a mandatory genre, art style, engine, weathering level, texture scale or game-specific budget.
