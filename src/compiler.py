"""Template compiler and code generator for ai-assist-bootstrap.

Compiles unified Single Source of Truth (SSOT) templates into target
agent formats (AGENTS.md, CLAUDE.md, .cursor/rules, .agents/skills, MCP).
"""

from __future__ import annotations

import datetime
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DIRECTORY_TREES = {
    "nextjs": """app/
├── layout.tsx             # Root layout with metadata & fonts
├── page.tsx               # Home landing route
├── actions/               # Server Actions (mutations with Zod)
└── (routes)/              # Scoped route groups
components/
├── ui/                    # Reusable shadcn/radix primitives
└── shared/                # Composed domain components
lib/                       # Utilities, auth, and database clients""",
    "nestjs": """src/
├── main.ts                # Bootstrap entrypoint & global validation pipes
├── app.module.ts          # Root module registering feature modules
└── <feature>/
    ├── <feature>.controller.ts
    ├── <feature>.service.ts
    ├── <feature>.module.ts
    └── dto/               # Class-validator request/response DTOs""",
    "react-native": """app/
├── _layout.tsx            # Global providers & root stack
├── (auth)/                # Authentication screens
├── (tabs)/                # Bottom navigation tabs
└── (modals)/              # Sliding presentation sheets
components/                # NativeWind UI components
hooks/                     # Custom navigation and state hooks""",
    "monorepo": """apps/
├── web/                   # Next.js / Vite web application
└── docs/                  # Documentation site
packages/
├── ui/                    # Shared design system components
├── typescript-config/     # Canonical tsconfig bases
└── eslint-config/         # Shared linter definitions""",
    "reactjs": """src/
├── main.tsx               # DOM root & React query provider
├── App.tsx                # Client route configuration
├── features/              # Vertical feature slices (components, hooks)
├── components/ui/         # Atomic UI primitives
└── lib/                   # API client, query key factories""",
    "golang": """cmd/
└── server/
    └── main.go            # Dependency injection, flags, graceful shutdown
internal/                  # Private compiler-protected packages
├── domain/                # Entity models & repository interfaces
├── service/               # Core business logic
└── repository/            # Database drivers & external clients""",
    "python": """src/<app>/
├── main.py                # FastAPI app initialization & middleware
├── api/                   # APIRouter route handlers
├── models/                # SQLAlchemy 2.0 ORM models
├── schemas/               # Pydantic v2 validation schemas
└── services/              # Business operations
tests/                     # pytest-asyncio test suites""",
    "rust": """src/
├── main.rs                # Axum listener, router binding, state injection
├── error.rs               # thiserror AppError enum & IntoResponse
├── state.rs               # AppState with connection pools
├── routes/                # HTTP endpoint handlers
└── models/                # Domain types & sqlx queries""",
    "erlang": """src/
├── <app>_app.erl          # OTP application behaviour callback
├── <app>_sup.erl          # Root supervisor with map child specs
└── <worker>.erl           # gen_server worker process
test/                      # EUnit & Common Test suites""",
    "shell": """bin/
└── <tool>                 # Executable entrypoint (set -euo pipefail)
lib/
├── utils.sh               # Logging, colors, helper functions
└── commands.sh            # Modular subcommand implementations
test/                      # bats-core hermetic test suites""",
}


MCP_DEFINITIONS: dict[str, dict[str, Any]] = {
    "postgres": {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-postgres",
            "postgresql://user:pass@localhost:5432/db",
        ],
    },
    "playwright": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-playwright"],
    },
    "context7": {
        "command": "npx",
        "args": ["-y", "@context7/mcp-server"],
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"},
    },
}


@dataclass
class CompilerConfig:
    project_dir: Path
    project_name: str
    stack_id: str
    templates_root: Path
    package_manager: str | None = None
    custom_skills: list[str] = field(default_factory=list)
    targets: list[str] = field(
        default_factory=lambda: ["claude", "cursor", "antigravity", "copilot"]
    )


def get_template_root(start_dir: Path | None = None) -> Path:
    """Finds the templates directory either locally or relative to this script."""
    current = Path(__file__).resolve().parent.parent / "templates"
    if current.is_dir():
        return current
    if start_dir:
        candidate = Path(start_dir) / "templates"
        if candidate.is_dir():
            return candidate
    return current


def compile_project(config: CompilerConfig) -> list[str]:
    """Compiles all AI configuration files into the target project directory."""
    generated_files: list[str] = []
    root = config.project_dir
    root.mkdir(parents=True, exist_ok=True)

    stack_dir = config.templates_root / "stacks" / config.stack_id
    if not stack_dir.is_dir():
        raise ValueError(
            f"Unknown stack profile '{config.stack_id}'. Available in templates/stacks/"
        )

    with open(stack_dir / "stack.json", "r", encoding="utf-8") as f:
        stack_info = json.load(f)

    pkg_manager = config.package_manager or stack_info.get("packageManager", "npm")
    commands = stack_info.get("commands", {})

    rules_list = stack_info.get("rules", [])
    stack_rules_md = "\n".join(f"- {r}" for r in rules_list)
    tree_md = DIRECTORY_TREES.get(config.stack_id, "src/\n└── main")

    replacements = {
        "{{PROJECT_NAME}}": config.project_name,
        "{{GENERATED_DATE}}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{{STACK_PROFILE}}": config.stack_id,
        "{{STACK_TITLE}}": stack_info.get("title", config.stack_id),
        "{{STACK_SUMMARY}}": stack_info.get("summary", ""),
        "{{PACKAGE_MANAGER}}": pkg_manager,
        "{{INSTALL_CMD}}": commands.get("install", ""),
        "{{DEV_CMD}}": commands.get("dev", ""),
        "{{TEST_CMD}}": commands.get("test", ""),
        "{{LINT_CMD}}": commands.get("lint", ""),
        "{{TYPECHECK_CMD}}": commands.get("typecheck", ""),
        "{{BUILD_CMD}}": commands.get("build", ""),
        "{{TEST_FRAMEWORK}}": stack_info.get("testFramework", "testing"),
        "{{DIRECTORY_TREE}}": tree_md,
        "{{STACK_RULES}}": stack_rules_md,
    }

    # 1. Compile AGENTS.md
    common_dir = config.templates_root / "common"
    with open(common_dir / "AGENTS.md.tpl", "r", encoding="utf-8") as f:
        agents_content = f.read()
    for k, v in replacements.items():
        agents_content = agents_content.replace(k, str(v))
    target_agents = root / "AGENTS.md"
    with open(target_agents, "w", encoding="utf-8") as f:
        f.write(agents_content)
    generated_files.append("AGENTS.md")

    # 2. Compile CLAUDE.md
    with open(common_dir / "CLAUDE.md.tpl", "r", encoding="utf-8") as f:
        claude_content = f.read()
    for k, v in replacements.items():
        claude_content = claude_content.replace(k, str(v))
    target_claude = root / "CLAUDE.md"
    with open(target_claude, "w", encoding="utf-8") as f:
        f.write(claude_content)
    generated_files.append("CLAUDE.md")

    # Copy Custom Slash Commands (.claude/commands/)
    if "claude" in config.targets:
        commands_src = config.templates_root / "commands"
        if commands_src.is_dir():
            claude_commands_dir = root / ".claude" / "commands"
            claude_commands_dir.mkdir(parents=True, exist_ok=True)
            for cmd_file in sorted(commands_src.glob("*.md")):
                shutil.copyfile(cmd_file, claude_commands_dir / cmd_file.name)
                generated_files.append(f".claude/commands/{cmd_file.name}")

    # 3. Compile GitHub Copilot instructions
    if "copilot" in config.targets:
        github_dir = root / ".github"
        github_dir.mkdir(exist_ok=True)
        with open(
            common_dir / "copilot-instructions.md.tpl", "r", encoding="utf-8"
        ) as f:
            copilot_content = f.read()
        for k, v in replacements.items():
            copilot_content = copilot_content.replace(k, str(v))
        target_copilot = github_dir / "copilot-instructions.md"
        with open(target_copilot, "w", encoding="utf-8") as f:
            f.write(copilot_content)
        generated_files.append(".github/copilot-instructions.md")

    # 4. Copy Cursor Rules (.cursor/rules/)
    if "cursor" in config.targets:
        cursor_rules_dir = root / ".cursor" / "rules"
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        src_rules = stack_dir / "cursor-rules"
        if src_rules.is_dir():
            for rule_file in src_rules.glob("*.mdc"):
                dest_file = cursor_rules_dir / rule_file.name
                shutil.copyfile(rule_file, dest_file)
                generated_files.append(f".cursor/rules/{rule_file.name}")

    # 5. Copy Curated Skills (.agents/skills/)
    skills_to_install = list(
        set(stack_info.get("defaultSkills", []) + config.custom_skills)
    )
    skills_root = root / ".agents" / "skills"
    for skill_name in skills_to_install:
        src_skill_file = config.templates_root / "skills" / skill_name / "SKILL.md"
        if src_skill_file.is_file():
            target_skill_dir = skills_root / skill_name
            target_skill_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_skill_file, target_skill_dir / "SKILL.md")
            generated_files.append(f".agents/skills/{skill_name}/SKILL.md")

    # 6. Generate MCP Config (.mcp/mcp_config.json)
    mcp_needed = stack_info.get("mcp", ["context7", "github"])
    mcp_servers = {}
    for server_id in mcp_needed:
        if server_id in MCP_DEFINITIONS:
            mcp_servers[server_id] = MCP_DEFINITIONS[server_id]
    mcp_dir = root / ".mcp"
    mcp_dir.mkdir(exist_ok=True)
    mcp_config = {"mcpServers": mcp_servers}
    with open(mcp_dir / "mcp_config.json", "w", encoding="utf-8") as f:
        json.dump(mcp_config, f, indent=2)
    generated_files.append(".mcp/mcp_config.json")

    # 7. Generate ai-assist.json manifest
    manifest = {
        "$schema": "https://raw.githubusercontent.com/innerpeace080/ai-assist-bootstrap/main/schema/ai-assist.schema.json",
        "name": config.project_name,
        "templateVersion": "1.0.0",
        "stack": config.stack_id,
        "packageManager": pkg_manager,
        "generatedAt": datetime.datetime.now().isoformat(),
        "skills": skills_to_install,
        "upstream": {
            "gitRemote": "https://github.com/innerpeace080/ai-assist-bootstrap.git",
            "localRepoPath": str(config.templates_root.parent),
            "defaultBranch": "main",
        },
    }
    with open(root / "ai-assist.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    generated_files.append("ai-assist.json")

    return generated_files
