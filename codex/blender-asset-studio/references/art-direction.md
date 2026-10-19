# Art direction and quality gates

Read before a new design and whenever a user says the result feels cheap, generic, too clean, too damaged or unlike the intended quality. These gates concern visual decisions; technical reports cannot replace them.

## Define what the asset should look like

Keep three distinct anchors:

1. **Design target:** shape, proportions, construction, material distribution and condition from selected references or a selected concept.
2. **Quality benchmark:** a visible example of the intended finish, material richness, form treatment and detail hierarchy. It can be an accepted project asset or a supplied game/render/photo example; say which aspects transfer. A photograph can guide material behavior without requiring that game's asset to reproduce every photographic detail.
3. **Constraints:** functional clearances, camera, project style, real scale and production budgets.

An overview mood board does not automatically define a particular object's design or quality. “AAA” is not an operational target until translated into observable criteria. Record 3–6 task-specific success criteria and the main ways a simplistic result would fail. Examples: a readable shaped silhouette; convincing joins and thickness; distinguishable material response; wear related to contact/exposure; coherent large, medium and fine detail; no procedural repetition at the intended view.

When the user has no examples and delegates selection, choose an appropriate visible benchmark from accepted project work or accessible reference sources. Inspect its actual pixels and record provenance; do not invent an unseen benchmark. If no suitable visual evidence is available, state the provisional quality assumptions and uncertainty rather than claiming externally benchmarked acceptance.

Do not infer a photorealistic or weathered style for every task. A clean stylized product can meet a high bar through designed curves, edge treatment and controlled material response. Match the selected benchmark, not the skill author's taste.

## Initial concept route

The intake establishes whether to use Imagegen and who chooses the result. Do not silently bypass this stage because it adds an image-generation call. If the user selected existing references or direct-to-3D work, honor that choice.

Before generation, prepare a concise art brief: subject/function, dimensions and ratios, style, condition, constraints, prohibited additions, intended camera and the uncertainty the board resolves. Use [the concept brief template](../assets/concept-brief-template.md) when helpful. Pass actual supplied images to the image tool when using them, rather than relying on their filenames. Follow host image-tool and skill instructions.

A useful initial board usually contains one strong three-quarter view, the additional top/side/opposing view necessary to understand the form, and one close-up of the difficult material or junction. Choose views for the asset; do not demand all six directions by default. For a family, show the common construction and meaningful variant differences coherently. Keep presentation lighting inspectable and avoid scenery hiding weak parts.

Check the board before showing or adopting it:

- Same counts, proportions, handedness, openings, support positions and material boundaries across views.
- Required function and interfaces remain possible; no attractive but impossible connections.
- User exclusions remain intact, even when a reference contains those excluded features.
- The image actually provides a stronger visual target than a plain box, rather than merely adding cinematic lighting.

Reject or repair contradictions; never silently treat inconsistent generated views as reliable blueprints. Save prompt, source roles, outputs and selection status. Label the board generated, and distinguish user-selected from agent-selected under delegation.

When concept review was requested, show the completed board and wait for direction selection before detailed modeling. If the user delegated selection, perform that selection internally and continue. Once direction is resolved, only generate further views/materials for specific unresolved regions, without repeatedly returning ordinary decisions to the user.

## Reference transfer without accidental redesign

Annotate what each source contributes and what is excluded. A reference may demonstrate broken fibers, a thin slab, surface staining or how a path meets a structure without authorizing its railing, water, vegetation, color scheme or exact scale. Current task requirements outrank incidental reference contents.

For damage, infer cause and material behavior: wood splits and tears with fibers and joints; concrete loses cover, exposes aggregate and fractures through volume; thin metal bends/tears differently from masonry. Local shape, exposed interior, edge shading and deposited dirt must agree. Random polygon bites, identical scallops, flat dark lines and neat repeated holes are weak substitutes when the target calls for natural material failure. Do not add reinforcement, debris or damage merely to decorate the model.

## Representative visual pilot

Before polishing an entire object or expanding a family, make the hardest visible representative section: for example, a curved panel and its join, a damaged edge and exposed cross-section, or a character's face and skin material. Include enough neighboring structure to judge scale and contacts.

Inspect it against the design target and quality benchmark under comparable neutral light and the intended viewing conditions. The pilot needs to prove the intended material/geometry/export method, not just that the script runs. If it still resembles a blockout with a texture or a flat surface with drawn-on defects, stop expansion and repair the method. Use a better mesh treatment, suitable source textures, local masks/decals, sculpt/bake workflow or a targeted material study as appropriate; more random noise is not a default remedy.

The pilot is normally an internal acceptance gate. Do not ask the user to debug it unless a genuinely new design decision is required.

## Stage gates

| Gate | Required evidence | Reason to keep working |
|---|---|---|
| Direction ready | Selected reference/concept or explicitly delegated design, quality benchmark, protected features and visibility priorities | Only dimensions or a genre label are known; reference/art choice is pending. |
| Form ready | Whole object and key opposing view at useful scale; major joins and interfaces | Proportion, silhouette, thickness, support or spatial logic is wrong. |
| Pilot ready | Matched target/current crops plus neutral and intended-view renders | Materials look generic/plastic, damage looks cut by a stencil, repetition or joins expose the procedural recipe. |
| Candidate ready | Full asset and each materially different variant, with visible surfaces covered | Good local details do not form a convincing whole; a large blank area or wrong condition dominates. |
| Delivery ready | Candidate passes artistic gate; final source/export comparison passes fidelity; requested application checks are separate | Matching GLB merely preserves a visually weak candidate, or a final optimization undoes the visual result. |

Never trade away the largest visible quality defects to make time for hidden detail, report decoration or additional beauty renders. Hidden surfaces may be simplified when they do not affect visible silhouettes, shadows, openings, reflections, required interactions or manufacture. Spend saved effort on visible form and materials.

## Reject weak results concretely

Reject a candidate when a major target-relative discrepancy is visible, such as:

- Unshaped primitives with uniform bevels where the target has specific contours and transitions.
- Flat or uniformly noisy materials where the target has readable layers, roughness variation and localized wear.
- Repetition at identical intervals, mirrored damage or equally sized holes without a design reason.
- Cracks with no surrounding breakup/shading when the target shows volumetric fracture.
- Clean planar cutouts and uniformly sharp broken edges where the material should splinter, crumble or deform.
- Inconsistent detail scale: giant grain, miniature stones, paper-thin members or a surface texture that implies the wrong construction.
- A hero render that depends on darkness, distance, props or scenery to conceal these issues.

Describe the target and current pixels, identify the cause, and write a measurable repair. Do not apply the list indiscriminately to deliberately simplified styles. Do not call a major mismatch “subtle at game distance” if the agreed target still differs at that distance.

If the quality gate remains failed at the effort limit, deliver the best candidate as incomplete with the visible deficits and next method. A low polygon count and a long acceptance report do not authorize “finished,” “high quality” or “AAA.”
