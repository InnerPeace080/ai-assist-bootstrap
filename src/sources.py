"""Sources and provenance tracking module for ai-assist-bootstrap.

Inspects registry.lock, audits community lineages, generates ATTRIBUTION.md,
and shows diffs between local customizations and upstream templates.
"""

from __future__ import annotations

import difflib
import json
from pathlib import Path


def list_sources(registry_lock_path: Path) -> None:
    """Prints a formatted table of all sources and tracked artifacts."""
    if not registry_lock_path.is_file():
        print(f"Error: registry.lock not found at {registry_lock_path}")
        return

    with open(registry_lock_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    artifacts = data.get("artifacts", {})
    sources = data.get("sources", {})

    print("\nTracked Community Sources:")
    print("─" * 70)
    for s_id, s_info in sources.items():
        name = s_info.get("name", s_id)
        repo = s_info.get("repo", "")
        lic = s_info.get("license", "Unknown")
        print(f" • \033[1m{name}\033[0m ({lic}) -> {repo}")

    print("\nTracked Skills & Workflows Lineage:")
    print(f"{'Artifact':<36} {'Source':<20} {'Lineage':<22}")
    print("─" * 80)
    for art_id, art_info in artifacts.items():
        source = art_info.get("source", "local")
        lineage = art_info.get("lineage", "unknown")
        print(f"{art_id:<36} {source:<20} {lineage:<22}")
    print("─" * 80 + "\n")


def diff_skill(skill_name: str, project_root: Path, templates_root: Path) -> None:
    """Compares the project's customized skill against upstream template."""
    local_file = project_root / ".agents" / "skills" / skill_name / "SKILL.md"
    upstream_file = templates_root / "skills" / skill_name / "SKILL.md"

    if not local_file.is_file():
        print(f"Local skill '{skill_name}' not found at {local_file}")
        return
    if not upstream_file.is_file():
        print(f"Upstream skill template '{skill_name}' not found at {upstream_file}")
        return

    with open(upstream_file, "r", encoding="utf-8") as f:
        upstream_lines = f.readlines()
    with open(local_file, "r", encoding="utf-8") as f:
        local_lines = f.readlines()

    diff = difflib.unified_diff(
        upstream_lines,
        local_lines,
        fromfile=f"upstream/{skill_name}/SKILL.md",
        tofile=f"local/{skill_name}/SKILL.md",
        lineterm="",
    )

    diff_list = list(diff)
    if not diff_list:
        print(
            f"\nNo differences found. Local '{skill_name}' is in sync with upstream.\n"
        )
        return

    print(f"\nDiff for skill: {skill_name} (Upstream Base vs Local Customized)")
    print("─" * 70)
    for line in diff_list:
        if line.startswith("+"):
            print(f"\033[32m{line}\033[0m")
        elif line.startswith("-"):
            print(f"\033[31m{line}\033[0m")
        elif line.startswith("@"):
            print(f"\033[36m{line}\033[0m")
        else:
            print(line)
    print("─" * 70 + "\n")


def generate_attribution(registry_lock_path: Path, output_file: Path) -> None:
    """Generates an ATTRIBUTION.md file honoring community licenses."""
    if not registry_lock_path.is_file():
        print(f"Error: registry.lock not found at {registry_lock_path}")
        return

    with open(registry_lock_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", {})
    artifacts = data.get("artifacts", {})

    lines = [
        "# Open Source Attribution",
        "",
        "This project utilizes, curates, and adapts community rules, workflows, and skills.",
        "Special thanks and credit to the upstream projects and authors:",
        "",
        "## Upstream Sources",
        "",
    ]

    for s_id, s_info in sources.items():
        name = s_info.get("name", s_id)
        repo = s_info.get("repo", "")
        lic = s_info.get("license", "Unknown")
        commit = s_info.get("commit", "main")
        lines.append(f"### {name}")
        lines.append(f"- **Repository**: [{repo}]({repo})")
        lines.append(f"- **License**: {lic}")
        lines.append(f"- **Tracked Commit**: `{commit}`")
        lines.append("")

    lines.append("## Curated Skills & Lineage")
    lines.append("")
    lines.append("| Skill / Workflow | Upstream Source | Lineage | Description |")
    lines.append("| :--- | :--- | :--- | :--- |")

    for art_id, art_info in artifacts.items():
        src = art_info.get("source", "community")
        lineage = art_info.get("lineage", "curated")
        desc = art_info.get("description", "")
        lines.append(f"| `{art_id}` | {src} | {lineage} | {desc} |")

    lines.append("")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Attribution generated successfully at {output_file}")
