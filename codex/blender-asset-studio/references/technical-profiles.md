# Technical constraints and fallback profiles

## Constraint hierarchy

1. Current explicit user requirements.
2. Applicable project/asset contracts and compatibility rules.
3. Target importer/platform constraints.
4. Clearly disclosed provisional defaults.

Keep the source and scope of every limit. Never claim a fallback number is an industry standard or transplant a game's art style/budgets into another project.

There is no single useful triangle ceiling for every 3D deliverable. Screen coverage, camera distance, silhouette, instances, shading, transparency and deformation all matter. Existing budgets are acceptance gates; negotiate a real conflict rather than silently exceeding or weakening them.

Separate user/project hard limits from an agent's planning estimate. Do not invent an unnecessarily low cap and then use it to excuse a weak visible result. An agent-selected estimate may be adjusted autonomously within actual project limits when justified by the target. Neither raising the count nor hitting a low count proves quality. A hard budget conflict needs a different representation or a user decision, not a silent downgrade of the visual target.

## Universal checks, conditional requirements

- Preserve documented units, axes, origin, hierarchy and animation interfaces. In a new unspecified asset, use meters, Blender +Z up, identity root transform and an appropriate support/attachment origin; record the chosen forward axis.
- Count evaluated/exported triangles, not source polygons. Distinguish an active variant from all alternatives, unique geometry from placed instances, and mesh materials from draw-call predictions.
- Use clean normals and intentional smoothing; avoid accidental duplicate surfaces, z-fighting and hidden dense geometry.
- Check forbidden solid penetration and working clearances between assembled parts and interacting assets, separately from support/contact. Keep intentional embedding explicit and bounded; include relevant poses and actual export context.
- UVs need appropriate scale, padding and distortion control. Mirroring/overlap is allowed when intentional and compatible with baking; not every asset needs unique UVs.
- Interpret BaseColor/emissive color and linear data maps correctly. Declare normal-map convention and packed channels. Uniform maps can often be scalar values.
- Reuse compatible material resources and consolidate static geometry where useful without destroying separate required parts.
- Keep textures and native procedural sources recoverable. Verify the actual exported material; a Blender graph is not an export guarantee.
- For deformation, prioritize topology and weights at joints; preserve the existing rig/bind pose. Test required poses after reduction and export.
- For print/manufacture, confirm units, wall thickness, watertightness and fabrication requirements. Visual acceptance alone is insufficient; do not apply game budgets.

## Provisional real-time starting caps

Use only when real-time delivery is requested and no applicable limits exist. These are initial agent planning assumptions for one active LOD0 asset, not established universal standards. Revisit them based on actual target views and platform. Desktop hero values are unsuitable as mobile defaults.

| Profile | LOD0 starting cap | Material slots starting cap | Typical starting maps |
|---|---:|---:|---|
| Small/background prop | 2,000 triangles | 1 | 256–512 px |
| Ordinary desktop prop | 10,000 triangles | 2 | 512–1024 px |
| Close-view desktop hero prop | 60,000 triangles | 4 | 1024–2048 px |
| Character, vehicle, modular building | Derive per asset and target; do not force the prop table | Explicit per-part/material plan | Shared tiling sets, trim/atlas or authored maps as appropriate |

Set a concrete cap for the actual task before detailed production. For an unspecified standalone visualization, avoid an arbitrary game cap: prioritize editable topology, useful render cost and detail justified by the requested resolution.

## Texture size from use

Estimate the largest projected footprint. In orthographic views, projected pixels per meter are approximately image height / vertical world span. In perspective views, use the actual camera or a projection measurement; a rough near-center estimate is H / (2 d tan(FOV_y/2)), with consistent units.

Choose a practical texel density from that footprint and UV usage, accounting for close views and minification. A standalone prop may start around 512 texels/m; distant props may need less and close hero views more. This is a provisional assumption, not a quality guarantee.

Texture dimensions follow real surface area/UV span, not just the object's bounding box. A large surface can use tiling materials, trim sheets and localized decals instead of a huge unique atlas. Account for UV padding and intended mips. Verify at the closest use distance and target resolution.

For real-time assets, use target-supported compression and mipmaps unless a specific data texture forbids them. Alpha overdraw, material count and shadow work can outweigh polygon reductions. Consult the current target documentation for format-specific settings.

## Production decisions

Use [modeling discipline](modeling-discipline.md) for screen-size thresholds, curvature/repetition choices, hidden-surface examples, post-modifier contact checks and the optional geometry diagnostics. Its example pixel, segment, embed and contact values are heuristics; retain this document's constraint hierarchy.

Use geometry for visible silhouette, openings, thickness, major dents and deformation. Use maps for surface detail when the target view does not justify geometry. A high-detail source plus a lower-cost baked export is useful only if it improves the requested result.

Plan by visibility: focal/near, routinely visible, occasionally visible, and hidden. Simplify hidden geometry without damaging silhouette, shadows, reflections, visible openings or required function. Do not spend the saved budget on more invisible detail. Preserve visible material richness through suitable source textures, local masks, roughness/normal detail and baking when appropriate. Camera distance is a resource-allocation input, not permission to accept a placeholder.

Avoid indiscriminate decimation of rigs, thin shells, openings or hard-surface edges. After reduction, compare paired images and test protected interfaces. Low-poly visual style and low render cost are different claims.

Game collision, LODs and effects are conditional on task scope. A light socket is not a light; an emission texture is not proof of scene illumination. Do not add controllers or a test game to standalone model work.

## Source guidance

[Godot's 3D optimization guidance](https://docs.godotengine.org/en/stable/tutorials/performance/optimizing_3d_performance.html) discusses visibility, transparent surfaces and LOD. It does not establish the provisional caps above. For another engine or an updated importer, consult that target's current official documentation and installed behavior.
