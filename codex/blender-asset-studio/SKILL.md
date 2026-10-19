---
name: blender-asset-studio
description: Create or refine editable 3D assets through Blender MCP with reference intake, an optional initial Imagegen concept, autonomous modeling, and bounded visual acceptance against a selected quality target. Use for reference-matched props, vehicles, buildings, characters, asset families, or high-quality/AAA-like asset work with detailed self-review. Includes precise repairs, project-aware budgets, and separate export verification. Do not use for a concept image alone, ordinary engine programming, or a trivial export that needs no modeling review.
metadata:
  version: "1.3.0"
---

# Blender Asset Studio

Produce an editable model that withstands close comparison with its reference and intended viewing conditions. Own the work from intake to delivery, including the critical review the user would otherwise have to request repeatedly.

This is a self-contained production skill. Do not call another 3D-production or graphics-pipeline skill to execute it. All required workflow instructions are here and in the linked resources. Host-mandated instructions for specific tools still apply.

## Load only the current stage

| Stage | Read |
|---|---|
| Start or changed scope | [Intake and brief](references/intake.md) |
| Choose the visual target, concept route or quality bar | [Art direction and quality gates](references/art-direction.md) |
| Analyze references or fill a visual gap | [Reference preparation](references/references.md) |
| Build geometry, simplify hidden surfaces, check contacts or unwanted intersections | [Modeling discipline](references/modeling-discipline.md) |
| Every visual acceptance pass | [Review and repair protocol](references/review.md) |
| Set budgets, materials, topology or deformation requirements | [Technical profiles](references/technical-profiles.md) |
| Use helpers, export, or hand off | [Production and delivery](references/production.md) |
| Maintain/evaluate this skill | [Evaluation scenarios](references/evaluation.md) |

Reuse an existing task brief and ledger. The [working brief](assets/brief-template.md), optional [concept brief](assets/concept-brief-template.md) and [review ledger example](assets/review-ledger.example.json) supply formats; they do not certify acceptance.

## Non-negotiable behavior

- Preserve the user's scope, primary references and protected features. Project instructions and established asset contracts override this skill's fallback choices.
- Read applicable project guidance and inspect the actual reference pixels. A filename, a summary, or the builder's description is not visual evidence.
- For a new design, conduct the intake before substantive modeling: explicitly request user references/examples and offer initial concept art through Imagegen. Record the user's reference status and concept choice; answering a size question closes only the size question. Reuse explicit prior answers.
- Distinguish initial art direction from later gap filling. Initial concepts establish a target with the user's chosen review/autonomy mode; supporting generation then resolves specific uncertainties without repeatedly asking the user. Do not automatically generate every possible view.
- Never treat a generated view as stronger evidence than the supplied reference. Record invented structure as an inference.
- Separate maker and reviewer passes. A successful script, a low triangle count, or a polished narrative cannot pass the visual gate.
- Compare artistic quality against the visual target/quality benchmark, and export fidelity against the source. Source-versus-export similarity proves only fidelity. A basic shape with flat fill, random cuts or generic noise can fail even when every technical check passes.
- Every material criticism must lead to an executable repair: target object/region, observed evidence, measurable target or annotated shape, operation, protected constraints, and an acceptance observation.
- A repair is verified only from fresh evidence of the modified model. Retouched images are proposals, never proof of a 3D change.
- Allocate geometry by its visible or functional contribution across the allowed views and states. Check actual joins and supports after modifiers; a visibility/contact diagnostic supplies candidates for inspection, not permission to delete or a quality certificate.
- Check unwanted interpenetration separately from support/contact, including interacting assets and required poses. A hand through a wall or chair through a tabletop is a defect even if a contact graph calls the parts connected. Permit designed embedding only for a documented pair, extent and purpose; do not treat every intersection as either forbidden or automatically acceptable.
- Preserve the best checkpoint. Budget exhaustion means incomplete delivery with named defects, never automatic acceptance.

## 1. Discover and establish the brief

Inspect relevant project instructions, style references, existing assets, texture libraries, target dimensions, conventions and budgets. Record their paths and the origin of each constraint; do not copy one project's style or numerical limits into unrelated work.

Use [intake](references/intake.md). For an incomplete new-design request, normally ask one compact batch of 4–6 meaningful questions covering the missing artistic and functional choices. Do not manufacture redundant questions to meet a count. Fewer or no questions are justified only by recorded answers, including reference status and the initial-art route—not by project style alone or an agent's assumptions. Missing engine information does not block a standalone model.

Set a compact acceptance contract before expensive work:

- Reference authority, required views and semantic regions to inspect.
- User reference status, initial Imagegen choice, concept review/autonomy mode and resolved visual target.
- A quality benchmark and observable reasons the finished asset should meet it.
- Shape/proportion targets and any allowed design freedom.
- Technical limits, their source, and counting basis.
- Required export formats and application verification scope.
- Effort budget and stop/recovery rules.

Convert "AAA-like" into a concrete visual target: credible construction, intentional silhouette, convincing material response, controlled detail, clean finishing and consistency at the intended scale. Do not promise an industry label or substitute a numeric beauty score.

## 2. Check capabilities and preserve the scene

Discover the installed Blender MCP surface and its actual contracts. Start with read-only status/scene inspection: active file, Blender version, collections, units, existing work, tools and available render/image-generation capabilities.

Use MCP as the primary authoring connection. If unavailable, an installed local Blender can run an inspected builder in a separate process; disclose the fallback. If Blender cannot run, finish the independent brief/reference work and clearly identify the model stage as unexecuted.

Own a stable collection and output folder. Do not reset the user's scene, overwrite unrelated files, or delete other tasks' objects. Serialize mutations to a shared Blender instance. Heavy baking/rendering can use an isolated background process with controlled CPU/GPU usage. Do not start conflicting jobs against the same file.

For paid generators, new services, downloads with unclear rights, installations or external publishing, follow the user's authorization and host policies. Do not silently spend credits or add providers. A missing image generator does not block modeling when the available reference is sufficient.

## 3. Establish art direction, then fill specific gaps

Read [art direction](references/art-direction.md) and [reference preparation](references/references.md). Initial-art routes are: work from sufficient supplied references; generate a concept for user selection; generate and choose autonomously when delegated; or explicitly delegated direct-to-3D design. An unanswered art choice is not authorization. For a requested concept review, generate and show the concrete art before asking the user to select it; stop dependent detailed modeling until that selection. Do not add this checkpoint when the user already selected a design or delegated the choice.

Inventory the whole object and its meaningful regions: silhouette, primary masses, construction, attachments, materials and distinctive details. Define a visibility/detail map, including hidden surfaces that may be simplified. Approve a representative difficult area internally against the target before multiplying a family or finishing the entire asset.

Classify each important fact as observed, measured, inferred, or provisional. Infer unseen areas consistently with known dimensions and construction. If that inference could alter identity or a costly functional interface, resolve it before detailing.

After direction is resolved, request additional views/crops/material studies autonomously within the agreed scope and generation budget when they answer a named question. Check newly generated views against the invariant list. A concept is not a dimensionally reliable blueprint.

## 4. Build and accept in stages

1. **Blockout:** proportions, silhouette, scale, openings, contact plane and major parts. Check the reference-matched view and an opposing view.
2. **Construction:** thickness, supports, joins, negative spaces, moving parts, attachment points and internal surfaces exposed by requested actions. Read [modeling discipline](references/modeling-discipline.md) for screen-size decisions, hidden-surface rules, contacts and penetration/clearance checks. Inspect the assembled context and required poses; isolated parts cannot establish compatibility. Establish the allowed camera/state range before removing geometry.
3. **Materials and details:** use suitable project resources, adapting/baking or creating missing detail when the library cannot meet the target. Develop scale-appropriate material response and purposeful condition. A library texture or a noise node is not, by itself, a finished material. Add geometry where it changes visible shape or required deformation.
4. **Production:** UVs, appropriate baking, textures, material consolidation and topology reduction without losing protected features or functional structure.
5. **Delivery:** inspect the actual exported artifact, including changes caused by optimization and export.

Before each expensive downstream step, perform the relevant acceptance pass. A blocking silhouette, structural error or major material/quality mismatch keeps the asset at the current stage. Do not label a technically valid blockout as a finished asset. Independent useful work may continue while a different issue is being resolved.

Prove the difficult material/export path on a representative part before baking a large set. For families, accept a representative pilot before expanding, then review every materially different member and the family together.

## 5. Run the autonomous review/repair loop

Read [review and repair](references/review.md). Use this sequence for every meaningful revision:

1. Save a uniquely identified candidate and identify its source/export revision; do not overwrite a revision already used as evidence.
2. Capture comparable overview views, target-scale images and needed detail crops. Apply the silhouette, value, target-size, scale, contact, wireframe and neutral-light checks in the review protocol where relevant; record the finding, not merely that a test ran.
3. Review the whole object against the visual target before local tiles. Separately compare corresponding semantic regions and source/export fidelity. For every inspected region, describe the actual target pixels, candidate pixels and concrete difference or reason to pass. Mark unobserved regions explicitly.
4. Create/update the prioritized defect ledger with concrete repairs and evidence.
5. Fix the highest-impact coherent group of defects.
6. Capture fresh evidence, recheck the changed regions, adjacent contacts and protected features.
7. Keep the improved candidate or restore the better checkpoint; update the ledger and remaining budget now. Do not reconstruct a passing ledger only at handoff.

The reviewer examines the brief, primary references, current images and measurements before reading the maker's explanations. If separate agents are available and delegation is authorized, a read-only reviewer may return the defect ledger; only the designated maker mutates the asset. Otherwise perform a distinct sequential review. Do not pretend self-review is independent review.

Review does not require user approval at every stage. Continue autonomously within the brief. Ask only when a consequential ambiguity, new cost/access, missing essential reference or changed direction prevents the next useful action.

## 6. Stop based on evidence and budget

Use user limits first. Without limits, announce a provisional standard budget: up to four complete repair cycles after the initial candidate, two additional targeted repair passes, and at most three supporting image-generation calls. These are task-wide limits, not reset at each stage or after compaction. Unused cycles need not be consumed; task size may justify another explicit initial budget.

If initial art is selected, include its calls explicitly in the generation allowance before starting (default: up to two initial-concept calls plus the three supporting calls). A repair cycle is review → a coherent correction group → fresh inspection. A subsequent correction after that inspection is another pass, even if called cleanup or given the same version name. User steering can change the target; record the change and affected budget explicitly instead of restarting counters.

Two consecutive attempts that fail to improve the same important defect trigger diagnosis and one change of method within the remaining budget. Do not keep adjusting the same ineffective parameter or regenerate the whole object by habit.

Stop successfully when required regions and deliverables are inspected, blocking/major defects are resolved, technical gates pass, and any minor accepted deviations are explicit. Stop as incomplete when limits are reached or capabilities are insufficient. Preserve the best files and report unresolved defects without silently weakening the acceptance target.

Maintain brief, reference decisions, checkpoints and ledger in the task output directory so work can resume without repeating failed attempts. Keep user updates concise: current stage, meaningful finding, next correction and any changed limit.

## 7. Verify and deliver

Read [production and delivery](references/production.md). Compare final source and reopened/reimported export for dimensions, orientation, parts, material appearance, dependencies and required animation. Re-run affected visual checks after optimization, baking and export.

If requested, verify in the consuming application as a separate stage. A standalone model is complete after the artistic-target gate and agreed source/export checks pass; do not invent an engine project merely for acceptance.

Deliver editable source, reproducible builder/recipe where applicable, requested exports, required textures, effective reference-generation prompts, representative comparison images and the concise final defect/status record.

Report artistic acceptance against the selected target, source verification, export verification and application verification separately. Use candidate/draft status if the visual target is unresolved or major quality gaps remain. Do not downgrade a visible defect to a minor limitation to fit the remaining budget. Do not claim user approval, runtime performance or universal AAA quality from an internal review.
