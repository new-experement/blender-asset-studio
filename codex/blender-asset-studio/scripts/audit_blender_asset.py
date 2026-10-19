#!/usr/bin/env python3
"""Read-only asset audit in isolated background Blender; no artistic verdict."""
import argparse
import hashlib
import json
import sys
from pathlib import Path


def digest(path):
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(block)
    return checksum.hexdigest()


def main():
    try:
        import bpy
        from mathutils import Vector
    except ImportError:
        raise RuntimeError("Run this script with background Blender, not ordinary Python")
    if not bpy.app.background:
        raise RuntimeError("Refusing to run in live Blender; use a separate --background process")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--collection")
    parser.add_argument("--max-triangles", type=int)
    parser.add_argument("--max-materials", type=int)
    parser.add_argument("--max-texture-edge", type=int)
    parser.add_argument("--require-uv", action="store_true")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
    source = args.input.resolve(strict=True)
    if source.suffix.lower() not in {".blend", ".glb", ".gltf"}:
        raise ValueError("Supported inputs: .blend, .glb, .gltf")
    if args.output.exists() or args.output.resolve() == source:
        raise ValueError("Output must be a new report path, never the input")
    for flag in ("max_triangles", "max_materials", "max_texture_edge"):
        if getattr(args, flag) is not None and getattr(args, flag) < 1:
            raise ValueError(f"{flag} must be a positive integer")
    before_hash = digest(source)
    if source.suffix.lower() == ".blend":
        bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(source))
    if args.collection:
        collection = bpy.data.collections.get(args.collection)
        if collection is None:
            raise ValueError(f"Collection not found: {args.collection}")
        allowed = set(collection.all_objects)
    else:
        allowed = set(bpy.context.scene.objects)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    findings = []
    def finding(level, code, detail):
        findings.append({"level": level, "code": code, "detail": detail})
    records, materials = [], {}
    bounds_min = Vector((float("inf"),) * 3)
    bounds_max = Vector((float("-inf"),) * 3)
    total_triangles = 0
    modifier_mismatches = set()
    unsupported = set()
    for instance in depsgraph.object_instances:
        obj = instance.object
        original = obj.original
        parent = instance.parent.original if instance.parent else None
        if original not in allowed and parent not in allowed:
            continue
        if original.hide_render or (parent and parent.hide_render) or not instance.show_self:
            continue
        if obj.type != "MESH":
            if obj.type in {"CURVE", "SURFACE", "FONT", "META", "VOLUME", "POINTCLOUD", "GREASEPENCIL"}:
                unsupported.add(original.name)
            continue
        for modifier in original.modifiers:
            if modifier.show_viewport != modifier.show_render:
                modifier_mismatches.add(f"{original.name}/{modifier.name}")
        mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
        try:
            mesh.calc_loop_triangles()
            triangles = len(mesh.loop_triangles)
            total_triangles += triangles
            if args.require_uv and triangles and not mesh.uv_layers:
                finding("error", "missing_uv", original.name)
            negative = instance.matrix_world.to_3x3().determinant() < 0
            if negative:
                finding("warning", "negative_transform", original.name)
            for vertex in mesh.vertices:
                point = instance.matrix_world @ vertex.co
                for axis in range(3):
                    bounds_min[axis] = min(bounds_min[axis], point[axis])
                    bounds_max[axis] = max(bounds_max[axis], point[axis])
            # Include all assigned slots conservatively; do not equate with draw calls.
            assigned = list(mesh.materials)
            assigned.extend(slot.material for slot in obj.material_slots)
            names = sorted({mat.name for mat in assigned if mat})
            materials.update({mat.name: mat for mat in assigned if mat})
            records.append({"object": original.name, "instance": bool(instance.is_instance),
                            "parent": parent.name if parent else None,
                            "triangles": triangles, "vertices": len(mesh.vertices),
                            "uv_layers": [layer.name for layer in mesh.uv_layers],
                            "materials": names, "negative_transform": negative})
        finally:
            obj.to_mesh_clear()
    if not records:
        finding("error", "no_meshes_in_scope", "No evaluated mesh instances were counted")
    if unsupported:
        finding("warning", "non_mesh_geometry_not_counted", sorted(unsupported))
    if modifier_mismatches:
        finding("warning", "viewport_render_modifier_difference", sorted(modifier_mismatches))

    images, visited = {}, set()
    def inspect_nodes(tree):
        if tree is None or tree.as_pointer() in visited:
            return
        visited.add(tree.as_pointer())
        for node in tree.nodes:
            im = getattr(node, "image", None)
            if im is not None:
                images[im.name] = im
            inspect_nodes(getattr(node, "node_tree", None))
    for mat in materials.values():
        inspect_nodes(mat.node_tree)
    textures = []
    for name, im in sorted(images.items()):
        size = list(im.size)
        packed = bool(im.packed_file or len(im.packed_files))
        file_path = Path(bpy.path.abspath(im.filepath, library=im.library)) if im.filepath else None
        missing = im.source == "FILE" and not packed and (file_path is None or not file_path.is_file())
        if missing:
            finding("error", "missing_texture", name)
        if min(size) == 0:
            finding("error", "texture_has_no_pixels", name)
        if args.max_texture_edge and max(size) > args.max_texture_edge:
            finding("error", "texture_edge_limit", {"image": name, "actual": size, "limit": args.max_texture_edge})
        if im.source in {"TILED", "SEQUENCE", "MOVIE"}:
            finding("warning", "texture_sequence_or_tiles_need_review", name)
        textures.append({"image": name, "size": size, "channels": im.channels,
                         "source": im.source, "color_space": im.colorspace_settings.name,
                         "packed": packed, "path": str(file_path) if file_path else None,
                         "missing": missing})
    if args.max_triangles and total_triangles > args.max_triangles:
        finding("error", "triangle_limit", {"actual": total_triangles, "limit": args.max_triangles})
    if args.max_materials and len(materials) > args.max_materials:
        finding("error", "material_limit", {"actual": len(materials), "limit": args.max_materials})
    after_hash = digest(source)
    if before_hash != after_hash:
        raise RuntimeError("Input changed during audit; no stable-revision report can be issued")
    has_bounds = all(v != float("inf") for v in bounds_min)
    dimensions = list(bounds_max - bounds_min) if has_bounds else None
    unit_scale = bpy.context.scene.unit_settings.scale_length
    report = {
        "schema_version": 1, "input": str(source), "input_sha256": before_hash,
        "blender_version": bpy.app.version_string,
        "scope": {"collection": args.collection, "view_layer": bpy.context.view_layer.name,
                  "frame": bpy.context.scene.frame_current, "evaluation_mode": depsgraph.mode,
                  "basis": "Evaluated active-view-layer mesh instances filtered by object hide_render and show_self; viewport evaluation is not a full render/export prediction"},
        "units": {"system": bpy.context.scene.unit_settings.system, "scale_length": unit_scale,
                  "dimensions_blender_units": dimensions,
                  "dimensions_meters_at_declared_scale": [v * unit_scale for v in dimensions] if dimensions else None},
        "counts": {"triangles_with_instances": total_triangles, "mesh_instances": len(records),
                   "distinct_object_names": len({r["object"] for r in records}),
                   "assigned_materials": len(materials), "image_textures": len(textures)},
        "objects": records, "textures": textures, "findings": findings,
        "limits": {key: getattr(args, key) for key in ("max_triangles", "max_materials", "max_texture_edge", "require_uv")},
        "technical_limits_passed": not any(f["level"] == "error" for f in findings),
        "artistic_acceptance": "not-assessed",
        "limitations": ["Active view layer/current frame only; inspect hidden variants and other frames separately",
                        "Viewport-excluded geometry and collection render restrictions require scope review",
                        "No UV distortion, normal-map, rig, collision, shader appearance or performance verdict",
                        "Linked input dependencies are not covered by the primary-file hash"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({"report": str(args.output.resolve()), "counts": report["counts"],
                      "technical_limits_passed": report["technical_limits_passed"]}))
    return 0 if report["technical_limits_passed"] else 2


if __name__ == "__main__":
    try:
        status = main()
    except Exception as exc:
        print(f"Asset audit failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
    sys.exit(status)
