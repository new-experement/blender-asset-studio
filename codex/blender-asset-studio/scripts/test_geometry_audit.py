#!/usr/bin/env python3
"""Integration tests; creates temporary fixtures in separate background Blender only.

Run ordinary Python: test_geometry_audit.py --blender /path/to/Blender
No project asset is opened or saved. Requires Blender's bundled glTF importer/exporter.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('audit_geometry.py')
BLENDER = '/Applications/Blender.app/Contents/MacOS/Blender'
FIXTURE_CODE = r'''
import bpy, os
from mathutils import Matrix
bpy.ops.wm.read_factory_settings(use_empty=True)
root = os.environ['GEOMETRY_AUDIT_TEST_DIR']
def col(name):
    c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c
def cube(name, location, size, collection):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    o=bpy.context.object; o.name=name; o.scale=size
    for c in list(o.users_collection): c.objects.unlink(o)
    collection.objects.link(o)
    return o
def face(name, vertices, collection):
    m=bpy.data.meshes.new(name); m.from_pydata(vertices,[],[(0,1,2,3)]); m.update()
    o=bpy.data.objects.new(name,m); collection.objects.link(o); return o
chain=col('Chain')
cube('Base',(0,0,.5),(1,1,1),chain)
cube('Within',(0,0,1.502),(1,1,1),chain)
cube('ChainTop',(0,0,2.504),(1,1,1),chain)
cube('Outside',(3,0,1.504),(1,1,1),chain)
cube('SeparateBase',(3,0,.5),(1,1,1),chain)
cube('Buried',(6,0,-2),(1,1,1),chain)
cube('Float',(9,0,2),(1,1,1),chain)
hang=col('Hanging')
cube('HangingPart',(20,0,3),(1,1,1),hang)
ctx=col('Context')
cube('Anchor',(20,0,4),(2,2,1),ctx)
cube('Unrelated',(0,0,20),(80,80,1),ctx)
vis=col('Visibility')
face('Panel',[(30,0,0),(32,0,0),(32,2,0),(30,2,0)],vis)
# The +Z view sees only a small near-edge sliver. Centroid-only misses one triangle;
# near-corner samples recover both even though the centroid and most area is covered.
face('PartialCover',[(30,0,.1),(31.8,0,.1),(31.8,2,.1),(30,2,.1)],ctx)
under=col('Underside')
cube('Box',(40,0,1),(2,2,2),under)
mods=col('ModifiersInstances')
seed=cube('Seed',(50,0,1),(1,1,1),mods)
modifier=seed.modifiers.new('TwoCopies','ARRAY'); modifier.count=2; modifier.relative_offset_displace=(2,0,0)
# Instance of the same evaluated source through a collection outside the scene tree.
instance_source=bpy.data.collections.new('InstanceSource')
cube('InstancedCube',(0,0,0),(1,1,1),instance_source)
instance=bpy.data.objects.new('Emitter',None); instance.instance_type='COLLECTION'; instance.instance_collection=instance_source
instance.location=(54,0,1); mods.objects.link(instance)
bbox=col('AABBOnly')
cube('OuterShell',(70,0,1),(4,4,2),bbox)
cube('NestedNoSurfaceContact',(70,0,1),(.2,.2,.2),bbox)
empty=col('Empty')
# Two disjoint cubes joined into one object must still be two face islands.
islandcol=col('Disconnected')
a=cube('JoinedA',(60,0,.5),(1,1,1),islandcol)
b=cube('JoinedB',(62,0,3),(1,1,1),islandcol)
bpy.ops.object.select_all(action='DESELECT'); a.select_set(True); b.select_set(True); bpy.context.view_layer.objects.active=a
bpy.ops.object.join()
bpy.ops.wm.save_as_mainfile(filepath=root+'/fixture.blend')
# Declared unit conversion: 0.3 Blender-unit gap = 3mm at centimetre scale.
bpy.context.scene.unit_settings.system='METRIC'; bpy.context.scene.unit_settings.scale_length=.01
scaled=col('Scaled')
cube('CentimetreBase',(0,10,50),(100,100,100),scaled)
cube('CentimetreTop',(0,10,150.2),(100,100,100),scaled)
bpy.ops.wm.save_as_mainfile(filepath=root+'/scaled.blend')
# A small GLB round-trip establishes explicit importer support.
bpy.ops.object.select_all(action='DESELECT'); seed.select_set(True)
bpy.ops.export_scene.gltf(filepath=root+'/fixture.glb',use_selection=True,export_format='GLB')
bpy.ops.export_scene.gltf(filepath=root+'/fixture.gltf',use_selection=True,export_format='GLTF_SEPARATE')
'''


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GeometryAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='geometry-audit-test-')
        cls.root = Path(cls.temp.name)
        fixture = cls.root / 'make_fixture.py'
        fixture.write_text(FIXTURE_CODE)
        env = dict(os.environ, GEOMETRY_AUDIT_TEST_DIR=str(cls.root))
        result = subprocess.run([BLENDER, '--background', '--factory-startup', '--disable-autoexec',
                                 '--threads', '2', '--python-exit-code', '1', '--python', str(fixture)],
                                capture_output=True, text=True, env=env, timeout=120)
        if result.returncode:
            raise RuntimeError('Fixture creation failed:\n' + result.stdout + result.stderr)
        cls.initial_hashes = {p.name: checksum(p) for p in cls.root.iterdir() if p.suffix in {'.blend', '.glb', '.gltf', '.bin'}}
        cls.serial = 0

    @classmethod
    def tearDownClass(cls):
        for name, expected in cls.initial_hashes.items():
            if checksum(cls.root / name) != expected:
                raise AssertionError('Fixture changed: ' + name)
        cls.temp.cleanup()

    def run_audit(self, *options, source='fixture.blend', expect=0, output=None):
        type(self).serial += 1
        report = output or self.root / f'report_{self.serial}.json'
        result = subprocess.run([BLENDER, '--background', '--factory-startup', '--disable-autoexec',
                                 '--threads', '2', '--python-exit-code', '1', '--python', str(SCRIPT), '--',
                                 '--input', str(self.root / source), '--output', str(report), *options],
                                capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        if expect == 0 or (expect == 2 and report.exists()):
            data = json.loads(report.read_text())
            self.assertEqual(data['input_sha256'], self.initial_hashes[source])
            self.assertEqual(data['input_sha256_after'], self.initial_hashes[source])
            return data
        return result

    def test_chain_gap_buried_floating(self):
        r = self.run_audit('--check', 'contacts', '--collection', 'Chain', '--ground-z-m', '0')
        c = r['checks']['contacts']
        names = {p['id']: p['object'] for p in r['islands']}
        supported = {names[i] for i in c['supported_asset_islands']}
        self.assertEqual(supported, {'Base', 'Within', 'ChainTop', 'SeparateBase'})
        self.assertEqual({names[i] for i in c['fully_below_ground_islands']}, {'Buried'})
        unresolved = {names[i] for g in c['unresolved_components'] for i in g['islands']}
        self.assertEqual(unresolved, {'Outside', 'Buried', 'Float'})
        self.assertTrue(all(g['classification'] == 'unsupported_candidate' for g in c['unresolved_components']))
        self.assertEqual(r['counts']['asset_mesh_instances'], 7)

    def test_aabb_overlap_is_not_contact(self):
        r = self.run_audit('--check', 'contacts', '--collection', 'AABBOnly', '--ground-z-m', '0')
        c = r['checks']['contacts']
        names = {p['id']: p['object'] for p in r['islands']}
        self.assertEqual({names[i] for i in c['supported_asset_islands']}, {'OuterShell'})
        self.assertEqual({names[i] for g in c['unresolved_components'] for i in g['islands']}, {'NestedNoSurfaceContact'})
        self.assertEqual(c['contact_links'], [])

    def test_hanging_anchor_and_no_anchor(self):
        r = self.run_audit('--check', 'contacts', '--collection', 'Hanging')
        self.assertFalse(r['checks']['contacts']['support_specified'])
        self.assertEqual(r['checks']['contacts']['unresolved_components'][0]['classification'], 'unanchored_no_support_declared')
        r = self.run_audit('--check', 'contacts', '--collection', 'Hanging', '--anchor', 'Anchor')
        self.assertEqual(len(r['checks']['contacts']['supported_asset_islands']), 1)
        self.assertEqual(r['checks']['contacts']['unresolved_components'], [])
        self.assertEqual(r['counts']['context_islands'], 1)
        # A visibility occluder must not silently become a contact-chain anchor.
        r = self.run_audit('--check', 'contacts', '--collection', 'Hanging', '--occluder', 'Anchor', '--ground-z-m', '4')
        self.assertEqual(r['checks']['contacts']['supported_asset_islands'], [])

    def test_partly_visible_more_than_centroid_and_scope(self):
        r = self.run_audit('--check', 'visibility', '--collection', 'Visibility', '--occluder', 'PartialCover',
                           '--elevations=90', '--azimuths=0', '--samples-per-face', '7')
        self.assertEqual(r['checks']['visibility']['counts']['sampled_visible'], 2)
        self.assertEqual(r['counts']['context_islands'], 1)  # Unrelated overhead slab excluded.
        r = self.run_audit('--check', 'visibility', '--collection', 'Visibility', '--occluder', 'PartialCover',
                           '--elevations=90', '--azimuths=0', '--samples-per-face', '1')
        self.assertEqual(r['checks']['visibility']['counts']['candidate_unseen'], 2)

    def test_restricted_and_unrestricted_underside(self):
        top = self.run_audit('--check', 'visibility', '--collection', 'Underside',
                             '--elevations=90', '--azimuths=0')
        both = self.run_audit('--check', 'visibility', '--collection', 'Underside',
                              '--elevations=-90,90', '--azimuths=0')
        # Horizontal upper/lower surfaces differ by exactly two triangles.
        self.assertEqual(top['checks']['visibility']['counts']['sampled_visible'], 2)
        self.assertEqual(both['checks']['visibility']['counts']['sampled_visible'], 4)
        with_ground = self.run_audit('--check', 'visibility', '--collection', 'Underside',
                                     '--elevations=-90,90', '--azimuths=0', '--ground-z-m', '0')
        self.assertEqual(with_ground['checks']['visibility']['counts']['sampled_visible'], 2)

    def test_instances_modifiers_islands_and_unit_scale(self):
        r = self.run_audit('--check', 'contacts', '--collection', 'ModifiersInstances')
        self.assertEqual(r['counts']['asset_triangles'], 36)
        self.assertEqual(r['counts']['asset_islands'], 3)
        self.assertTrue(any(o['instance'] for o in r['objects']))
        r = self.run_audit('--check', 'contacts', '--collection', 'Disconnected', '--ground-z-m', '0')
        self.assertEqual(r['counts']['asset_mesh_instances'], 1)
        self.assertEqual(r['counts']['asset_islands'], 2)
        self.assertEqual(len(r['checks']['contacts']['supported_asset_islands']), 1)
        r = self.run_audit('--check', 'contacts', '--collection', 'Scaled', '--ground-z-m', '0', source='scaled.blend')
        self.assertAlmostEqual(r['settings']['metres_per_blender_unit'], .01)
        self.assertEqual(len(r['checks']['contacts']['supported_asset_islands']), 2)

    def test_work_cap_never_calls_untested_hidden(self):
        r = self.run_audit('--check', 'visibility', '--collection', 'Underside', '--max-work', '1', expect=2)
        counts = r['checks']['visibility']['counts']
        self.assertEqual(r['status'], 'incomplete')
        self.assertEqual(counts['candidate_unseen'], 0)
        self.assertEqual(sum(counts[k] for k in ('sampled_visible', 'candidate_unseen', 'unclassified')), 12)
        self.assertGreater(counts['unclassified'], 0)
        r = self.run_audit('--check', 'contacts', '--collection', 'Chain', '--ground-z-m', '0', '--max-work', '1', expect=2)
        self.assertTrue(all(g['classification'] == 'support_unresolved_incomplete'
                            for g in r['checks']['contacts']['unresolved_components']))

    def test_glb_and_gltf_and_no_change(self):
        for source in ('fixture.glb', 'fixture.gltf'):
            r = self.run_audit('--check', 'contacts', source=source)
            self.assertGreaterEqual(r['counts']['asset_triangles'], 12)

    def test_empty_missing_invalid_and_overwrite(self):
        r = self.run_audit('--check', 'contacts', '--collection', 'Empty', expect=2)
        self.assertEqual(r['findings'][0]['code'], 'no_mesh_geometry_in_scope')
        for flags in (('--collection', 'Missing'), ('--tolerance-m', '-.1'), ('--max-work', '0'),
                      ('--elevations=100',), ('--anchor', 'Missing')):
            self.run_audit(*flags, expect=1)
        self.run_audit(source='missing.blend', expect=1)
        output = self.root / 'existing.json'
        output.write_text('DO NOT CHANGE')
        self.run_audit(output=output, expect=1)
        self.assertEqual(output.read_text(), 'DO NOT CHANGE')
        result = subprocess.run([sys.executable, str(SCRIPT), '--input', str(self.root / 'fixture.blend'),
                                 '--output', str(self.root / 'python.json')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('background Blender', result.stderr)
        self.assertFalse((self.root / 'python.json').exists())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', default=BLENDER)
    args, remaining = parser.parse_known_args()
    BLENDER = args.blender
    unittest.main(argv=[sys.argv[0], *remaining], verbosity=2)
