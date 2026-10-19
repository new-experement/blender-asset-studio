# Visual acceptance and precise repairs

The reviewer exists to catch what the user would otherwise have to point out. Inspect actual images before evaluating the maker's explanation.

## Keep artistic quality and export fidelity separate

Label every comparison as **target-to-candidate**, **before-to-after**, or **source-to-export** and identify the role of each image. The artistic target is the selected reference/concept and quality benchmark from the brief. The current model or its export is not its own independent quality benchmark.

Source-to-export equality proves that the exporter preserved the candidate, even if the candidate is artistically poor. Pixel-difference metrics, triangle counts, successful renders and technical-audit results cannot close an artistic defect. A helper's generic “reference” label does not turn a source render into an artistic reference.

Before local crops, answer: does the whole candidate actually reach the selected design and finish at the intended viewing size? Compare silhouette, mass distribution, material hierarchy, condition and focal detail. If the whole looks like a placeholder, record a major quality issue even when component counts and dimensions match. Use the art-direction rejection criteria linked in SKILL.md.

## Capture a fair comparison

Record candidate revision, file path/hash, camera pose and lens/projection, framing, render size, lighting, exposure and color transform. Match the primary reference viewpoint where feasible without modifying the asset's proportions to fit the camera.

Use:

1. A whole-object comparison for identity, silhouette, composition and material distribution.
2. Reference-matched detail crops for corresponding semantic parts.
3. Opposing/top/underside views where relevant to the deliverable.
4. The intended viewing size and a close view.
5. Functional/extreme poses if the asset moves or deforms.

Grid tiles are locators. Compare the corresponding part even when it lies in different tiles in the two images. Do not compare a roof to empty background merely because both occupy tile B2. Match useful orientation and scale; do not warp the model image to conceal differences. Parts invisible in the reference are assessed for consistency and plausibility, not claimed as exact matches.

The comparison helper supports different normalized crop boxes in the two images. It preserves aspect ratios, labels each pair and displays alpha over a checkerboard. It produces inspection sheets, not a similarity score or an acceptance decision. Independently fitted crops can have different display scales; use recorded measurements or calibrated views for quantitative proportion checks.

## What to inspect

### Fast visual tests before local acceptance

Use the relevant tests on the whole candidate and its difficult pilot, then inspect corresponding semantic regions. Record an actual observation and any resulting repair; a checked box or a successful diagnostic is not acceptance. Keep source revision, camera, lighting and target role traceable.

| Test | Evidence and decision |
|---|---|
| Silhouette | A flat silhouette from 2–3 useful directions exposes wrong proportions, negative spaces and contour faceting. Preserve required alpha cutouts; an opaque material override alone cannot represent foliage or cards. Do not mistake recognition for correct material finish. |
| Value hierarchy | Inspect a grayscale and lightly blurred view: large, medium and fine masses should read like the benchmark. Use it to find uniform noise or lost focal contrast, then confirm in the original color render. |
| Target-size / thumbnail | Inspect at actual intended screen coverage and at the closest allowed view, without zooming to rescue unreadable features. Record what disappears, what matters and which geometry contributes no visible effect. Smaller display alone cannot excuse a target mismatch. |
| Scale | Place a known-size compatible object, ruler or human dummy where appropriate. Check doors, handles, supports, grain and fasteners against it; an unscaled reference photo does not supply exact millimetres. |
| Contacts | Inspect joins and supports after modifiers, including cavities exposed by damage. Use measured distances and the optional island/contact diagnostic in modeling discipline. Bounding-box overlap or a low minimum Z does not prove contact. Explain intentional suspension or separation from the brief. |
| Penetration / clearance | Inspect assembled interacting objects, not just isolated parts: hands/walls, furniture, clothing/body, doors/frames. Use section/x-ray/opposing views and required poses. Support-graph connectivity is not permission to occupy another solid. Distinguish intended bounded embedding, forbidden intrusion and required moving clearance; run the separate intersection diagnostic when useful. |
| Wireframe / density | Inspect evaluated topology at focal contours and broad flat surfaces. Look for excessive flat/hidden detail, faceted curves, duplicates and dense modifier output. Use candidate-unseen geometry diagnostics for investigation, not automatic removal. |
| Neutral light | Use a repeatable neutral stage with a fixed HDRI or light rig, exposure and color transform, plus the intended-use lighting. Materials must survive both; deep shadows, props or scenery cannot hide a weak pilot. |

Keep scale dummies, test stages, diagnostic material overrides and temporary reduced-detail copies outside the export. Record which states/views justify hidden-surface removal; keep shadows, reflections and required interfaces. See [modeling discipline](modeling-discipline.md) for operations and diagnostic limitations. If a test view is not relevant, record why rather than manufacturing an image ritual.

Walk every required region, recording inspected, needs-view, blocked or not-applicable.

For each inspected region, write a short paired observation before proposing a fix: **reference appearance → candidate appearance → difference → repair ID or pass rationale**. Describe visible contour, material response, localized variation and finish—not just object counts or the maker's intended features. Include normalized crop coordinates or landmarks so another pass can find the same part. A geometric pass does not imply a material pass for the same region. For an unseen reference side, state the chosen inferred target and check consistency; do not invent an observation.

| Region | Reference / agreed target | Current model | Difference and next action |
|---|---|---|---|
| Upper edge | Continuous thick lip, about twice the candidate's apparent thickness at matched scale | Thin edge; contact with the left support is interrupted | Measure shell and support contact; create separate thickness/contact repairs, preserve outer contour |
| Three lower fasteners | Three evenly spaced heads along the seam | Same count, spacing and placement in the matched crop | Pass for placement; material finish reviewed separately |

These observations locate the defect; the repair record below supplies executable numbers or an annotated contour. Do not skip whole-object judgment because individual tiles pass.

| Layer | Observable questions |
|---|---|
| Identity and silhouette | Right component count, mass ratios, contour, negative spaces and signature details? |
| Construction | Plausible thickness, loads, supports, joints, attachments and exposed internal surfaces? |
| Materials | Correct material assignment, scale, hue/value, roughness, metal response and transparency? |
| Condition | Finish matches the chosen age/use; wear has causes and localization; no unwanted pristine or uniformly noisy surfaces? |
| Detail | Important features present; small details help at target scale; no intersections, floating parts or accidental fragments? |
| Context | Contact with intended support; consistent neighboring scale/material response; no visible seams hidden by the studio render? |
| Function | Required pivots, gaps, contact points and extreme poses work? |
| Interactions | No forbidden interpenetration with other assets, self/clothing or nearby surfaces; required clearances survive poses, modifiers and assembly? Permitted embeds bounded and justified? |
| Production | Budget, topology, UVs, dependencies and actual exported appearance preserved? |

Surface condition is task-specific. Clean product visualization should remain clean; weathering is not a universal quality requirement.

## Defect record

Each actionable issue contains:

- Stable ID, severity, affected object/material/region, views and revision.
- Reference evidence and observed candidate evidence.
- Measurement origin: measured, estimated ratio, or artistic choice; uncertainty.
- Current value/structure and concrete target with unit and tolerance where meaningful.
- Exact operation and responsible layer (geometry, topology, UV, material, texture, lighting or integration).
- Invariants, expected observation and verification method.
- Status: open → planned → applied → verified; failed verification returns to open.
- For verified: fresh image/measurement paths and the candidate revision actually checked.
- For an artistic issue: target image/role, whole-object effect, and the observation that proves the intended visual change, separately from numeric compliance.
- For penetration/clearance: both objects, affected local region, frame/pose and context revision, measured or sampled depth/gap with uncertainty, allowed extent if any, and the evidence needed from each relevant view/state. A passing support audit does not close this issue.

Severity:

- **Blocking:** identity/major silhouette wrong, required part missing, unusable export or broken required behavior.
- **Major:** clearly visible reference/style/construction defect at the intended view.
- **Minor:** local imperfection that does not materially weaken the accepted target.

A numeric score cannot cancel a blocking or major defect. Maintain coverage even when the current repair pass focuses on only the highest-impact issues.

## Write executable corrections

Bad: "make the roof thicker."

Useful: "roof_panel thickness 0.018 m → 0.036 m (±0.002 m); move the lower shell along local −Z by 0.018 m while keeping the upper surface, pitch and eave outline fixed. Check cross-section measurement and the right-side render."

Bad: "make the concrete less white."

Useful: "The neutral-light test is too bright compared with the chosen target. Change surface Base Color from #D6D3C8 to #A9A393 (sRGB), roughness 0.50 → 0.82, metallic stays 0. Preserve the stain mask. Re-render with the same exposure/color transform; then inspect under the intended scene light." These example values are not defaults.

Bad: "improve the broken corner."

Useful: "Cut the upper outer corner along the annotated three-point contour in review/corner_target.png; retain the lower support and attachment face. Expose the cross-section with 30–50 mm irregular chips concentrated at the break, not every edge. Match the silhouette in the front/side crops and ensure the support still contacts the upper beam."

Use landmarks, ratios, vector displacements, angles, profiles, masks and annotated contours when scalar parameters are insufficient. The repair must be specific enough to execute, but cannot falsely claim certainty absent from the reference.

Material colors must identify encoding. If setting Blender node values in scene-linear space, convert sRGB channel c to c/12.92 for c ≤ 0.04045, otherwise ((c+0.055)/1.055)^2. Do not feed normalized sRGB values as linear values by accident. Numeric material changes are a hypothesis; confirm their visual effect.

## Loop discipline

Freeze the target and protected features. Pick the highest-impact coherent group, make the changes, capture again, then verify both the issue and adjacent/previously accepted features.

Write observations and repair plans when the review occurs. Close issues individually after inspecting their fresh evidence; do not bulk-mark all regions/repairs verified at handoff. Each materially changed candidate gets a new immutable revision ID. Keep the source/export hashes used by a comparison with its evidence.

Each pass must produce a real observation or a changed artifact. A rephrased self-critique is not progress. If the fix creates a more serious defect, revert to the best checkpoint and revise the approach.

After two non-improving attempts at the same important issue:

1. Identify whether the cause is form, material, lighting, projection, export or integration.
2. Choose one different method or diagnostic.
3. Use the remaining task budget; do not start a fresh unlimited loop.

Do not expand scope to compensate for poor execution. More props, more mechanisms, more random damage and more polygons are not automatically improvements. Before scaling a family or procedural placement rule, accept one representative result in its intended context. Internal acceptance is sufficient unless the user requested their own approval.

## Final acceptance

Inspect fresh evidence after the final relevant change. Earlier screenshots remain valid only for unaffected claims with an explicit reason. Optimizing geometry, rebaking, changing material export or modifying rig transforms requires affected checks again.

Artistic pass: the whole object and required regions meet the selected visual target/quality benchmark; no open blocking/major visual defects; any minor deviations are identified and compatible with the brief. It is not enough that every named part exists. If no visual target was resolved, report a design candidate rather than inventing retrospective acceptance.

Do not lower the benchmark to the best model produced so far. Budget pressure, hidden-side simplification, “game distance,” or successful export cannot relabel a still-visible major mismatch as a minor deviation. If an honest reclassification is justified by new target evidence, record that evidence and why it changes the judgment.

Technical pass: final file checks meet the agreed limits and required interfaces.

Application pass, if in scope: the actual asset is inspected in the requested environment. Headless logic tests, source renders or cloud screenshots from another renderer do not substitute for that evidence.

Stop within budget and deliver the best revision if unresolved. Say exactly what remains. Do not ask the user to perform ordinary visual inspection that the agent can perform itself. If the target environment is inaccessible, complete all available checks and describe only the remaining gap.
