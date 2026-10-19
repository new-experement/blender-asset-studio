#!/usr/bin/env python3
"""Temporary integration fixtures for audit_intersections.py; never opens project assets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

BLENDER = '/Applications/Blender.app/Contents/MacOS/Blender'
SCRIPT = Path(__file__).with_name('audit_intersections.py')
FIXTURE_CODE = r'''
import bpy, os
bpy.ops.wm.read_factory_settings(use_empty=True)
root=os.environ['INTERSECTION_AUDIT_TEST_DIR']
def col(name):
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c
def cube(name, location, size, collection):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    o=bpy.context.object; o.name=name; o.scale=size
    for c in list(o.users_collection): c.objects.unlink(o)
    collection.objects.link(o); return o
def pair(name,offset,x):
    c=col(name)
    cube(name+'A',(x,0,0),(1,1,1),c)
    cube(name+'B',(x+1-offset,0,0),(1,1,1),c)
pair('Touch',0,0); pair('Shallow',.002,4); pair('Deep',.2,8); pair('Gap',-.002,12)
c=col('Contained'); cube('Large',(20,0,0),(4,4,4),c); cube('Small',(20,0,0),(.4,.4,.4),c)
c=col('Cross'); cube('LongX',(30,0,0),(4,.4,.4),c); cube('LongY',(30,0,0),(.4,4,.4),c)
c=col('Coincident'); cube('CoincidentA',(40,0,0),(1,1,1),c); cube('CoincidentB',(40,0,0),(1,1,1),c)
c=col('Actor'); cube('Arm',(50,0,0),(2,.4,.4),c)
ctx=col('Context'); cube('Wall',(50.7,0,0),(.2,4,4),ctx)
cube('Unrelated',(0,0,0),(100,100,100),ctx)
c=col('Open'); cube('Closed',(60,0,0),(1,1,1),c)
m=bpy.data.meshes.new('OpenMesh'); m.from_pydata([(59,-1,0),(61,-1,0),(61,1,0),(59,1,0)],[],[(0,1,2,3)]); m.update()
o=bpy.data.objects.new('Plane',m); c.objects.link(o)
c=col('Evaluated'); a=cube('ArraySeed',(70,0,0),(1,1,1),c)
mod=a.modifiers.new('Copies','ARRAY'); mod.count=2; mod.relative_offset_displace=(.8,0,0)
src=bpy.data.collections.new('InstanceSource'); cube('InstanceCube',(0,0,0),(1,1,1),src)
emitter=bpy.data.objects.new('Emitter',None); emitter.instance_type='COLLECTION'; emitter.instance_collection=src; emitter.location=(70,0,0); c.objects.link(emitter)
c=col('Frame'); a=cube('AnimatedA',(80,0,0),(1,1,1),c)
b=cube('AnimatedB',(83,0,0),(1,1,1),c); b.keyframe_insert(data_path='location',frame=1)
b.location.x=80.8; b.keyframe_insert(data_path='location',frame=7); bpy.context.scene.frame_set(7)
c=col('Cavity'); a=cube('Shell',(90,0,0),(4,4,4),c); b=cube('Inner',(90,0,0),(2,2,2),c)
# Reverse inner winding, join to make a conventional hollow shell object.
for poly in b.data.polygons: pass
import bmesh
bm=bmesh.new(); bm.from_mesh(b.data); bmesh.ops.reverse_faces(bm,faces=list(bm.faces)); bm.to_mesh(b.data); bm.free()
bpy.ops.object.select_all(action='DESELECT'); a.select_set(True); b.select_set(True); bpy.context.view_layer.objects.active=a; bpy.ops.object.join()
cube('InsideCavity',(90,0,0),(.4,.4,.4),c)
def curve(name, collection, x):
    data=bpy.data.curves.new(name,'CURVE'); data.dimensions='3D'; data.bevel_depth=.02
    spline=data.splines.new('POLY'); spline.points.add(1)
    spline.points[0].co=(x,0,0,1); spline.points[1].co=(x+1,0,0,1)
    obj=bpy.data.objects.new(name,data); collection.objects.link(obj); return obj
mixed=col('MixedContext'); cube('MixedLeg',(110,0,0),(1,1,1),mixed); curve('CurveTabletop',mixed,110)
partial=col('PartialAsset'); cube('PartialMesh',(115,0,0),(1,1,1),partial); curve('AssetCurve',partial,115)
postsource=bpy.data.collections.new('PostSource'); cube('Post',(0,0,0),(1,1,1),postsource)
posts=col('PostInstances')
for name, x in [('PostPlacementA',100),('PostPlacementB',103)]:
    inst=bpy.data.objects.new(name,None); inst.instance_type='COLLECTION'; inst.instance_collection=postsource
    inst.location=(x,0,0); posts.objects.link(inst)
cube('Footing',(101.5,0,-.4),(5,2,1),col('FootingContext'))
col('Empty')
bpy.ops.wm.save_as_mainfile(filepath=root+'/fixture.blend')
# Centimetre units, 2mm physical overlap.
bpy.context.scene.unit_settings.system='METRIC'; bpy.context.scene.unit_settings.scale_length=.01
c=col('Scaled'); cube('ScaledA',(0,100,0),(100,100,100),c); cube('ScaledB',(99.8,100,0),(100,100,100),c)
bpy.ops.wm.save_as_mainfile(filepath=root+'/scaled.blend')
# Millimetre declared units, 20cm overlap at physical size1m.
bpy.context.scene.unit_settings.scale_length=.001
c=col('Millimetre'); cube('MMA',(0,1000,0),(1000,1000,1000),c); cube('MMB',(800,1000,0),(1000,1000,1000),c)
bpy.ops.wm.save_as_mainfile(filepath=root+'/millimetre.blend')
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.collections['Deep'].objects: o.select_set(True)
bpy.ops.export_scene.gltf(filepath=root+'/fixture.glb',use_selection=True,export_format='GLB')
bpy.ops.export_scene.gltf(filepath=root+'/fixture.gltf',use_selection=True,export_format='GLTF_SEPARATE')
'''


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class IntersectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='intersection-audit-test-')
        cls.root = Path(cls.temp.name)
        fixture = cls.root / 'make_fixture.py'
        fixture.write_text(FIXTURE_CODE)
        env = dict(os.environ, INTERSECTION_AUDIT_TEST_DIR=str(cls.root))
        result = subprocess.run([BLENDER, '--background', '--factory-startup', '--disable-autoexec',
                                 '--threads', '2', '--python-exit-code', '1', '--python', str(fixture)],
                                capture_output=True, text=True, env=env, timeout=120)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        cls.hashes = {p.name: checksum(p) for p in cls.root.iterdir() if p.suffix in {'.blend', '.glb', '.gltf', '.bin'}}
        cls.serial = 0

    @classmethod
    def tearDownClass(cls):
        for name, before in cls.hashes.items():
            if checksum(cls.root / name) != before:
                raise AssertionError('Fixture changed: ' + name)
        cls.temp.cleanup()

    def run_audit(self, *flags, source='fixture.blend', expect=0, output=None):
        type(self).serial += 1
        path = output or self.root / f'report{self.serial}.json'
        result = subprocess.run([BLENDER, '--background', '--factory-startup', '--disable-autoexec', '--threads', '2',
                                 '--python-exit-code', '1', '--python', str(SCRIPT), '--', '--input',
                                 str(self.root / source), '--output', str(path), *flags],
                                capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        if path.exists() and expect in (0, 2):
            data = json.loads(path.read_text())
            self.assertEqual(data['input_sha256'], self.hashes[source])
            self.assertEqual(data['input_sha256_after'], self.hashes[source])
            self.assertFalse(data['certified_clearance'])
            return data
        return result

    def only_pair(self, collection, **options):
        r = self.run_audit('--collection', collection, **options)
        self.assertEqual(r['counts']['recorded_pairs'], 1)
        return r['pairs'][0]

    def test_touch_shallow_deep_and_near_gap(self):
        touch = self.only_pair('Touch')
        self.assertEqual(touch['status'], 'touching_or_shallow_within_tolerance_at_samples')
        self.assertAlmostEqual(touch['max_sampled_interior_distance_m'], 0, places=5)
        shallow = self.only_pair('Shallow')
        self.assertEqual(shallow['status'], 'touching_or_shallow_within_tolerance_at_samples')
        self.assertAlmostEqual(shallow['max_sampled_interior_distance_m'], .002, places=4)
        deep = self.only_pair('Deep')
        self.assertEqual(deep['status'], 'penetration_candidate')
        self.assertGreater(deep['max_sampled_interior_distance_m'], .19)
        gap = self.only_pair('Gap')
        self.assertEqual(gap['status'], 'touching_or_shallow_within_tolerance_at_samples')
        self.assertEqual(gap['max_sampled_interior_distance_m'], 0)

    def test_containment_coincident_and_thin_cross(self):
        for name in ('Contained', 'Coincident', 'Cross'):
            pair = self.only_pair(name)
            self.assertEqual(pair['status'], 'penetration_candidate', pair)
            self.assertGreater(pair['max_sampled_interior_distance_m'], .01)
        cross = self.only_pair('Cross')
        self.assertGreater(cross['edge_surface_hits'], 0)
        # Both cross bars have all original vertices outside the other bar by construction.
        self.assertTrue(any(p['basis'] in ('edge_crossing_interval_midpoint', 'surface_sample', 'verified_source_interior_witness')
                            for p in cross['evidence_points']))

    def test_context_scope_and_collection(self):
        r = self.run_audit('--collection', 'Actor')
        self.assertEqual(r['counts']['eligible_pairs'], 0)
        r = self.run_audit('--collection', 'Actor', '--against', 'Wall')
        self.assertEqual(r['counts']['context_islands'], 1)
        self.assertEqual(r['pairs'][0]['status'], 'penetration_candidate')
        r = self.run_audit('--collection', 'Actor', '--against-collection', 'Context')
        self.assertEqual(r['counts']['context_islands'], 2)
        self.assertEqual(r['counts']['eligible_pairs'], 2)

    def test_allowance_is_pair_specific_and_exceedance_remains(self):
        path = self.root / 'allowance.json'
        data = {'pairs': [{'objects': ['DeepA', 'DeepB'], 'max_interior_distance_m': .25, 'reason': 'Designed footing'}]}
        path.write_text(json.dumps(data))
        r = self.run_audit('--collection', 'Deep', '--allowances', str(path))
        self.assertEqual(r['pairs'][0]['status'], 'within_allowance_at_samples')
        self.assertFalse(r['pairs'][0]['depth_is_certified_maximum'])
        data['pairs'][0]['max_interior_distance_m'] = .05
        path.write_text(json.dumps(data))
        r = self.run_audit('--collection', 'Deep', '--allowances', str(path))
        self.assertEqual(r['pairs'][0]['status'], 'penetration_candidate')
        self.assertTrue(r['pairs'][0]['allowance_exceeded_by_sample'])
        r = self.run_audit('--collection', 'Cross', '--allowances', str(path))
        self.assertEqual(r['pairs'][0]['status'], 'penetration_candidate')
        self.assertIsNone(r['pairs'][0]['allowance'])

    def test_explicit_context_rejects_mixed_unsupported_and_asset_is_partial(self):
        result = self.run_audit('--collection', 'Actor', '--against-collection', 'MixedContext', expect=1)
        self.assertIn('CurveTabletop', result.stderr)
        self.run_audit('--collection', 'Actor', '--against', 'CurveTabletop', expect=1)
        r = self.run_audit('--collection', 'PartialAsset', expect=2)
        self.assertEqual(r['geometry_scope_coverage'], 'partial_unsupported_geometry')
        self.assertIn('AssetCurve', r['excluded_unsupported_objects'])
        self.assertTrue(any(f['code'] == 'unsupported_non_mesh_geometry_partial_coverage' for f in r['findings']))

    def test_allowance_below_contact_tolerance_still_exceeds(self):
        path = self.root / 'narrow_allowance.json'
        for limit in (0, .001):
            path.write_text(json.dumps({'pairs': [{'objects': ['ShallowA', 'ShallowB'],
                                                  'max_interior_distance_m': limit, 'reason': 'Exact limited join'}]}))
            r = self.run_audit('--collection', 'Shallow', '--tolerance-m', '.003', '--allowances', str(path))
            pair = r['pairs'][0]
            self.assertEqual(pair['status'], 'penetration_candidate')
            self.assertTrue(pair['allowance_exceeded_by_sample'])
            self.assertAlmostEqual(pair['max_sampled_interior_distance_m'], .002, places=4)
            self.assertIn('not axial embed', pair['metric'])

    def test_allowance_does_not_apply_to_multiple_post_instances(self):
        path = self.root / 'post_allowance.json'
        path.write_text(json.dumps({'pairs': [{'objects': ['Post', 'Footing'],
                                              'max_interior_distance_m': 10, 'reason': 'One intended join'}]}))
        r = self.run_audit('--collection', 'PostInstances', '--against', 'Footing', '--allowances', str(path), expect=2)
        self.assertEqual(r['counts']['ambiguous_allowance_pairs'], 2)
        pairs = [p for p in r['pairs'] if p['allowance_resolution']]
        self.assertEqual(len(pairs), 2)
        for pair in pairs:
            self.assertIsNone(pair['allowance'])
            resolution = pair['allowance_resolution']
            self.assertEqual(resolution['status'], 'ambiguous_multiple_evaluated_instances')
            self.assertEqual({p['parent'] for p in resolution['instance_candidates']['Post']},
                             {'PostPlacementA', 'PostPlacementB'})
            self.assertTrue(all(p['id'] for p in resolution['instance_candidates']['Post']))
            self.assertEqual(pair['status'], 'penetration_candidate')

    def test_open_plane_and_hollow_shell_are_uncertain(self):
        pair = self.only_pair('Open')
        self.assertEqual(pair['status'], 'uncertain_solid_semantics')
        r = self.run_audit('--collection', 'Cavity')
        self.assertTrue(all(p['status'] == 'uncertain_solid_semantics' for p in r['pairs']))
        self.assertTrue(any(i['topology'].get('nested_shell_semantics_untested') for i in r['islands']))
        self.assertTrue(all(i['topology']['self_intersection'] == 'untested' for i in r['islands']))

    def test_units_modifiers_instances_and_saved_frame(self):
        scaled = self.only_pair('Scaled', source='scaled.blend')
        self.assertEqual(scaled['status'], 'touching_or_shallow_within_tolerance_at_samples')
        self.assertAlmostEqual(scaled['max_sampled_interior_distance_m'], .002, places=4)
        mm = self.only_pair('Millimetre', source='millimetre.blend')
        self.assertEqual(mm['status'], 'penetration_candidate')
        self.assertAlmostEqual(mm['max_sampled_interior_distance_m'], .2, places=4)
        r = self.run_audit('--collection', 'Evaluated')
        self.assertEqual(r['counts']['asset_islands'], 3)
        self.assertTrue(any(o['instance'] for o in r['objects']))
        self.assertGreater(sum(p['status'] == 'penetration_candidate' for p in r['pairs']), 0)
        r = self.run_audit('--collection', 'Frame')
        self.assertEqual(r['scope']['frame'], 7)
        self.assertEqual(r['pairs'][0]['status'], 'penetration_candidate')

    def test_budget_is_incomplete_not_clean(self):
        r = self.run_audit('--collection', 'Cross', '--max-work', '2', expect=2)
        self.assertEqual(r['status'], 'incomplete')
        self.assertEqual(r['pairs'][0]['status'], 'incomplete')
        self.assertTrue(r['work']['exhausted'])
        r = self.run_audit('--collection', 'Actor', '--against-collection', 'Context', '--max-work', '1', expect=2)
        self.assertGreater(r['counts']['unclassified_pairs'], 0)
        r = self.run_audit('--collection', 'Contained', '--max-hits-per-ray', '1', expect=2)
        self.assertEqual(r['pairs'][0]['incomplete_reason'], 'per_ray_hit_cap')

    def test_glb_gltf_no_mutation_and_invalid_inputs(self):
        for source in ('fixture.glb', 'fixture.gltf'):
            r = self.run_audit(source=source)
            self.assertGreater(r['counts']['asset_islands'], 0)
        r = self.run_audit('--collection', 'Empty', expect=2)
        self.assertEqual(r['findings'][0]['code'], 'no_mesh_geometry_in_scope')
        for flags in (('--collection', 'Missing'), ('--against', 'Missing'), ('--against-collection', 'Missing'),
                      ('--tolerance-m', '-1'), ('--max-work', '0'), ('--max-hits-per-ray', '0'),
                      ('--against-collection', 'Empty')):
            self.run_audit(*flags, expect=1)
        self.run_audit(source='missing.blend', expect=1)
        output = self.root / 'existing.json'; output.write_text('KEEP')
        self.run_audit(output=output, expect=1)
        self.assertEqual(output.read_text(), 'KEEP')
        invalid = self.root / 'invalid.json'; invalid.write_text(json.dumps({'pairs':[{'objects':['*','Wall'],'max_interior_distance_m':10,'reason':'all'}]}))
        self.run_audit('--allowances', str(invalid), expect=1)
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('background Blender', result.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', default=BLENDER)
    args, rest = parser.parse_known_args()
    BLENDER = args.blender
    unittest.main(argv=[sys.argv[0], *rest], verbosity=2)
