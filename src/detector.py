"""Project detector for ai-assist-bootstrap.

Scans directories to automatically identify programming languages,
frameworks, package managers, and architectural topologies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class DetectionResult:
    stack_id: Optional[str] = None
    confidence: float = 0.0
    language: Optional[str] = None
    package_manager: Optional[str] = None
    detected_files: list[str] = field(default_factory=list)
    has_git: bool = False
    existing_agent_configs: list[str] = field(default_factory=list)


def detect_project(target_dir: Path | str) -> DetectionResult:
    """Inspects a project directory and detects its stack and environment."""
    root = Path(target_dir).resolve()
    result = DetectionResult()

    if not root.exists() or not root.is_dir():
        return result

    result.has_git = (root / ".git").is_dir()

    # Check existing agent configurations
    agent_indicators = [
        "AGENTS.md",
        "CLAUDE.md",
        ".cursor/rules",
        ".agents/skills",
        ".github/copilot-instructions.md",
        "ai-assist.json",
    ]
    for ind in agent_indicators:
        if (root / ind).exists():
            result.existing_agent_configs.append(ind)

    # 1. Monorepo detection
    if (
        (root / "turbo.json").is_file()
        or (root / "pnpm-workspace.yaml").is_file()
        or (root / "lerna.json").is_file()
    ):
        result.stack_id = "monorepo"
        result.confidence = 0.95
        result.language = "typescript"
        result.package_manager = (
            "pnpm" if (root / "pnpm-workspace.yaml").exists() else "npm"
        )
        if (root / "turbo.json").is_file():
            result.detected_files.append("turbo.json")
        if (root / "pnpm-workspace.yaml").is_file():
            result.detected_files.append("pnpm-workspace.yaml")
        return result

    # 2. Rust detection
    if (root / "Cargo.toml").is_file():
        result.stack_id = "rust"
        result.confidence = 0.99
        result.language = "rust"
        result.package_manager = "cargo"
        result.detected_files.append("Cargo.toml")
        return result

    # 3. Go detection
    if (root / "go.mod").is_file():
        result.stack_id = "golang"
        result.confidence = 0.99
        result.language = "go"
        result.package_manager = "go"
        result.detected_files.append("go.mod")
        return result

    # 4. Erlang detection
    if (
        (root / "rebar.config").is_file()
        or list(root.glob("src/*.erl"))
        or list(root.glob("apps/*/*.erl"))
    ):
        result.stack_id = "erlang"
        result.confidence = 0.95
        result.language = "erlang"
        result.package_manager = "rebar3"
        if (root / "rebar.config").is_file():
            result.detected_files.append("rebar.config")
        return result

    # 5. Python detection
    py_indicators = [
        "pyproject.toml",
        "requirements.txt",
        "Pipfile",
        "setup.py",
        "uv.lock",
    ]
    found_py = [f for f in py_indicators if (root / f).is_file()]
    if found_py:
        result.stack_id = "python"
        result.confidence = 0.95
        result.language = "python"
        result.detected_files.extend(found_py)
        if (root / "uv.lock").is_file():
            result.package_manager = "uv"
        elif (root / "poetry.lock").is_file():
            result.package_manager = "poetry"
        elif (root / "Pipfile").is_file():
            result.package_manager = "pipenv"
        else:
            result.package_manager = "uv"
        return result

    # 6. JavaScript / TypeScript detection
    pkg_json_path = root / "package.json"
    if pkg_json_path.is_file():
        result.detected_files.append("package.json")
        try:
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
            deps = {
                **pkg_data.get("dependencies", {}),
                **pkg_data.get("devDependencies", {}),
            }

            # Package manager check
            if (root / "pnpm-lock.yaml").is_file():
                result.package_manager = "pnpm"
            elif (root / "yarn.lock").is_file():
                result.package_manager = "yarn"
            elif (root / "bun.lockb").is_file() or (root / "bun.lock").is_file():
                result.package_manager = "bun"
            else:
                result.package_manager = "npm"

            # Check framework signatures
            if (
                "next" in deps
                or (root / "next.config.js").is_file()
                or (root / "next.config.mjs").is_file()
                or (root / "next.config.ts").is_file()
            ):
                result.stack_id = "nextjs"
                result.confidence = 0.95
                result.language = "typescript"
                return result

            if "@nestjs/core" in deps or (root / "nest-cli.json").is_file():
                result.stack_id = "nestjs"
                result.confidence = 0.95
                result.language = "typescript"
                return result

            if (
                "expo" in deps
                or "react-native" in deps
                or (root / "app.json").is_file()
            ):
                result.stack_id = "react-native"
                result.confidence = 0.95
                result.language = "typescript"
                return result

            if "react" in deps:
                result.stack_id = "reactjs"
                result.confidence = 0.90
                result.language = "typescript"
                return result

        except Exception:
            pass

    # 7. Shell Script detection
    sh_files = (
        list(root.glob("*.sh")) + list(root.glob("bin/*")) + list(root.glob("lib/*.sh"))
    )
    if sh_files:
        result.stack_id = "shell"
        result.confidence = 0.85
        result.language = "shell"
        result.package_manager = "bash"
        result.detected_files.extend([str(f.relative_to(root)) for f in sh_files[:3]])
        return result

    return result
