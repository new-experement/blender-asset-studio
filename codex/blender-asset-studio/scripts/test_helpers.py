#!/usr/bin/env python3
"""Small isolated regression suite; optionally exercise a real Blender executable."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
BLENDER = None


def run(command, timeout=90):
    return subprocess.run(command, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout)


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        from PIL import Image
        self.scratch = tempfile.TemporaryDirectory(prefix="blender-studio-comparison-")
        self.root = Path(self.scratch.name)
        self.reference = self.root / "reference.png"
        self.candidate = self.root / "candidate.png"
        Image.new("RGBA", (200, 100), (255, 0, 0, 128)).save(self.reference)
        Image.new("RGB", (80, 160), "blue").save(self.candidate)
        self.regions = self.root / "regions.json"
        self.regions.write_text(json.dumps([{"id": "detail", "reference": [0, 0, 0.5, 1],
                                             "candidate": [0, 0.5, 1, 1]}]))
        self.output = self.root / "comparison"

    def tearDown(self):
        self.scratch.cleanup()

    def command(self):
        return [sys.executable, str(SCRIPTS / "compare_views.py"), "--reference", str(self.reference),
                "--candidate", str(self.candidate), "--regions", str(self.regions),
                "--output", str(self.output), "--panel-size", "128"]

    def test_success_preserves_inputs_and_aspect(self):
        from PIL import Image
        before = self.reference.read_bytes(), self.candidate.read_bytes()
        result = run(self.command())
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(before, (self.reference.read_bytes(), self.candidate.read_bytes()))
        metadata = json.loads((self.output / "provenance.json").read_text())
        self.assertEqual(metadata["inputs"][0]["sha256"], hashlib.sha256(before[0]).hexdigest())
        self.assertEqual(metadata["evidence"][0]["pixel_boxes"]["reference"], [0, 0, 100, 100])
        self.assertEqual(metadata["artistic_acceptance"], "not-assessed")
        with Image.open(self.output / "contact-sheet.png") as sheet:
            self.assertEqual(sheet.size, (256, 320))
        with Image.open(self.output / "overview.png") as overview:
            # Wide reference keeps letterboxing, transparency composites, portrait stays narrow.
            top = overview.getpixel((4, 40))
            self.assertEqual(top[0], top[1])
            middle = overview.getpixel((64, 96))
            self.assertGreater(middle[0], middle[1])
            self.assertGreater(middle[1], 0)
            self.assertEqual(overview.getpixel((192, 96)), (0, 0, 255))
            left = overview.getpixel((132, 96))
            self.assertEqual(left[0], left[1])

    def test_invalid_crop_does_not_create_output(self):
        self.regions.write_text('[{"id":"bad","reference":[0,0,2,1],"candidate":[0,0,1,1]}]')
        result = run(self.command())
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_rejects_duplicate_and_unsafe_names(self):
        for name in ("../escape", "overview"):
            self.regions.write_text(json.dumps([{"id": name, "reference": [0, 0, 1, 1], "candidate": [0, 0, 1, 1]}]))
            self.assertNotEqual(run(self.command()).returncode, 0)
            self.assertFalse(self.output.exists())
        duplicate = {"id": "same", "reference": [0, 0, 1, 1], "candidate": [0, 0, 1, 1]}
        self.regions.write_text(json.dumps([duplicate, duplicate]))
        self.assertNotEqual(run(self.command()).returncode, 0)
        self.assertFalse(self.output.exists())

    def test_refuses_overwrite(self):
        self.output.mkdir()
        marker = self.output / "keep.txt"
        marker.write_text("preserve")
        self.assertNotEqual(run(self.command()).returncode, 0)
        self.assertEqual(marker.read_text(), "preserve")

    def test_missing_dependency_message(self):
        command = self.command()
        command.insert(1, "-S")
        result = run(command)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Pillow is unavailable", result.stdout)
        self.assertFalse(self.output.exists())

    def test_audit_requires_blender(self):
        result = run([sys.executable, str(SCRIPTS / "audit_blender_asset.py")])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("background Blender", result.stdout)


@unittest.skipUnless(BLENDER, "Pass --blender to run isolated real-Blender checks")
class BlenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = tempfile.TemporaryDirectory(prefix="blender-studio-audit-")
        cls.root = Path(cls.scratch.name)
        fixture = cls.root / "fixture.py"
        fixture.write_text(textwrap.dedent('''
            import bpy
            import sys
            from pathlib import Path
            root = Path(sys.argv[sys.argv.index("--") + 1])
            bpy.ops.wm.read_factory_settings(use_empty=True)
            asset = bpy.data.collections.new("Asset")
            bpy.context.scene.collection.children.link(asset)
            def move(obj, collection):
                for current in list(obj.users_collection): current.objects.unlink(obj)
                collection.objects.link(obj)
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.object
            cube.name = "ArrayCube"
            move(cube, asset)
            mat = bpy.data.materials.new("Red")
            mat.use_nodes = True
            cube.data.materials.append(mat)
            modifier = cube.modifiers.new("TwoCopies", "ARRAY")
            modifier.count = 2
            other = cube.copy()
            other.name = "MirroredCopy"
            asset.objects.link(other)
            other.location.y = 4
            other.scale.x = -1
            # An unlinked source collection contributes only through its instance.
            source = bpy.data.collections.new("InstanceSource")
            bpy.ops.mesh.primitive_cube_add()
            small = bpy.context.object
            small.name = "InstancedCube"
            move(small, source)
            instance = bpy.data.objects.new("CollectionInstance", None)
            instance.instance_type = "COLLECTION"
            instance.instance_collection = source
            instance.location.z = 4
            asset.objects.link(instance)
            bpy.ops.mesh.primitive_cube_add()
            hidden = bpy.context.object
            hidden.name = "HiddenVariant"
            hidden.hide_render = True
            move(hidden, asset)
            bpy.ops.mesh.primitive_cube_add()
            bpy.context.object.name = "UnrelatedCube"
            bpy.ops.wm.save_as_mainfile(filepath=str(root / "source.blend"))
            # A separate deliberately broken dependency/UV fixture.
            cube.data.uv_layers.remove(cube.data.uv_layers[0])
            image = bpy.data.images.new("MissingTexture", 64, 64)
            image.source = "FILE"
            image.filepath = str(root / "does-not-exist.png")
            mat.node_tree.nodes.new("ShaderNodeTexImage").image = image
            bpy.ops.wm.save_as_mainfile(filepath=str(root / "broken.blend"))
            # A small independent export gives known triangles and dimensions.
            bpy.ops.wm.read_factory_settings(use_empty=True)
            bpy.ops.mesh.primitive_cube_add(size=2)
            bpy.ops.export_scene.gltf(filepath=str(root / "export.glb"), export_format="GLB")
        '''))
        result = run(cls.base() + ["--python", str(fixture), "--", str(cls.root)])
        if result.returncode:
            cls.scratch.cleanup()
            raise AssertionError(result.stdout)

    @classmethod
    def tearDownClass(cls):
        cls.scratch.cleanup()

    @classmethod
    def base(cls):
        return [BLENDER, "--background", "--factory-startup", "--disable-autoexec", "--python-exit-code", "1"]

    def audit(self, source, name, *extra):
        output = self.root / name
        command = self.base() + ["--python", str(SCRIPTS / "audit_blender_asset.py"), "--",
                                 "--input", str(self.root / source), "--output", str(output), *extra]
        result = run(command)
        return result, json.loads(output.read_text()) if output.exists() else None

    def test_evaluates_modifiers_instances_and_preserves_source(self):
        before = (self.root / "source.blend").read_bytes()
        result, report = self.audit("source.blend", "pass.json", "--collection", "Asset", "--max-triangles", "60", "--require-uv")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["counts"]["triangles_with_instances"], 60)
        self.assertEqual(report["counts"]["mesh_instances"], 3)
        self.assertTrue(report["technical_limits_passed"])
        self.assertTrue(any(f["code"] == "negative_transform" for f in report["findings"]))
        self.assertEqual(before, (self.root / "source.blend").read_bytes())

    def test_limit_violation_is_failure(self):
        result, report = self.audit("source.blend", "limit.json", "--collection", "Asset", "--max-triangles", "59")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse(report["technical_limits_passed"])
        self.assertTrue(any(f["code"] == "triangle_limit" for f in report["findings"]))

    def test_missing_dependencies_and_uv(self):
        result, report = self.audit("broken.blend", "broken.json", "--collection", "Asset", "--require-uv")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        codes = {f["code"] for f in report["findings"]}
        self.assertIn("missing_texture", codes)
        self.assertIn("missing_uv", codes)

    def test_reimport_glb(self):
        result, report = self.audit("export.glb", "export.json", "--max-triangles", "12", "--require-uv")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["counts"]["triangles_with_instances"], 12)
        self.assertEqual(report["units"]["dimensions_meters_at_declared_scale"], [2, 2, 2])

    def test_bad_scope_and_existing_output(self):
        result, report = self.audit("source.blend", "absent.json", "--collection", "WrongCollection")
        self.assertNotEqual(result.returncode, 0)
        self.assertIsNone(report)
        existing = self.root / "existing.json"
        existing.write_text('{"keep":true}')
        result, report = self.audit("source.blend", "existing.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report, {"keep": True})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--blender")
    args, rest = parser.parse_known_args()
    BLENDER = str(Path(args.blender).resolve(strict=True)) if args.blender else None
    # unittest decorators are evaluated before CLI parsing.
    BlenderTests.__unittest_skip__ = not bool(BLENDER)
    unittest.main(argv=[sys.argv[0], *rest], verbosity=2)
