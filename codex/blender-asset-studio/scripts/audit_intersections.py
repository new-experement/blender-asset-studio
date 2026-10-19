#!/usr/bin/env python3
"""Read-only sampled interpenetration diagnostic in isolated background Blender.

Contact/support is not proof of non-penetration. This reports geometric evidence
and uncertainty, never an artistic pass, certified clearance or automatic fix.
"""
import argparse
import itertools
import json
import math
import sys
from pathlib import Path

# Reuse only read-only evaluated-instance extraction and generic helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_geometry import Work, digest, extract_geometry, samples_for_triangle


class IncompleteQuery(RuntimeError):
    pass


def spend(work):
    if not work.take():
        raise IncompleteQuery('work_cap')


def load_allowances(path):
    if path is None:
        return {}, None
    source = path.resolve(strict=True)
    data = json.loads(source.read_text())
    if not isinstance(data, dict) or set(data) != {'pairs'} or not isinstance(data['pairs'], list):
        raise ValueError('Allowances must be {"pairs":[{"objects":["A","B"],"max_interior_distance_m":0.02,"reason":"..."}]}')
    records = {}
    for record in data['pairs']:
        if not isinstance(record, dict) or set(record) != {'objects', 'max_interior_distance_m', 'reason'}:
            raise ValueError('Each allowance needs exactly objects, max_interior_distance_m and reason')
        names, limit, reason = record['objects'], record['max_interior_distance_m'], record['reason']
        if (not isinstance(names, list) or len(names) != 2 or
                not all(isinstance(x, str) and x and '*' not in x for x in names) or names[0] == names[1]):
            raise ValueError('Allowance needs two different exact object names, no wildcard')
        if isinstance(limit, bool) or not isinstance(limit, (int, float)) or not math.isfinite(limit) or limit < 0:
            raise ValueError('Allowance max_interior_distance_m must be finite and nonnegative')
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('Allowance reason must be nonempty')
        key = tuple(sorted(names))
        if key in records:
            raise ValueError('Duplicate allowance pair: ' + str(key))
        records[key] = record
    return records, {'path': str(source), 'sha256': digest(source), 'pairs': list(records.values())}


def topology(part):
    edges = {}
    volume6 = 0.0
    origin = part['points'][0]
    for face in part['triangles']:
        for u, v in zip(face, face[1:] + face[:1]):
            edges.setdefault(tuple(sorted((u, v))), []).append((u, v))
        a, b, c = (part['points'][i] - origin for i in face)
        volume6 += a.dot(b.cross(c))
    boundary = sum(len(v) == 1 for v in edges.values())
    nonmanifold = sum(len(v) != 2 for v in edges.values())
    inconsistent = sum(len(v) == 2 and v[0] == v[1] for v in edges.values())
    diagonal = (part['hi'] - part['lo']).length
    nonzero_volume = abs(volume6) > max(diagonal ** 3 * 1e-12, 1e-24)
    solid_candidate = not nonmanifold and not inconsistent and nonzero_volume
    return {'closed_oriented_solid_candidate': solid_candidate, 'boundary_edges': boundary,
            'nonmanifold_edges': nonmanifold, 'inconsistent_winding_edges': inconsistent,
            'signed_volume_m3': volume6 / 6,
            'orientation': 'outward_by_signed_volume' if volume6 > 0 else 'inward_or_zero_by_signed_volume',
            'self_intersection': 'untested', 'edges': sorted(edges)}


def nearest(part, point, work):
    spend(work)
    return part['query_bvh'].find_nearest(point - part['query_origin'])


def ray_hits(part, point, direction, distance, args, work):
    """Bound every BVH query and every ray's hit count; do not materialize BVH overlap lists."""
    base = point - part['query_origin']
    hits, travelled, origin = [], 0.0, base.copy()
    for unused in range(args.max_hits_per_ray):
        spend(work)
        location, normal, face, travel = part['query_bvh'].ray_cast(origin, direction, distance - travelled)
        if location is None:
            return hits
        total = travelled + travel
        if not hits or total - hits[-1] > args.ray_epsilon_m * .5:
            hits.append(total)
        advance = max(travel, 0) + args.ray_epsilon_m
        travelled += advance
        if travelled >= distance:
            return hits
        origin = base + direction * travelled
    raise IncompleteQuery('per_ray_hit_cap')


def interior_distance(part, point, topo, args, work, directions):
    """Return positive distance only when 3 parity rays agree inside a closed candidate."""
    spend(work)
    if any(point[k] < part['lo'][k] - args.tolerance_m - args.ray_epsilon_m or
           point[k] > part['hi'][k] + args.tolerance_m + args.ray_epsilon_m for k in range(3)):
        return 'outside', None
    hit, normal, face, distance = nearest(part, point, work)
    if hit is None:
        return 'uncertain', None
    if distance <= args.ray_epsilon_m * 2:
        return 'boundary', distance
    if any(point[k] < part['lo'][k] - args.ray_epsilon_m or
           point[k] > part['hi'][k] + args.ray_epsilon_m for k in range(3)):
        return 'outside', distance
    if not topo['closed_oriented_solid_candidate']:
        return 'uncertain', distance
    ray_length = max((part['hi'] - part['lo']).length * 3, args.ray_epsilon_m * 100)
    votes = [len(ray_hits(part, point, direction, ray_length, args, work)) % 2 for direction in directions]
    if len(set(votes)) != 1:
        return 'uncertain', distance
    return ('inside', distance) if votes[0] else ('outside', distance)


def pair_check(a, b, ta, tb, allowance, args, work, directions):
    spend(work)
    record = {'a': a['id'], 'b': b['id'], 'objects': [a['object'], b['object']],
              'status': None, 'max_sampled_interior_distance_m': 0.0,
              'edge_surface_hits': 0, 'tested_surface_samples': 0,
              'uncertain_point_classifications': 0, 'near_surface_sample_distance_m': None,
              'allowance': allowance, 'depth_is_certified_maximum': False,
              'evidence_points': [], 'max_depth_witness': None,
              'allowance_exceeded_by_sample': False, 'allowance_comparison_epsilon_m': args.ray_epsilon_m,
              'metric': 'Maximum observed distance from a verified interior sample to the nearest target surface; not axial embed extent or minimum translation to separate.'}
    if any(a['lo'][k] > b['hi'][k] + args.tolerance_m or
           b['lo'][k] > a['hi'][k] + args.tolerance_m for k in range(3)):
        record['status'] = 'aabb_separated'
        return record
    try:
        for source, target, target_topology, source_topology in ((a, b, tb, ta), (b, a, ta, tb)):
            def inspect(point, basis):
                state, distance = interior_distance(target, point, target_topology, args, work, directions)
                record['tested_surface_samples'] += 1
                if state == 'uncertain':
                    record['uncertain_point_classifications'] += 1
                if distance is not None:
                    old = record['near_surface_sample_distance_m']
                    record['near_surface_sample_distance_m'] = distance if old is None else min(old, distance)
                if state == 'inside' and distance > record['max_sampled_interior_distance_m']:
                    record['max_sampled_interior_distance_m'] = distance
                    if allowance and distance > allowance['max_interior_distance_m'] + args.ray_epsilon_m:
                        record['allowance_exceeded_by_sample'] = True
                    evidence = {'source_island': source['id'], 'target_island': target['id'],
                                'point_m': list(point), 'interior_distance_m': distance, 'basis': basis}
                    record['max_depth_witness'] = evidence
                    if len(record['evidence_points']) < 8:
                        record['evidence_points'].append(evidence)
            # Vertices and face samples discover ordinary intrusion and full containment.
            for point in itertools.chain(source['points'],
                    (p for face in source['triangles']
                     for p in samples_for_triangle([source['points'][v] for v in face], args.samples_per_face))):
                inspect(point, 'surface_sample')
            # Inward probes distinguish coincident closed solids from mere touching.
            # Verify the witness lies inside its own source solid before testing target.
            extents = [source['hi'][k] - source['lo'][k] for k in range(3)]
            step = min(extents) * .25
            if source_topology['closed_oriented_solid_candidate'] and step > args.ray_epsilon_m * 4:
                for face in source['triangles']:
                    p, q, r = [source['points'][v] for v in face]
                    normal = (q - p).cross(r - p).normalized()
                    inward = -normal if source_topology['signed_volume_m3'] > 0 else normal
                    witness = (p + q + r) / 3 + inward * step
                    own_state, own_distance = interior_distance(source, witness, source_topology, args, work, directions)
                    if own_state == 'inside':
                        inspect(witness, 'verified_source_interior_witness')
            # Split original/triangulation edges at intersections with the other solid.
            # Midpoints of intersected intervals catch large thin crossings even when all
            # original mesh vertices remain outside the other object.
            for u, v in source_topology['edges']:
                spend(work)
                start, end = source['points'][u], source['points'][v]
                delta = end - start
                length = delta.length
                if length <= args.ray_epsilon_m * 4:
                    continue
                direction = delta / length
                hits = ray_hits(target, start + direction * args.ray_epsilon_m, direction,
                                length - args.ray_epsilon_m * 2, args, work)
                if hits:
                    record['edge_surface_hits'] += len(hits)
                    cuts = [0.0] + [x + args.ray_epsilon_m for x in hits] + [length]
                    for left, right in zip(cuts, cuts[1:]):
                        if right - left > args.ray_epsilon_m * 4:
                            inspect(start + direction * ((left + right) / 2), 'edge_crossing_interval_midpoint')
    except IncompleteQuery as exc:
        record['status'] = 'incomplete'
        record['incomplete_reason'] = str(exc)
        return record
    depth = record['max_sampled_interior_distance_m']
    exceeded = allowance is not None and depth > allowance['max_interior_distance_m'] + args.ray_epsilon_m
    record['allowance_exceeded_by_sample'] = exceeded
    record['allowance_comparison_epsilon_m'] = args.ray_epsilon_m
    record['metric'] = 'Maximum observed distance from a verified interior sample to the nearest target surface; not axial embed extent or minimum translation to separate.'
    if not ta['closed_oriented_solid_candidate'] or not tb['closed_oriented_solid_candidate']:
        record['status'] = 'uncertain_solid_semantics'
    elif exceeded or (depth > args.tolerance_m and not allowance):
        record['status'] = 'penetration_candidate'
    elif record['uncertain_point_classifications']:
        record['status'] = 'uncertain_point_parity'
    elif depth > args.tolerance_m:
        record['status'] = ('within_allowance_at_samples' if allowance and
                            depth <= allowance['max_interior_distance_m'] + args.ray_epsilon_m else 'penetration_candidate')
    elif depth > 0 or (record['near_surface_sample_distance_m'] is not None and
                       record['near_surface_sample_distance_m'] <= args.tolerance_m):
        record['status'] = 'touching_or_shallow_within_tolerance_at_samples'
    elif record['edge_surface_hits']:
        record['status'] = 'surface_crossing_candidate_depth_unresolved'
    else:
        record['status'] = 'no_penetration_found_in_samples'
    return record


def main():
    try:
        import bpy
        from mathutils import Vector
        from mathutils.bvhtree import BVHTree
    except ImportError as exc:
        raise RuntimeError('Run with isolated background Blender, not ordinary Python') from exc
    if not bpy.app.background:
        raise RuntimeError('Refusing live Blender; use a separate --background process')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--collection')
    parser.add_argument('--against', action='append', default=[], metavar='OBJECT')
    parser.add_argument('--against-collection', action='append', default=[], metavar='COLLECTION')
    parser.add_argument('--allowances', type=Path)
    parser.add_argument('--tolerance-m', type=float, default=.003)
    parser.add_argument('--samples-per-face', type=int, choices=(1, 4, 7), default=7)
    parser.add_argument('--max-work', type=int, default=2000000)
    parser.add_argument('--max-hits-per-ray', type=int, default=128)
    parser.add_argument('--ray-epsilon-m', type=float, default=.000001)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    source = args.input.resolve(strict=True)
    if source.suffix.lower() not in {'.blend', '.glb', '.gltf'}:
        raise ValueError('Supported input: .blend, .glb, .gltf')
    if args.output.exists() or args.output.resolve() == source:
        raise ValueError('Output must be a new report path, never the input')
    if args.allowances and args.output.resolve() == args.allowances.resolve():
        raise ValueError('Output must not replace the allowance file')
    if not math.isfinite(args.tolerance_m) or args.tolerance_m < 0:
        raise ValueError('--tolerance-m must be finite and nonnegative')
    if args.max_work < 1 or args.max_hits_per_ray < 1 or args.max_hits_per_ray > 4096:
        raise ValueError('Work must be positive; per-ray hit cap must be 1–4096')
    if not math.isfinite(args.ray_epsilon_m) or args.ray_epsilon_m <= 0:
        raise ValueError('Ray epsilon must be finite and positive')
    allowances, allowance_meta = load_allowances(args.allowances)
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
    context_names = set(args.against)
    for name in args.against_collection:
        collection = bpy.data.collections.get(name)
        if collection is None:
            raise ValueError('Against collection not found: ' + name)
        unsupported = [obj.name for obj in collection.all_objects if obj.type in
                       {'CURVE', 'SURFACE', 'FONT', 'META', 'VOLUME', 'POINTCLOUD', 'GREASEPENCIL'}]
        if unsupported:
            raise ValueError('Unsupported explicit context geometry in collection ' + name + ': ' + ', '.join(sorted(unsupported)))
        names = {obj.name for obj in collection.all_objects if obj.type == 'MESH' or obj.instance_type == 'COLLECTION'}
        if not names:
            raise ValueError('Against collection contains no mesh/collection-instance objects: ' + name)
        context_names.update(names)
    for name in context_names:
        obj = bpy.data.objects.get(name)
        if obj is None:
            raise ValueError('Against object not found: ' + name)
        if obj.type != 'MESH' and obj.instance_type != 'COLLECTION':
            raise ValueError('Unsupported explicit context object: ' + name + ' (' + obj.type + ')')
    for pair in allowances:
        if any(bpy.data.objects.get(name) is None for name in pair):
            raise ValueError('Allowance names an absent object: ' + str(pair))
    scale = bpy.context.scene.unit_settings.scale_length
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError('Scene unit scale must be finite and positive')
    graph, objects, islands, triangles, excluded = extract_geometry(
        bpy, Vector, BVHTree, allowed, set(), context_names, scale)
    # Object names identify source data, not a unique placed instance. Resolve all
    # current-view-layer placements before applying any object-pair allowance.
    allowance_names = {name for key in allowances for name in key}
    placed = {name: [] for name in allowance_names}
    scope_ids = {obj['id'] for obj in objects}
    for serial, inst in enumerate(graph.object_instances):
        obj = inst.object
        if obj.type != 'MESH' or obj.original.name not in placed or not inst.show_self:
            continue
        parent = inst.parent.original if inst.parent else None
        context_requested = obj.original.name in context_names or (parent and parent.name in context_names)
        if (obj.original.hide_render or (parent and parent.hide_render)) and not context_requested:
            continue
        identity = f'{obj.original.name}@{serial}'
        placed[obj.original.name].append({'id': identity, 'object': obj.original.name,
                                          'parent': parent.name if parent else None,
                                          'instance': bool(inst.is_instance), 'in_report_scope': identity in scope_ids})
    allowance_resolutions = {}
    for key, definition in allowances.items():
        counts = [len(placed[name]) for name in key]
        state = ('ambiguous_multiple_evaluated_instances' if any(count > 1 for count in counts)
                 else 'not_evaluated' if any(count == 0 for count in counts) else 'unique_evaluated_pair')
        allowance_resolutions[key] = {'status': state, 'definition': definition,
                                     'instance_candidates': {name: placed[name] for name in key}}
    if allowance_meta is not None:
        allowance_meta['resolutions'] = list(allowance_resolutions.values())
    # BVH queries use translated local coordinates to avoid repeated ray-origin
    # rounding at distant world positions; report/evidence remain world metres.
    for part in islands:
        part['query_origin'] = (part['lo'] + part['hi']) / 2
        local = [point - part['query_origin'] for point in part['points']]
        part['query_bvh'] = BVHTree.FromPolygons(local, part['triangles'], all_triangles=True)
    topologies = [topology(part) for part in islands]
    # Separate nested shells in one instance may describe an empty cavity. Treat
    # their solid semantics as uncertain rather than filling each shell independently.
    instance_groups = {}
    for index, part in enumerate(islands):
        instance_groups.setdefault(part['label'].rsplit('/island', 1)[0], []).append(index)
    for ids in instance_groups.values():
        for offset, i in enumerate(ids):
            for j in ids[offset + 1:]:
                a, b = islands[i], islands[j]
                contains = any(all(outer['lo'][k] <= inner['lo'][k] + args.ray_epsilon_m and
                                   outer['hi'][k] >= inner['hi'][k] - args.ray_epsilon_m for k in range(3))
                               for outer, inner in ((a, b), (b, a)))
                if contains:
                    for index in (i, j):
                        topologies[index]['nested_shell_semantics_untested'] = True
                        topologies[index]['closed_oriented_solid_candidate'] = False
    work = Work(args.max_work)
    directions = [Vector(v).normalized() for v in ((1, .371, .173), (-.217, 1, .413), (.317, .269, 1))]
    records = []
    count = len(islands)
    context_count = sum(not part['asset'] for part in islands)
    eligible = count * (count - 1) // 2 - context_count * (context_count - 1) // 2
    incomplete = False
    for i, a in enumerate(islands):
        if incomplete:
            break
        for j in range(i + 1, len(islands)):
            b = islands[j]
            if not (a['asset'] or b['asset']):
                continue
            try:
                resolution = allowance_resolutions.get(tuple(sorted((a['object'], b['object']))))
                applicable = (resolution['definition'] if resolution and
                              resolution['status'] == 'unique_evaluated_pair' else None)
                result = pair_check(a, b, topologies[i], topologies[j], applicable, args, work, directions)
                result['allowance_resolution'] = resolution
            except IncompleteQuery:
                incomplete = True
                break
            records.append(result)
            if result['status'] == 'incomplete':
                incomplete = True
                break
    asset_count = sum(p['asset'] for p in islands)
    ambiguous_allowances = sum(result.get('allowance_resolution', {}).get('status') ==
                               'ambiguous_multiple_evaluated_instances'
                               for result in records if result.get('allowance_resolution') is not None)
    after = digest(source)
    if before != after:
        raise RuntimeError('Input changed during audit; refusing stable-revision report')
    if allowance_meta and digest(Path(allowance_meta['path'])) != allowance_meta['sha256']:
        raise RuntimeError('Allowance file changed during audit')
    counts = {}
    for record in records:
        counts[record['status']] = counts.get(record['status'], 0) + 1
    report = {'schema_version': 1, 'input': str(source), 'input_sha256': before, 'input_sha256_after': after,
              'blender_version': bpy.app.version_string,
              'status': 'incomplete' if incomplete or not asset_count or excluded or ambiguous_allowances else 'complete',
              'geometry_scope_coverage': 'partial_unsupported_geometry' if excluded else 'evaluated_mesh_geometry_only',
              'excluded_unsupported_objects': excluded,
              'artistic_acceptance': 'not-assessed', 'certified_clearance': False,
              'penetration_metric': {'name': 'maximum_sampled_interior_nearest_surface_distance',
                                     'unit': 'metre', 'certified_maximum': False,
                                     'not_measured': ['axial embed extent', 'minimum translation to separate', 'continuous collision']},
              'scope': {'collection': args.collection, 'against_objects': args.against,
                        'against_collections': args.against_collection,
                        'resolved_context_objects': sorted(context_names),
                        'frame': bpy.context.scene.frame_current, 'view_layer': bpy.context.view_layer.name,
                        'evaluation_mode': graph.mode,
                        'basis': 'Asset islands against each other and explicit context islands; context-context pairs excluded'},
              'settings': {'tolerance_m': args.tolerance_m, 'metres_per_blender_unit': scale,
                           'samples_per_face': args.samples_per_face, 'ray_epsilon_m': args.ray_epsilon_m,
                           'max_hits_per_ray': args.max_hits_per_ray, 'max_work': args.max_work},
              'counts': {'asset_islands': asset_count, 'context_islands': sum(not p['asset'] for p in islands),
                         'evaluated_mesh_instances': len(objects), 'eligible_pairs': eligible,
                         'recorded_pairs': len(records), 'unclassified_pairs': eligible - len(records),
                         'ambiguous_allowance_pairs': ambiguous_allowances, 'pair_statuses': counts}, 'work': work.report(), 'objects': objects,
              'islands': [{k: part[k] for k in ('id', 'label', 'object', 'parent', 'asset')}
                          | {'topology': {k: v for k, v in topologies[i].items() if k != 'edges'},
                             'bounds_m': [list(part['lo']), list(part['hi'])]} for i, part in enumerate(islands)],
              'pairs': records, 'allowances': allowance_meta,
              'findings': ([{'level': 'error', 'code': 'no_mesh_geometry_in_scope'}] if not asset_count else []) +
                          ([{'level': 'warning', 'code': 'unsupported_non_mesh_geometry_partial_coverage', 'objects': excluded}] if excluded else []) +
                          ([{'level': 'warning', 'code': 'viewport_render_modifier_difference'}]
                           if any(obj['modifier_visibility_mismatch'] for obj in objects) else []),
              'method': 'AABB broadphase only; symmetric vertices/triangle samples; bounded edge-to-BVH crossing intervals; nearest-surface distance plus three agreeing parity rays for closed oriented solid candidates.',
              'limitations': [
                  'Maximum sampled interior distance is penetration evidence, not a certified maximum depth or minimum translation to separate objects. Small missed penetrations remain possible.',
                  'Within-allowance-at-samples needs visual review; max_interior_distance_m limits the sampled nearest-surface metric, not axial embed extent or minimum translation. An observed exceedance beyond numeric ray epsilon is flagged even below the generic tolerance.',
                  'Object-pair allowances are not applied when a source name has multiple evaluated placements; candidate instance IDs/parents are reported and allowance resolution remains incomplete.',
                  'Unsupported asset geometry makes coverage incomplete. Unsupported explicit context objects/collection members are rejected, or reported as partial when encountered through evaluated instances.',
                  'Open/nonmanifold/inconsistently wound/zero-volume surfaces and nested shells of one instance cannot establish solid inside/outside and remain uncertain when bounds overlap; a cavity is not filled as independent solids.',
                  'Self-intersection within one connected face island is UNTESTED, including limbs folded through the same body mesh. Inspect poses, self-collision and alternate animation frames separately.',
                  'Closedness and winding do not prove a valid non-self-intersecting solid. Coincident faces, tiny gaps and numeric precision may make parity uncertain.',
                  'Opaque geometric surfaces only; alpha cards, transparent materials, cloth/thin sheets, collision proxies, render restrictions and designed intersections require interpretation.',
                  'Only saved current frame/view layer evaluated. Animation motion, other poses/states and render/export evaluation require separate checks.',
                  'World transforms, declared unit scale, evaluated modifiers and instances are included. Primary-file SHA does not cover linked files or external glTF dependencies.',
                  'Work counts pair/edge/probe checks, nearest queries and ray queries; per-ray hit count is bounded. It is not a memory or wall-clock limit; extraction/BVH construction and topology scans precede the query budget.',
                  'Contact/support audit and intersection audit are independent; being supported does not establish freedom from penetration. No model mutation or automatic fix.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    print(json.dumps({'report': str(args.output.resolve()), 'status': report['status'], 'counts': report['counts']}))
    return 2 if report['status'] == 'incomplete' else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'Intersection audit failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        sys.exit(1)
