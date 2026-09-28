"""Bidirectional synchronization and export-back engine for ai-assist-bootstrap.

Handles 3-way updates, extraction of working project rules back to
personal global layers (~/.ai-assist/) or directly to the central Git repo.
"""

from __future__ import annotations

import difflib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

SECRET_PATTERNS = [
    (r"sk_live_[0-9a-zA-Z]{24,}", "Live Stripe API Secret Key"),
    (r"ghp_[0-9a-zA-Z]{36,}", "GitHub Personal Access Token"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "Private Cryptographic Key"),
]


def sanitize_check(file_path: Path) -> list[str]:
    """Scans a file for potential secrets before exporting."""
    issues = []
    if not file_path.is_file():
        return issues
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    for regex, desc in SECRET_PATTERNS:
        if re.search(regex, text):
            issues.append(f"Secret pattern found: {desc}")
    return issues


def export_back(
    item_name: str,
    project_root: Path,
    templates_root: Path,
    to_git: bool = False,
    to_local_repo: Optional[str] = None,
    push: bool = False,
) -> bool:
    """Exports a project skill or rule back to personal library or Git repository."""
    # Locate item in project
    skill_candidate = project_root / ".agents" / "skills" / item_name / "SKILL.md"
    rule_candidate = project_root / ".cursor" / "rules" / f"{item_name}.mdc"

    src_file = None
    is_skill = False
    if skill_candidate.is_file():
        src_file = skill_candidate
        is_skill = True
    elif rule_candidate.is_file():
        src_file = rule_candidate
        is_skill = False
    else:
        print(
            f"Error: Could not find skill or rule '{item_name}' in project {project_root}"
        )
        return False

    # Security check
    issues = sanitize_check(src_file)
    if issues:
        print(f"\033[31mExport blocked by Security Guardrail in {src_file}:\033[0m")
        for iss in issues:
            print(f"  - {iss}")
        print("Please remove sensitive credentials before exporting.")
        return False

    # Determine destination
    if to_local_repo or to_git:
        dest_repo = Path(to_local_repo) if to_local_repo else templates_root.parent
        if not dest_repo.is_dir():
            print(f"Error: Target repo path does not exist: {dest_repo}")
            return False

        if is_skill:
            dest_dir = dest_repo / "templates" / "skills" / item_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / "SKILL.md"
        else:
            # Look for stack or common rule directory
            dest_dir = dest_repo / "templates" / "rules"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / f"{item_name}.mdc"

        shutil.copyfile(src_file, dest_file)
        print(f"\033[32m[✓] Exported {item_name} to repo template: {dest_file}\033[0m")

        if push:
            try:
                subprocess.run(
                    ["git", "add", str(dest_file)], cwd=dest_repo, check=True
                )
                msg = f"feat(skills): update {item_name} from {project_root.name}"
                subprocess.run(["git", "commit", "-m", msg], cwd=dest_repo, check=True)
                print(f"[✓] Created Git commit: {msg}")
                subprocess.run(["git", "push"], cwd=dest_repo, check=True)
                print("[✓] Pushed changes to upstream repository.")
            except Exception as e:
                print(f"Git operation failed: {e}")
                return False
        return True

    else:
        # Default destination: ~/.ai-assist/ (Personal Global Layer, or AI_ASSIST_HOME)
        custom_home = os.environ.get("AI_ASSIST_HOME")
        personal_dir = Path(custom_home) if custom_home else Path.home() / ".ai-assist"
        if is_skill:
            dest_dir = personal_dir / "skills" / item_name
            dest_file = dest_dir / "SKILL.md"
        else:
            dest_dir = personal_dir / "rules"
            dest_file = dest_dir / f"{item_name}.mdc"

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_file, dest_file)
            print(
                f"\033[32m[✓] Saved {item_name} to personal library: {dest_file}\033[0m"
            )
            return True
        except (PermissionError, OSError) as e:
            print(f"Error: Could not write to personal library at {personal_dir}: {e}")
            print(
                "Tip: Use --to-local-repo <path> or set AI_ASSIST_HOME to specify a writable location."
            )
            return False


def diff_project(project_root: Path, templates_root: Path) -> None:
    """Shows diff between current project rules/skills and base templates."""
    manifest_file = project_root / "ai-assist.json"
    if not manifest_file.is_file():
        print(f"No ai-assist.json found in {project_root}.")
        return

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    stack_id = manifest.get("stack")
    print(
        f"\nComparing project '{project_root.name}' (Stack: {stack_id}) with upstream templates:\n"
    )

    # Check skills
    skills_dir = project_root / ".agents" / "skills"
    if skills_dir.is_dir():
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                local_skill = skill_dir / "SKILL.md"
                upstream_skill = templates_root / "skills" / skill_dir.name / "SKILL.md"
                if local_skill.is_file() and upstream_skill.is_file():
                    with open(upstream_skill, "r", encoding="utf-8") as f:
                        u_lines = f.readlines()
                    with open(local_skill, "r", encoding="utf-8") as f:
                        l_lines = f.readlines()
                    diff = list(
                        difflib.unified_diff(
                            u_lines, l_lines, fromfile="upstream", tofile="local"
                        )
                    )
                    if diff:
                        print(
                            f" \033[33m[MODIFIED SKILL]\033[0m {skill_dir.name} ({len(diff)} diff lines)"
                        )
                    else:
                        print(f" \033[32m[IN SYNC]\033[0m skill: {skill_dir.name}")
                elif local_skill.is_file() and not upstream_skill.is_file():
                    print(
                        f" \033[36m[PROJECT CUSTOM SKILL]\033[0m {skill_dir.name} (not in upstream)"
                    )

    print("")
