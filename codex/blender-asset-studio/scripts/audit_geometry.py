#!/usr/bin/env python3
"""Read-only contact/visibility diagnostics in isolated background Blender.

These sampled geometry checks produce review candidates, never artistic acceptance
or permission to delete geometry. Coordinates and tolerances are in declared metres.
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def angles(text):
    try:
        values = [float(x) for x in text.split(',')]
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Use a comma-separated list of degrees') from exc
    if not values or len(values) > 360 or not all(math.isfinite(x) for x in values):
        raise argparse.ArgumentTypeError('Use 1–360 finite angles')
    return list(dict.fromkeys(values))


def parser_for_cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--collection')
    parser.add_argument('--check', choices=('contacts', 'visibility', 'both'), default='both')
    parser.add_argument('--tolerance-m', type=float, default=.003)
    parser.add_argument('--ground-z-m', type=float, default=None)
    parser.add_argument('--anchor', action='append', default=[], metavar='OBJECT')
    parser.add_argument('--occluder', action='append', default=[], metavar='OBJECT')
    parser.add_argument('--elevations', type=angles, default=angles('-75,-45,-20,0,20,45,75'))
    parser.add_argument('--azimuths', type=angles, default=angles('0,45,90,135,180,225,270,315'))
    parser.add_argument('--samples-per-face', type=int, choices=(1, 4, 7), default=7)
    parser.add_argument('--max-work', type=int, default=2000000,
                        help='Maximum counted operations per check; exhaustion means incomplete')
    parser.add_argument('--ray-epsilon-m', type=float, default=.000001)
    parser.add_argument('--backface-cull', action='store_true',
                        help='Only test outward-facing directions; default conservatively tests both sides')
    return parser


class Work:
    def __init__(self, maximum):
        self.maximum = maximum
        self.used = 0
        self.exhausted = False

    def take(self):
        if self.used >= self.maximum:
            self.exhausted = True
            return False
        self.used += 1
        return True

    def report(self):
        return {'used': self.used, 'cap': self.maximum, 'exhausted': self.exhausted}


def samples_for_triangle(points, count):
    a, b, c = points
    samples = [(a + b + c) / 3]
    if count >= 4:
        # Near corners rather than exact boundaries: reduce BVH shared-edge ambiguity.
        samples.extend([a * .98 + b * .01 + c * .01,
                        a * .01 + b * .98 + c * .01,
                        a * .01 + b * .01 + c * .98])
    if count >= 7:
        samples.extend([a * .495 + b * .495 + c * .01,
                        a * .495 + b * .01 + c * .495,
                        a * .01 + b * .495 + c * .495])
    return samples


def extract_geometry(bpy, Vector, BVHTree, allowed, anchors, occluders, scale):
    """Copy evaluated world-space meshes; no source mesh or transform is changed."""
    graph = bpy.context.evaluated_depsgraph_get()
    records, islands, triangles, excluded = [], [], [], set()
    extra_names = anchors | occluders
    matched_context = set()
    for serial, inst in enumerate(graph.object_instances):
        obj = inst.object
        original = obj.original
        parent = inst.parent.original if inst.parent else None
        related = {original.name} | ({parent.name} if parent else set())
        asset = original in allowed or parent in allowed
        context = related & extra_names
        if not asset and not context:
            continue
        if not inst.show_self or (not context and (original.hide_render or (parent and parent.hide_render))):
            continue
        if obj.type != 'MESH':
            if obj.type not in {'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE', 'SPEAKER', 'LIGHT_PROBE'}:
                excluded.add(original.name)
            continue
        mesh = obj.to_mesh(preserve_all_data_layers=True, depsgraph=graph)
        try:
            mesh.calc_loop_triangles()
            points = [(inst.matrix_world @ v.co) * scale for v in mesh.vertices]
            if not points or not mesh.polygons:
                continue
            if not all(math.isfinite(x) for p in points for x in p):
                raise ValueError('Non-finite evaluated vertex: ' + original.name)
            # Face islands connect across shared edges; merely sharing a vertex does not attach faces.
            parents = list(range(len(mesh.polygons)))
            def find(index):
                while parents[index] != index:
                    parents[index] = parents[parents[index]]
                    index = parents[index]
                return index
            edge_face = {}
            for face in mesh.polygons:
                ids = list(face.vertices)
                for u, v in zip(ids, ids[1:] + ids[:1]):
                    edge = tuple(sorted((u, v)))
                    if edge in edge_face:
                        parents[find(face.index)] = find(edge_face[edge])
                    else:
                        edge_face[edge] = face.index
            groups = {}
            degenerate = 0
            for tri in mesh.loop_triangles:
                ids = tuple(tri.vertices)
                a, b, c = [points[i] for i in ids]
                if (b - a).cross(c - a).length_squared <= 1e-24:
                    degenerate += 1
                    continue
                groups.setdefault(find(tri.polygon_index), []).append(ids)
            label = f'{original.name}@{serial}'
            island_ids = []
            for group_index, face_ids in enumerate(groups.values()):
                indices = sorted({v for face in face_ids for v in face})
                remap = {old: new for new, old in enumerate(indices)}
                coords = [points[v] for v in indices]
                polys = [tuple(remap[v] for v in face) for face in face_ids]
                index = len(islands)
                island_ids.append(index)
                island = {'id': index, 'label': f'{label}/island{group_index}',
                          'object': original.name, 'parent': parent.name if parent else None,
                          'asset': asset, 'anchor': bool(related & anchors),
                          'occluder': bool(context) or asset, 'points': coords,
                          'triangles': polys, 'bvh': BVHTree.FromPolygons(coords, polys, all_triangles=True),
                          'lo': Vector(tuple(min(p[k] for p in coords) for k in range(3))),
                          'hi': Vector(tuple(max(p[k] for p in coords) for k in range(3)))}
                islands.append(island)
                for local, face in enumerate(polys):
                    triangles.append({'island': index, 'local': local, 'points': [coords[i] for i in face],
                                      'asset': asset})
            if groups:
                matched_context.update(context)
            records.append({'id': label, 'object': original.name, 'parent': parent.name if parent else None,
                            'instance': bool(inst.is_instance), 'asset': asset,
                            'anchor': bool(related & anchors), 'occluder': bool(context),
                            'vertices': len(points), 'triangles': sum(map(len, groups.values())),
                            'degenerate_triangles_ignored': degenerate, 'islands': island_ids,
                            'modifier_visibility_mismatch': [m.name for m in original.modifiers
                                                            if m.show_viewport != m.show_render]})
        finally:
            obj.to_mesh_clear()
    missing = extra_names - matched_context
    if missing:
        raise ValueError('Named context has no evaluated visible mesh in this view layer: ' + ', '.join(sorted(missing)))
    return graph, records, islands, triangles, sorted(excluded)


def contact_check(islands, args):
    budget = Work(args.max_work)
    parent = list(range(len(islands)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    links = []
    tol = args.tolerance_m
    complete = True
    # Sampling is symmetric, includes all vertices plus interior/edge probes. BVH triangle
    # overlap catches crossings where none of the sampled points is near the other surface.
    for i, a in enumerate(islands):
        if not (a['asset'] or a['anchor']):
            continue
        if not complete:
            break
        for j in range(i + 1, len(islands)):
            b = islands[j]
            if not (b['asset'] or b['anchor']):
                continue
            if not budget.take():
                complete = False
                break
            if any(a['lo'][k] > b['hi'][k] + tol or b['lo'][k] > a['hi'][k] + tol for k in range(3)):
                continue
            if find(i) == find(j):
                continue
            if not budget.take():
                complete = False
                break
            reason = 'surface_intersection' if a['bvh'].overlap(b['bvh']) else None
            if reason is None:
                for src, dst in ((a, b), (b, a)):
                    face_probes = (p for face in src['triangles']
                                   for p in samples_for_triangle([src['points'][v] for v in face], 7))
                    for p in itertools.chain(src['points'], face_probes):
                        if not budget.take():
                            complete = False
                            break
                        if dst['bvh'].find_nearest(p, tol)[0] is not None:
                            reason = 'sampled_surface_distance'
                            break
                    if reason or not complete:
                        break
            if reason:
                parent[find(i)] = find(j)
                links.append({'a': i, 'b': j, 'basis': reason})
            if not complete:
                break
    ground = args.ground_z_m
    roots = {find(i) for i, part in enumerate(islands) if part['anchor']}
    grounded, buried = [], []
    if ground is not None:
        for i, part in enumerate(islands):
            if not (part['asset'] or part['anchor']):
                continue
            # A fully buried object is not automatically a supporting contact.
            if part['hi'].z < ground - tol:
                buried.append(i)
            elif part['lo'].z <= ground + tol and part['hi'].z >= ground - tol:
                grounded.append(i)
                roots.add(find(i))
    supports_declared = ground is not None or bool(args.anchor)
    groups = {}
    for i, part in enumerate(islands):
        groups.setdefault(find(i), []).append(i)
    unresolved = []
    for key, ids in groups.items():
        asset_ids = [i for i in ids if islands[i]['asset']]
        if asset_ids and key not in roots:
            unresolved.append({'islands': asset_ids,
                               'classification': ('unsupported_candidate' if complete else 'support_unresolved_incomplete')
                               if supports_declared else 'unanchored_no_support_declared'})
    return {'status': 'complete' if complete else 'incomplete',
            'support_specified': supports_declared, 'contact_links': links,
            'ground_contact_islands': grounded, 'fully_below_ground_islands': buried,
            'supported_asset_islands': [i for i, p in enumerate(islands) if p['asset'] and find(i) in roots],
            'unresolved_components': unresolved, 'work': budget.report(),
            'method': 'Shared-edge face islands; AABB rejection only; triangle-surface intersection or symmetric vertex/7-point triangle probes within tolerance; support propagates through contact chains.',
            'limitations': ['Sampled near-contact distances can miss narrow edge-edge proximity; BVH intersection is surface-based and does not detect solid containment without a surface contact.',
                            'Contacts imply proximity, not load-bearing strength, correct assembly, collision or physics.',
                            'No declared support means unanchored components, not a finding of floating geometry.',
                            'If incomplete, disconnected components are unresolved, not established unsupported.']}


def visibility_check(islands, triangles, args, Vector, BVHTree):
    budget = Work(args.max_work)
    verts, faces = [], []
    for part in islands:
        start = len(verts)
        verts.extend(part['points'])
        faces.extend([tuple(start + i for i in face) for face in part['triangles']])
    bvh = BVHTree.FromPolygons(verts, faces, all_triangles=True)
    radius = max((max(p[k] for p in verts) - min(p[k] for p in verts)) for k in range(3))
    distance = max(radius * 4, 1.0)
    directions = [Vector((math.cos(math.radians(e)) * math.cos(math.radians(a)),
                          math.cos(math.radians(e)) * math.sin(math.radians(a)),
                          math.sin(math.radians(e)))) for e in args.elevations for a in args.azimuths]
    visible, unseen, unknown = [], [], []
    asset_tris = [tri for tri in triangles if tri['asset']]
    eps = args.ray_epsilon_m
    for index, tri in enumerate(asset_tris):
        a, b, c = tri['points']
        normal = (b - a).cross(c - a).normalized()
        seen, tested_all = False, True
        for point in samples_for_triangle(tri['points'], args.samples_per_face):
            for direction in directions:
                facing = normal.dot(direction)
                if abs(facing) <= 1e-7 or (args.backface_cull and facing <= 0):
                    # A mathematically edge-on face has zero projected area.
                    continue
                if not budget.take():
                    tested_all = False
                    break
                ground = args.ground_z_m
                if ground is not None:
                    # Ground is an opaque half-space; buried samples cannot be viewed from underground.
                    if point.z < ground - eps:
                        continue
                    if direction.z < -1e-12 and (point.z <= ground + eps or (ground - point.z) / direction.z > eps):
                        continue
                origin = point + direction * eps
                if bvh.ray_cast(origin, direction, distance)[0] is None:
                    seen = True
                    break
            if seen or not tested_all:
                break
        if seen:
            visible.append(index)
        elif tested_all:
            unseen.append(index)
        else:
            unknown.extend(range(index, len(asset_tris)))
            break
    grouped = {}
    for index in unseen:
        tri = asset_tris[index]
        entry = grouped.setdefault(tri['island'], {'island': tri['island'], 'count': 0, 'triangle_indices': []})
        entry['count'] += 1
        if len(entry['triangle_indices']) < 100:
            entry['triangle_indices'].append(tri['local'])
    for entry in grouped.values():
        entry['indices_truncated'] = entry['count'] > len(entry['triangle_indices'])
    return {'status': 'incomplete' if unknown else 'complete',
            'counts': {'asset_triangles': len(asset_tris), 'sampled_visible': len(visible),
                       'candidate_unseen': len(unseen), 'unclassified': len(unknown)},
            'candidate_unseen_by_island': list(grouped.values()), 'work': budget.report(),
            'settings': {'elevations_deg': args.elevations, 'azimuths_deg': args.azimuths,
                         'samples_per_triangle': args.samples_per_face,
                         'backface_cull': args.backface_cull, 'edge_on_dot_threshold': 1e-7, 'ray_epsilon_m': eps, 'ray_distance_m': distance},
            'method': 'Triangle centroid plus near-corner/edge samples; rays toward explicit parallel view directions, evaluated asset and named occluders; optional opaque ground half-space.',
            'limitations': ['Candidate-unseen means unseen by these samples/directions only, never proof of invisibility.',
                            'Finite samples can miss a small visible patch; restricted directions do not establish visibility outside the supplied camera range.',
                            'Opaque geometric ray casts ignore transparency, alpha cutouts, reflection, shadows, animation and alternate states.',
                            'Default rays consider both sides of surfaces; exactly edge-on directions are skipped (absolute normal/direction dot <= 1e-7); optional backface culling assumes correct winding.',
                            'A work cap leaves untested triangles unclassified; they are never added to candidate-unseen.',
                            'Do not delete any candidate automatically; check silhouettes, gaps, shadows, reflections, collision and movable/destructible states.']}


def main():
    try:
        import bpy
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
    except ImportError as exc:
        raise RuntimeError('Run with isolated background Blender, not ordinary Python') from exc
    if not bpy.app.background:
        raise RuntimeError('Refusing live Blender; run a separate --background process')
    cli = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    parser = parser_for_cli()
    args = parser.parse_args(cli)
    source = args.input.resolve(strict=True)
    if source.suffix.lower() not in {'.blend', '.glb', '.gltf'}:
        raise ValueError('Supported inputs: .blend, .glb, .gltf')
    if args.output.exists() or args.output.resolve() == source:
        raise ValueError('Output must be a new report path, never the input')
    if not math.isfinite(args.tolerance_m) or args.tolerance_m < 0:
        raise ValueError('--tolerance-m must be finite and nonnegative')
    if args.ground_z_m is not None and not math.isfinite(args.ground_z_m):
        raise ValueError('--ground-z-m must be finite')
    if args.max_work < 1 or not math.isfinite(args.ray_epsilon_m) or args.ray_epsilon_m <= 0:
        raise ValueError('--max-work and --ray-epsilon-m must be positive')
    if any(abs(e) > 90 for e in args.elevations):
        raise ValueError('Elevations must be between -90 and 90 degrees')
    before = digest(source)
    if source.suffix.lower() == '.blend':
        bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(source))
    if args.collection:
        collection = bpy.data.collections.get(args.collection)
        if collection is None:
            raise ValueError('Collection not found: ' + args.collection)
        allowed = set(collection.all_objects)
    else:
        allowed = set(bpy.context.scene.objects)
    for name in args.anchor + args.occluder:
        if bpy.data.objects.get(name) is None:
            raise ValueError('Named context object not found: ' + name)
    scale = bpy.context.scene.unit_settings.scale_length
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError('Scene unit scale must be finite and positive')
    graph, records, islands, triangles, excluded = extract_geometry(
        bpy, Vector, BVHTree, allowed, set(args.anchor), set(args.occluder), scale)
    findings = []
    has_asset = any(part['asset'] for part in islands)
    if not has_asset:
        findings.append({'level': 'error', 'code': 'no_mesh_geometry_in_scope'})
    if excluded:
        findings.append({'level': 'warning', 'code': 'unsupported_non_mesh_geometry', 'objects': excluded})
    if any(r['modifier_visibility_mismatch'] for r in records):
        findings.append({'level': 'warning', 'code': 'viewport_render_modifier_difference'})
    checks = {}
    if has_asset:
        if args.check in {'contacts', 'both'}:
            checks['contacts'] = contact_check(islands, args)
        if args.check in {'visibility', 'both'}:
            checks['visibility'] = visibility_check(islands, triangles, args, Vector, BVHTree)
    after = digest(source)
    if before != after:
        raise RuntimeError('Input changed during audit; refusing a stable-revision report')
    report = {'schema_version': 1, 'input': str(source), 'input_sha256': before,
              'input_sha256_after': after, 'blender_version': bpy.app.version_string,
              'status': 'complete' if has_asset and all(c['status'] == 'complete' for c in checks.values()) else 'incomplete',
              'artistic_acceptance': 'not-assessed',
              'scope': {'collection': args.collection, 'view_layer': bpy.context.view_layer.name,
                        'frame': bpy.context.scene.frame_current, 'evaluation_mode': graph.mode,
                        'anchors': args.anchor, 'occluders': args.occluder,
                        'basis': 'Evaluated active-view-layer mesh instances; collection asset scope plus explicitly named context only'},
              'settings': {'check': args.check, 'tolerance_m': args.tolerance_m,
                           'ground_z_m': args.ground_z_m, 'max_work_per_check': args.max_work,
                           'unit_system': bpy.context.scene.unit_settings.system,
                           'metres_per_blender_unit': scale},
              'counts': {'evaluated_mesh_instances': len(records),
                         'asset_mesh_instances': sum(r['asset'] for r in records),
                         'asset_triangles': sum(len(p['triangles']) for p in islands if p['asset']),
                         'asset_islands': sum(p['asset'] for p in islands),
                         'context_islands': sum(not p['asset'] for p in islands)},
              'objects': records,
              'islands': [{k: p[k] for k in ('id', 'label', 'object', 'parent', 'asset', 'anchor', 'occluder')}
                          | {'triangles': len(p['triangles']), 'bounds_m': [list(p['lo']), list(p['hi'])]} for p in islands],
              'checks': checks, 'findings': findings,
              'limitations': ['Primary input hash does not cover linked blend data or external glTF buffers/images.',
                              'Current scene/frame/view layer only; viewport evaluation is not a complete render/export prediction.',
                              'World transforms, instances and declared unit scale are applied. Collection exclusions may omit geometry; inspect scope and counts.',
                              'Heuristic diagnostic only: no automatic deletion, optimization, load-bearing verdict or artistic pass.',
                              'Work budget counts pair tests, BVH intersection queries, nearest-point queries or rays; it is not a wall-clock/memory bound.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    print(json.dumps({'report': str(args.output.resolve()), 'status': report['status'], 'counts': report['counts']}))
    return 0 if report['status'] == 'complete' else 2


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'Geometry audit failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        sys.exit(1)
