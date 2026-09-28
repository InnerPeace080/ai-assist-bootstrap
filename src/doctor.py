"""Diagnostic and health inspection engine for ai-assist-bootstrap.

Performs context budgeting audits, frontmatter schema validation,
dead glob detection, secret scanning, and provenance verification.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class DiagnosticIssue:
    category: str
    severity: str  # "ERROR", "WARNING", "INFO"
    file_path: str
    message: str
    recommendation: Optional[str] = None


@dataclass
class DiagnosticReport:
    project_root: str
    issues: list[DiagnosticIssue] = field(default_factory=list)
    passed_checks: list[str] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.severity == "ERROR" for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "ERROR")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "WARNING")


SECRET_PATTERNS = [
    (r"sk_live_[0-9a-zA-Z]{24,}", "Live Stripe API Secret Key"),
    (r"ghp_[0-9a-zA-Z]{36,}", "GitHub Personal Access Token"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "Private Cryptographic Key"),
]


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """Extracts simple key-value YAML frontmatter from markdown content."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content

    data: dict[str, str] = {}
    end_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip("\"'")

    body = "\n".join(lines[end_idx + 1 :]) if end_idx != -1 else content
    return data, body


def run_doctor(
    target_dir: Path | str, registry_lock_path: Optional[Path] = None
) -> DiagnosticReport:
    """Runs the full diagnostic inspection suite against a project directory."""
    root = Path(target_dir).resolve()
    report = DiagnosticReport(project_root=str(root))

    # 1. Context Budget Check (AGENTS.md & CLAUDE.md < 80 lines)
    for global_file in ["AGENTS.md", "CLAUDE.md"]:
        p = root / global_file
        if p.is_file():
            with open(p, "r", encoding="utf-8") as f:
                lines = f.readlines()
            count = len(lines)
            if count > 80:
                report.issues.append(
                    DiagnosticIssue(
                        category="Context Budget",
                        severity="WARNING",
                        file_path=global_file,
                        message=f"{global_file} is {count} lines, exceeding the 80-line budget",
                        recommendation="Move detailed step-by-step procedures into on-demand .agents/skills/",
                    )
                )
            else:
                report.passed_checks.append(
                    f"Context Budget: {global_file} ({count} lines <= 80)"
                )

    # 2. Skill Frontmatter Validation (.agents/skills/*/SKILL.md)
    skills_dir = root / ".agents" / "skills"
    if skills_dir.is_dir():
        valid_skills = 0
        total_skills = 0
        for skill_file in skills_dir.glob("*/SKILL.md"):
            total_skills += 1
            rel_path = str(skill_file.relative_to(root))
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
            frontmatter, _ = parse_frontmatter(content)
            if "name" not in frontmatter or not frontmatter["name"]:
                report.issues.append(
                    DiagnosticIssue(
                        category="Frontmatter",
                        severity="ERROR",
                        file_path=rel_path,
                        message="Missing or empty 'name' in YAML frontmatter",
                        recommendation="Add 'name: <skill-name>' to frontmatter",
                    )
                )
            elif "description" not in frontmatter or not frontmatter["description"]:
                report.issues.append(
                    DiagnosticIssue(
                        category="Frontmatter",
                        severity="ERROR",
                        file_path=rel_path,
                        message="Missing or empty 'description' in YAML frontmatter",
                        recommendation="Add 'description: <1-2 sentences>' so agents know when to load it",
                    )
                )
            else:
                valid_skills += 1

        if total_skills > 0 and valid_skills == total_skills:
            report.passed_checks.append(
                f"Frontmatter: All {valid_skills} skills have valid name and description"
            )

    # 3. Cursor Rules & Dead Globs Check (.cursor/rules/*.mdc)
    cursor_dir = root / ".cursor" / "rules"
    if cursor_dir.is_dir():
        for rule_file in cursor_dir.glob("*.mdc"):
            rel_path = str(rule_file.relative_to(root))
            with open(rule_file, "r", encoding="utf-8") as f:
                content = f.read()
            frontmatter, _ = parse_frontmatter(content)
            if "description" not in frontmatter:
                report.issues.append(
                    DiagnosticIssue(
                        category="Frontmatter",
                        severity="ERROR",
                        file_path=rel_path,
                        message="Missing 'description' in Cursor rule frontmatter",
                    )
                )
            # Globs check
            globs_val = frontmatter.get("globs", "")
            if globs_val:
                patterns = [
                    g.strip().strip("\"'[]") for g in globs_val.split(",") if g.strip()
                ]
                for pattern in patterns:
                    clean_pattern = pattern.strip("*").lstrip("/")
                    # Check if any file matches
                    matches = (
                        list(root.glob(pattern))
                        if "*" in pattern
                        else (
                            [root / clean_pattern]
                            if (root / clean_pattern).exists()
                            else []
                        )
                    )
                    if not matches and not list(root.glob(f"**/{clean_pattern}*")):
                        report.issues.append(
                            DiagnosticIssue(
                                category="Dead Glob",
                                severity="WARNING",
                                file_path=rel_path,
                                message=f"Glob pattern '{pattern}' matched 0 files in repository",
                                recommendation="Update the glob pattern or delete obsolete rule file",
                            )
                        )

    # 4. Secret Scanner
    scan_extensions = [".md", ".mdc", ".json", ".yaml", ".yml", ".toml"]
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in scan_extensions:
            if ".git" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                for regex, desc in SECRET_PATTERNS:
                    if re.search(regex, text):
                        report.issues.append(
                            DiagnosticIssue(
                                category="Security",
                                severity="ERROR",
                                file_path=str(path.relative_to(root)),
                                message=f"Potential hardcoded secret detected: {desc}",
                                recommendation="Move secret to environment variables and add to .env / .gitignore",
                            )
                        )
            except Exception:
                pass

    if not any(i.category == "Security" for i in report.issues):
        report.passed_checks.append(
            "Security: Zero hardcoded secrets found in scanned AI configurations"
        )

    # 5. Provenance Audit
    if registry_lock_path and registry_lock_path.is_file():
        try:
            with open(registry_lock_path, "r", encoding="utf-8") as f:
                lock_data = json.load(f)
            registered_artifacts = lock_data.get("artifacts", {})
            if skills_dir.is_dir():
                for skill_file in skills_dir.glob("*/SKILL.md"):
                    skill_id = f"skills/{skill_file.parent.name}"
                    if skill_id not in registered_artifacts:
                        report.issues.append(
                            DiagnosticIssue(
                                category="Provenance",
                                severity="INFO",
                                file_path=str(skill_file.relative_to(root)),
                                message=f"Skill '{skill_id}' is not recorded in registry.lock",
                                recommendation="Run 'ai-assist-bootstrap sources sync' to track provenance",
                            )
                        )
            report.passed_checks.append(
                "Provenance: Checked against registry.lock Bill of Materials"
            )
        except Exception:
            pass

    return report


def print_doctor_report(report: DiagnosticReport) -> None:
    """Formats and prints the report to stdout."""
    print(f"\nAI Assist Doctor - Auditing: {report.project_root}\n")

    for pass_msg in report.passed_checks:
        print(f"  \033[32m[✓]\033[0m {pass_msg}")

    for issue in report.issues:
        color = (
            "\033[31m"
            if issue.severity == "ERROR"
            else "\033[33m"
            if issue.severity == "WARNING"
            else "\033[36m"
        )
        symbol = (
            "[✗]"
            if issue.severity == "ERROR"
            else "[!]"
            if issue.severity == "WARNING"
            else "[i]"
        )
        print(
            f"\n  {color}{symbol} {issue.category} ({issue.severity}): {issue.file_path}\033[0m"
        )
        print(f"      {issue.message}")
        if issue.recommendation:
            print(f"      \033[90m↳ Recommendation: {issue.recommendation}\033[0m")

    print("\n" + "─" * 60)
    print(
        f"Summary: {report.error_count} Error(s), {report.warning_count} Warning(s)\n"
    )
