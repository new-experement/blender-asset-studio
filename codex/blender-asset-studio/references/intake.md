# Intake and autonomy contract

Use the user's language. Resolve the artistic choices early, then own ordinary production decisions.

## Discover, but do not substitute assumptions for answers

Read project guidance, existing briefs, style examples, models, texture libraries and export conventions. Inspect referenced pixels and the current model if editing. A project style guide can answer palette or camera conventions; it does not necessarily answer this asset's shape, condition, desired quality or concept route.

Keep a small intake table: topic → explicit answer/source → unresolved choice → next action. Distinguish **answered**, **pending**, **explicitly delegated** and **not applicable**. Confirmation of dimensions does not confirm a reference choice, damage level or permission to generate a concept.

## Required opening question: intended use

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

## First exchange for a new design

Normally ask one compact batch of 4–6 nonredundant questions. Ask fewer when actual prior answers cover the topics; do not pad the count. Cover these decisions, adapting examples to the task:

| Topic | What the question must resolve |
|---|---|
| Intended use (required) | Ask the opening question above with relevant example answers; resolve placement, interaction, visible sides and required states before detail/simplification or motion decisions. |
| Subject and function | What is being made, key dimensions, compatibility and variants. |
| User references and examples | Explicitly ask for images, links or existing assets and what the user likes about them: form, material, condition, detail or overall quality. “You may attach something if you want” buried after a size question is insufficient. |
| Character and condition | New/maintained/aged/damaged, extent and location of damage, repairs, asymmetry, period or style where unresolved. A genre does not define the exact amount of damage. |
| Viewing priorities | Closest view and screen size/FOV, allowed elevations/azimuths, important and hidden sides, focal details, ground/embed/mounting surface. Resolve whether opening, lifting, flipping, entering or destruction exposes concealed parts. Reuse established camera/state facts rather than asking again. |
| Initial art and review mode | Explicitly offer an artistic concept/reference sheet through Imagegen before 3D, and establish who chooses the direction. |
| Quality and scope | What visual examples define success; required source/export, interaction, deadline or effort limits if missing. Obtain technical budgets from project evidence when possible. |

A natural reference request is: “Please share 1–3 examples of the desired appearance or quality, and explain what to take from each: shape, materials, or condition. If you have no examples, say so.” Existing accessible attachments satisfy this request; inspect them, do not ask for duplicates. Use attachment-capable chat for requesting images, not a text-only input tool. Respect the host's message-channel rules.

The art question should give a concrete proposal, for example: “Should I first prepare an Imagegen concept with an overall view, the necessary projections, and a close-up of the key detail?” Offer the applicable routes:

- **Concept for selection:** generate and show an inspectable board, then let the user select/correct the direction before detailed 3D.
- **Autonomous concept:** the user delegates creating, assessing and selecting the concept; continue without another approval round.
- **Existing references / direct 3D:** use adequate supplied references, or direct design if the user explicitly chooses to skip concept art. Record which applies.

Do not infer an Imagegen choice from silence or a reply about size. Do not ask again if the user already requested concept generation or chose a route. If generation is unavailable, disclose that and offer a viable reference/sketch route; do not substitute a paid provider silently.

For a complete brief or a narrow edit to an approved asset, reuse the existing direction and ask only about the change. An export-only request needs no new art intake.

## Before substantial modeling

Proceed when these are resolved, not merely written down as agent assumptions:

1. Intended-use contract (explicit answer or explicit delegation), function, protected features and significant compatibility dimensions; include visibility and separate/moving-part implications.
2. References supplied, explicitly absent, or an existing accepted reference set selected.
3. Initial-art route and review/autonomy choice.
4. Visual target: selected references/concept, or an explicitly delegated provisional design plus a stated quality benchmark.
5. Applicable constraints, intended views and bounded effort budget.

While waiting for required choices, read files, measure existing assets, inspect capabilities, select candidate materials and draft the proposed art brief. Do not treat elapsed time as authorization or turn an exploratory blockout into the final design.

If the user selects concept review, complete and show the actual concept before requesting selection. This is one meaningful visual checkpoint, not permission for each modeling step. If choice is delegated, record the selected concept and reasons, then continue autonomously.

## After intake

Summarize the resolved brief once. Decide modeling method, hidden construction, UVs, suitable materials, exact damage placement within the selected range, corrective work and diagnostic views autonomously. Routine supporting references and textures within authorized scope/budget do not need repeated questions.

Ask again only for a consequential identity/function conflict, a missing essential reference or interface, a change outside the agreed scope, new cost/access, or a genuine quality/budget tradeoff. Never ask which obvious defect to repair or whether to continue necessary inspection.

User corrections become constraints and regression checks. Reopen only affected decisions; do not restart the interview. Do not expand the design to compensate for poor finish.

## Defaults and communication

For unspecified standalone work, deliver an editable model and useful interchange/preview files. Do not add an engine project, controller or level merely to demonstrate it. Derive numerical defaults from use and label them provisional.

Announce the effort budget, including initial-art calls if selected. Keep a running record rather than reconstructing it at the end. Report the meaningful visual finding and next correction. Show intermediates honestly as concepts, blockouts or candidates. Silence is not artistic approval.
