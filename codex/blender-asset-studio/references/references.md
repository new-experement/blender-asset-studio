# Reference analysis, initial art and gap filling

## Authority and invariants

Assign each source a role: primary shape, material/finish, functional construction, scale, mood, quality benchmark, existing accepted model, or generated hypothesis. Record both what transfers and what must not transfer. Keep the original pixels unchanged. Explicitly request user examples during intake; project mood imagery alone does not establish the asset's design.

Before modeling, list the characteristics that identify the object: silhouette, mass ratios, openings, component count and placement, distinguishing details, material distribution and condition. Record which are observed, measured, inferred or provisional.

Build a semantic region map. Examples are roof, openings, supports and joins for a structure; body, wheels, cabin and equipment for a vehicle; face, torso, limbs and clothing for a character. Choose regions appropriate to the object, not a universal checklist.

## Two different reasons to generate

**Initial art direction:** when selected during intake, generate an artistic concept/inspectable reference board before detailed 3D. This can establish the whole intended object, rather than only a hidden component. Use the art-direction guide linked in SKILL.md and respect the user's concept review/autonomy choice. This stage is not automatically authorized by an unanswered proposal.

**Supporting production studies:** after the direction is selected, generate to answer a named uncertainty, such as:

- A wall hides a connecting bracket.
- Only the front is visible and the rear must be delivered.
- A small crop does not reveal a mechanism's construction.
- A specific surface treatment needs a material study.

A sufficient selected reference needs no extra generation unless the user requested it. An initial multi-view board is useful when needed to settle design; later full turnarounds are not automatic. Do not consume the generation budget making attractive alternatives to an already fixed design.

Use an available image-generation/editing capability for new creative raster pixels. Follow host-required tool instructions. Missing generation can be handled with dimensions, a simple structural sketch or a clearly inferred blockout if sufficient; do not install a paid generator silently.

## Supporting generation prompt

Provide:

- The actual primary image and its role.
- The specific unknown region/question and the requested view.
- Fixed dimensions or ratios, axes and named component locations.
- The invariant list and protected colors/material assignments.
- What may be inferred and what must not change.
- Neutral inspectable lighting, no explanatory background unless necessary.
- A request to preserve already established geometry.

Save the effective prompt, inputs, output, consistency checks and inference/selection decision in the task folder. A generated reference stays labeled generated even after selection. It is not presented as a source photograph, measured orthographic drawing or user approval when selected by the agent.

## Consistency check

Check every generated view against common anchors: component counts, wheelbase, opening heights, handedness, seams, support positions and material boundaries. Check impossible intersections and mechanical connections. Front and rear views must use the same dimensions.

If views conflict, retain the primary source and correct/reject the auxiliary view. Do not average incompatible designs into a third unrequested object. One retry or a structural interpretation is often more useful than repeated full-image regeneration.

Once blockout proportions are stable, its own unretouched renders can anchor additional visual studies. A paintover may propose a change, but the corresponding geometry/material must subsequently be updated and re-rendered.

## Measurements and uncertainty

Use known dimensions to calibrate ratios. Distinguish an image-space measurement from a physical measurement: perspective, foreshortening, lens distortion and unknown scale matter.

Write targets with units/coordinate space and reasonable tolerances. Do not invent exact millimeters from an unscaled image. For example, record "post width ≈ 0.08–0.10 of opening width, inferred" before choosing a concrete production dimension.

Do not sample a lit reference pixel and automatically assign it as albedo. Separate illumination, exposure, roughness and surface color. Review material candidates under comparable lighting and neutral light.

## Additional textures

Inspect the project library first. Reuse depends on visual suitability, not mere availability: verify construction cues, scale, color, roughness and damage. A clean wall material does not become a convincing damaged road merely because both are concrete. Adapt source maps or add a mask/decal/bake when required; if the library cannot meet the target, create the missing material within the authorized scope. Never apply an object-specific UV atlas as an arbitrary tiling surface.

Generate a texture only when missing source detail prevents the intended result. Declare whether it is a seamless surface, decal, mask or object atlas, its real scale and color/data interpretation. Check tiling, UV alignment, channels and minified appearance. Do not infer physically accurate height/roughness from color without labeling that approximation.

Renders, reference sheets and texture masters remain separate from runtime exports.
