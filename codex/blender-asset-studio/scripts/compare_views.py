#!/usr/bin/env python3
"""Create evidence sheets; never change source images or judge artistic quality."""
import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path


def box_pixels(box, size):
    if (not isinstance(box, list) or len(box) != 4
            or any(isinstance(v, bool) or not isinstance(v, (int, float))
                   or not math.isfinite(v) for v in box)):
        raise ValueError("Each crop must contain four finite normalized numbers")
    x0, y0, x1, y1 = box
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise ValueError("Crop must satisfy 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1")
    w, h = size
    return [math.floor(x0 * w), math.floor(y0 * h),
            math.ceil(x1 * w), math.ceil(y1 * h)]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--regions", type=Path)
    parser.add_argument("--panel-size", type=int, default=512)
    args = parser.parse_args()
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError:
        parser.exit(1, "Pillow is unavailable. Use an existing image viewer or an authorized dependency setup.\n")
    if not 128 <= args.panel_size <= 2048:
        parser.error("--panel-size must be between 128 and 2048")
    if args.output.exists():
        parser.error("Output directory already exists; choose a new revision directory")

    images = []
    inputs = []
    for role in ("reference", "candidate"):
        path = getattr(args, role).resolve(strict=True)
        with Image.open(path) as original:
            # EXIF orientation is applied consistently before normalized cropping.
            oriented = ImageOps.exif_transpose(original).convert("RGBA")
            images.append(oriented)
            inputs.append({"role": role, "path": str(path), "sha256": sha256(path),
                           "oriented_size": list(oriented.size)})

    regions = json.loads(args.regions.read_text()) if args.regions else []
    if not isinstance(regions, list) or len(regions) > 24:
        raise ValueError("Regions must be a list of at most 24 semantic regions")
    prepared = []
    ids = set()
    for region in regions:
        if not isinstance(region, dict) or not isinstance(region.get("id"), str):
            raise ValueError("Every region needs a string id and reference/candidate boxes")
        name = region["id"]
        if not re.fullmatch(r"[\w-]{1,60}", name) or name in ids or name == "overview":
            raise ValueError("Region IDs must be unique safe names (1–60 letters, digits, underscores or hyphens)")
        ids.add(name)
        boxes = [box_pixels(region[role], images[i].size)
                 for i, role in enumerate(("reference", "candidate"))]
        prepared.append((name, boxes))

    panel = args.panel_size
    label_height = 32
    def composite(im):
        result = Image.new("RGB", (panel, panel), "#c9c9c9")
        draw = ImageDraw.Draw(result)
        for y in range(0, panel, 16):
            for x in range(0, panel, 16):
                if (x // 16 + y // 16) % 2:
                    draw.rectangle((x, y, x + 15, y + 15), fill="#eeeeee")
        fitted = ImageOps.contain(im, (panel, panel), Image.Resampling.LANCZOS)
        result.paste(fitted, ((panel - fitted.width) // 2, (panel - fitted.height) // 2), fitted)
        return result

    def pair(name, crops):
        result = Image.new("RGB", (2 * panel, panel + label_height), "#202020")
        draw = ImageDraw.Draw(result)
        for i, crop in enumerate(crops):
            draw.text((i * panel + 8, 8), f'{name} | {inputs[i]["role"]}', fill="white")
            result.paste(composite(crop), (i * panel, label_height))
        return result

    # All input validation precedes creating any output.
    args.output.mkdir(parents=True, exist_ok=False)
    rows = [pair("overview", images)]
    rows[0].save(args.output / "overview.png")
    evidence = []
    for name, boxes in prepared:
        row = pair(name, [im.crop(box) for im, box in zip(images, boxes)])
        row.save(args.output / f"{name}.png")
        rows.append(row)
        evidence.append({"id": name, "pixel_boxes": dict(zip(("reference", "candidate"), boxes)),
                         "image": f"{name}.png"})
    sheet = Image.new("RGB", (rows[0].width, sum(row.height for row in rows)), "#202020")
    for i, row in enumerate(rows):
        sheet.paste(row, (0, i * row.height))
    sheet.save(args.output / "contact-sheet.png")
    metadata = {"schema_version": 1, "inputs": inputs, "regions": regions,
                "evidence": evidence, "panel_size": panel,
                "note": "Analysis only. Crops are independently fitted without aspect distortion; panel scale is not a measurement.",
                "artistic_acceptance": "not-assessed"}
    (args.output / "provenance.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output.resolve()), "paired_regions": len(prepared),
                      "artistic_acceptance": "not-assessed"}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError) as exc:
        print(f"Comparison failed: {exc}", file=sys.stderr)
        sys.exit(1)
