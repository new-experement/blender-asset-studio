# Blender Asset Studio

Skills for creating and refining editable 3D assets through Blender MCP, with visual reference review, actionable repairs, geometry diagnostics, and verification of actual exports.

This repository contains **two separate adaptations**:

| Environment | Skill |
|---|---|
| Codex | [codex/blender-asset-studio](codex/blender-asset-studio) — version **1.3.0**, with instructions, templates, and diagnostic scripts |
| Claude Code | [claude-code/blender-asset-studio](claude-code/blender-asset-studio) — instructions for Claude Code |

Both versions derive style, dimensions, camera assumptions, and production constraints from the task and the relevant project. Their capabilities differ: the Codex package includes an Imagegen workflow, while the Claude version describes its own available tools. Install the adaptation for your environment.

## Installation

Install Blender and configure Blender MCP in your chosen agent first. This repository does not install Blender, the MCP server, or an image generator.

```bash
git clone https://github.com/new-experement/blender-asset-studio.git
cd blender-asset-studio
```

The following commands are for a fresh installation. If the destination already exists, preserve your current version or choose another location first.

### Codex

Copy the complete package, including its supporting directories:

```bash
mkdir -p ~/.codex/skills
cp -R codex/blender-asset-studio ~/.codex/skills/
```

If you use a custom `CODEX_HOME`, install into its `skills` directory instead. Invoke with:

```text
$blender-asset-studio Create a model from the attached references.
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R claude-code/blender-asset-studio ~/.claude/skills/
```

Invoke with:

```text
/blender-asset-studio Create a model from the attached references.
```

## Features

- Task clarification, reference intake, and visual direction selection.
- A finished representative pilot before expanding the method to the whole asset.
- Whole-object and corresponding-region comparisons against the target.
- Measurable repairs followed by inspection of fresh results.
- Visibility, support/contact, unwanted interpenetration, and working-clearance checks.
- Separate artistic acceptance, source technical checks, and export verification.

AAA quality is not guaranteed. If the repair budget is exhausted, preserve the best candidate and identify unresolved defects. Technical validity does not replace artistic acceptance.

## Testing the Codex package

The comparison tests require Pillow. Supply the path to your Blender executable:

```bash
cd codex/blender-asset-studio
python3 scripts/test_helpers.py --blender /path/to/blender
python3 scripts/test_geometry_audit.py --blender /path/to/blender
python3 scripts/test_intersections.py --blender /path/to/blender
```

Tests create temporary fixtures in separate background processes without connecting to a live Blender scene. Diagnostics do not automatically repair models. Contact does not prove freedom from penetration; sampling cannot guarantee detection of every collision, and one saved frame does not verify an entire motion. See each adaptation's instructions for details.

## License

[MIT](LICENSE).
