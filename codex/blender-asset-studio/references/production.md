# Production, helpers and delivery

## Working package

Keep a task-local package with the brief, reference decisions, current ledger, source, exports, textures, comparisons and checkpoints. Use stable asset IDs and increasing revision IDs. Record the actual paths in the brief. Do not duplicate a project's existing asset structure unnecessarily.

Also preserve the resolved intake, initial-art choice, selected visual target/quality benchmark and concept selection evidence when applicable. Keep target-to-candidate artistic comparisons separate from source-to-export fidelity comparisons. Write the ledger during reviews, not as a retrospective checklist.

Preserve source ownership, pivots, units, axes, hierarchy, UVs, material assignments, sockets and requested animation. Treat origin placement and assembly interfaces as part of the contract. Select export objects explicitly; exclude presentation lights, cameras and review geometry unless requested. Resolve linked dependencies deliberately. Keep a source checkpoint before destructive optimization.

Prefer parameterized, resumable builder steps with stable object IDs. After a tool timeout, inspect scene/file state before retrying: the operation may already have completed. Avoid duplicate objects and repeated transforms. Save checkpoints at useful stage boundaries; split long jobs so a failed bake does not require rebuilding the asset. Use an isolated process for costly operations when supported, and batch inspection to avoid repeatedly stealing application focus.

## Comparable views

Render through the discovered Blender MCP capability or a separate background Blender process. Capture real model pixels. A viewport can reveal geometry quickly; use material/render views when judging shading. Pair the reference view with an equivalent camera; add orthographic views for dimensions and other views for hidden construction. Record focal length or orthographic scale, framing, light, exposure and color transform.

The comparison helper needs ordinary Python with Pillow. Check availability first; if absent, use existing image-viewing/cropping capabilities or the host's normal dependency process. Do not install packages automatically merely to use a convenience helper.

For artistic review, the reference input is the selected target/benchmark image; for fidelity review, it is the source render. Record this distinction beside the helper output because the helper's generic labels do not establish a source's role. A matching source/export contact sheet cannot pass the artistic gate.

```bash
python3 scripts/compare_views.py --reference source.png --candidate r03.png --output comparison-r03 --regions regions.json
```

Run from this skill directory, or resolve the script path against it. `--output` must be a new directory. Example `regions.json` (normalized image coordinates, origin at top left):

```json
[
  {"id": "roof", "reference": [0.12, 0.08, 0.88, 0.38], "candidate": [0.15, 0.1, 0.86, 0.4]},
  {"id": "left_mount", "reference": [0.05, 0.4, 0.3, 0.8], "candidate": [0.08, 0.42, 0.32, 0.83]}
]
```

The helper produces an overview, separately addressable paired crops, a contact sheet and provenance JSON with input hashes and crop boxes. It letterboxes without distorting aspect ratio and shows transparency over a checkerboard. Open the resulting images and actually inspect them. It does not align cameras, assign semantic correspondence, calculate perceptual quality or pass the asset. Choose the crop boxes from observed pixels; correct camera mismatch before interpreting a shape difference. The output is an analysis artifact, not an edited reference or delivery render.

## Technical audit in an isolated process

`scripts/audit_blender_asset.py` runs **only in background Blender**, never inside the user's live MCP session. Use the installed Blender executable and its documented command-line flags. Example:

```bash
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/audit_blender_asset.py -- --input model.blend --collection Asset --output audit-source.json --max-triangles 10000 --max-materials 2 --max-texture-edge 1024 --require-uv
```

Audit the requested export separately, after writing it:

```bash
blender --background --factory-startup --disable-autoexec --python-exit-code 1 --python scripts/audit_blender_asset.py -- --input model.glb --output audit-export.json --max-triangles 10000
```

Only pass constraints that apply to this asset. The helper reads `.blend`, `.glb` or `.gltf` and writes a new JSON report. It does not save or modify the input. `.blend` scope is the named collection (including children) or the scene; choose a collection for files containing unrelated assets. It audits mesh instances in the active view layer's **viewport dependency graph** at the saved frame, filtered by object render visibility and instance `show_self`. It measures their bounding box, triangles, material assignments, UV presence, transforms and image textures, including textures inside node groups. Geometry Nodes instances exposed by that graph are counted; unresolved procedural/export behavior still needs inspection. Differences between viewport and render modifiers are flagged. Collection visibility and viewport exclusions can also differ from final export scope: this is a preliminary source audit, not a renderer prediction. Report limits refer to counted instances, not only unique meshes. Hidden variants, other animation frames and LOD configurations require separate runs/captures.

The helper reports findings, not full production acceptance. It cannot prove silhouette quality, correct normals/UV distortion, collision usability, rig deformation, target-engine performance, exporter-specific behavior or custom shader correctness. Curve/font/surface and other non-mesh geometry are explicitly flagged for manual review rather than silently certified. Image dimensions are uncompressed dimensions, not measured runtime memory. Assigned materials include unused slots conservatively and are not draw calls. The input hash covers the primary file, not external `.gltf` buffers, linked libraries or textures; preserve/hash those dependencies separately when establishing a reproducible revision.

Check the JSON `technical_limits_passed`, findings and scope even when the process exits normally. Limit violations are recorded with a nonzero process exit status. Parse/import failures return an error and no success report. Existing report paths are refused. If the source and export audit differ, investigate modifier evaluation, duplicate instances, hidden variants, triangulation and importer conversions; do not erase the discrepancy by increasing the budget.

## Final verification

For suspected excessive hidden geometry, gaps or floating components, use the separate background helper `scripts/audit_geometry.py` as described in [modeling discipline](modeling-discipline.md). Set the actual view range, saved state and explicit support/occluder context. It reports sampled candidates and incomplete work; it does not replace this asset audit, render inspection or application checks. Never delete geometry or certify support solely from its output.

For unwanted geometry intrusion, use the separate `scripts/audit_intersections.py` with explicit interacting objects/collections. Do not infer penetration-free assembly from the contact audit: it counts surface intersections as connectivity. Check containment as well as crossings, review ambiguous open shells and untested self-intersection, and inspect required poses/clearances. Export-only or isolated-asset evidence cannot establish compatibility with absent surroundings.

- Open/reimport the **actual final export** in a clean scene. Verify dimensions, orientation, visible parts, materials and dependencies against the final source. Audit evidence should identify input hashes/revisions.
- Render representative overview and semantic detail views of that export. A source render does not certify export appearance.
- Inspect required opening/rotation/deformation states; closed lids can hide defects. Check pivot and clearance, not only the existence of an object with the right name.
- Recheck affected object pairs in the actual exported assembly for forbidden penetration and functional clearance. Keep deliberate embedding scoped to its pair/region/depth/state; geometry-query completion or a sampled interior distance below an allowance is not a universal pass or a measurement of axial embed depth.
- Test the consuming application when included in the brief. Verify the final revision under its real camera, lighting, background and import settings. Distinguish visual inspection from a build/import check.
- Measure performance before claiming it. Fewer nodes, triangles or particles support a complexity claim, not a specific FPS claim.
- Require separate artistic-target evidence and export-fidelity evidence before claiming the asset finished. If the former fails, retain candidate/incomplete status even when the native file and GLB are valid.

For a standalone model, application verification may be `not-applicable`. If requested but unavailable, mark `not-verified` and name the missing evidence. A presentation turntable is optional and does not replace inspection of requested functional states.

Deliver paths to the editable source, required exports/textures and representative comparison images, plus a short status of artistic, source, export and application checks. Keep unresolved defects and inferred hidden parts visible. The user should only need to answer a new consequential design question or assess the delivered work, not rediscover obvious mismatches.
