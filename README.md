# ai-assist-bootstrap

> **Bootstrap modern software projects across 10 technology stacks with production-ready AI skills, scoped rules, workflows, quality check gates, and MCP configurations.**

---

## 🚀 Overview

`ai-assist-bootstrap` bridges the gap between software development and multi-agent AI coding assistants. Instead of manually configuring and maintaining ad-hoc prompt files across different AI tools, `ai-assist-bootstrap` provides an automated, modular, context-budgeted, and verifiable configuration engine for:

* **Antigravity / Gemini CLI** (`AGENTS.md`, `.agents/skills/*/SKILL.md`)
* **Claude Code** (`CLAUDE.md`, `.claude/` skills, commands, PreToolUse hooks)
* **Cursor** (`.cursor/rules/*.mdc` with scoped glob matching)
* **GitHub Copilot** (`.github/copilot-instructions.md`)
* **Windsurf & Devin** (Universal `AGENTS.md`)

---

## ⚡ Key Architectural Highlights

1. **Context Budgeting & Progressive Disclosure**: Prevents prompt dilution by enforcing lean global rules (< 80 lines) in `AGENTS.md` / `CLAUDE.md` and loading deep procedures on-demand via `.agents/skills/<name>/SKILL.md`.
2. **Single Source of Truth (SSOT)**: Canonical stack definitions compile cleanly into all agent target formats.
3. **10 Production-Ready Stacks**:
   - **Next.js 15+**: App Router, Server Actions, React 19 RSC boundaries, Zod validation.
   - **NestJS**: TypeScript modular architecture, class-validator DTOs, Prisma / TypeORM.
   - **React Native & Expo**: Expo Router v3/v4, typed routes, NativeWind, SafeArea.
   - **Monorepo**: Turborepo + pnpm workspaces, strict package boundaries.
   - **React.js SPA**: Vite, TanStack Query v5 (query key factories, no useEffect fetching), Zustand.
   - **Golang**: Go 1.23+, `cmd/` + `internal/`, explicit `%w` wrapping, structured concurrency with `context.Context`.
   - **Python**: Python 3.12+, FastAPI, Pydantic v2, `uv` package manager, `ruff`, async SQLAlchemy 2.0.
   - **Rust**: Rust 1.83+, Axum 0.7+, Tokio, `thiserror` domain errors, zero `.unwrap()` in production.
   - **Erlang**: OTP 26+, `rebar3`, supervision trees, map-based child specs, GenServer callback separation.
   - **Shell Scripting**: Bash 5+ / POSIX, `set -euo pipefail`, modular `bin/` + `lib/`, `getopts`, `shellcheck`, `bats-core`.
4. **Automated Diagnostic Suite (`doctor`)**: Audits context budgets, catches dead globs, validates frontmatter schemas, scans for leaked credentials, and checks provenance.
5. **Bidirectional Sync & Provenance Tracking**:
   - 3-Way non-destructive merge (`copier`/`cruft` model) when updating templates.
   - Extract project-refined rules back to local personal libraries (`~/.ai-assist/`) or push directly to the central Git repo (`export-back --to-git`).
   - Upstream origin, commit hash, and license tracking via `templates/registry.lock` and YAML frontmatter.

---

## 💻 CLI Quickstart

The CLI runs natively on Linux, macOS, and WSL without requiring external package installations:

```bash
# Display help and commands
./bin/ai-assist --help

# List all 10 supported stacks
./bin/ai-assist list-stacks

# List curated skills
./bin/ai-assist list-skills
```

### 1. Create a New Project (Greenfield)
```bash
./bin/ai-assist create my-app --stack golang
# Or: --stack python, nextjs, nestjs, rust, shell, etc.
```

### 2. Retrofit an Existing Codebase (Brownfield)
```bash
cd /path/to/my-existing-project
/path/to/ai-assist-bootstrap/bin/ai-assist add
# Auto-detects stack from project signatures and injects AI configurations!
```

### 3. Run Rule & Context Diagnostics (`doctor`)
```bash
./bin/ai-assist doctor
# Audits context budget (<80 lines), dead globs, schema validation, and secrets
```

### 4. Extract Project Rules Back Upstream (`export-back`)
```bash
# Save to local personal library (~/.ai-assist/)
./bin/ai-assist export-back my-custom-skill

# Export directly to central template repository
./bin/ai-assist export-back my-custom-skill --to-local-repo /media/Data/Codes/shell/ai-assist-bootstrap
```

### 5. Inspect Upstream Provenance & Generate Attribution
```bash
# List tracked sources and licenses
./bin/ai-assist sources list

# Generate Open Source ATTRIBUTION.md
./bin/ai-assist sources credit
```

---

## 📖 Master Documentation Index (`docs/`)

| Document                                                                                         | Focus                                                                     |
| :----------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| **[01. Research & Benchmarks](./docs/01-research-and-benchmarks.md)**                            | Analysis of 14 leading AI agent configuration repos & frameworks          |
| **[02. Architecture & Design](./docs/02-architecture-and-design.md)**                            | Progressive disclosure, SSOT compiler, and `ai-assist.json` specification |
| **[03. Stack Profiles](./docs/03-stack-profiles.md)**                                            | Rules, invariants, and commands across all 10 supported stacks            |
| **[04. Workflows & Skills Catalog](./docs/04-workflows-and-skills-catalog.md)**                  | 9 Core agentic workflows and catalog of 27 curated skills                 |
| **[05. Roadmap & Implementation](./docs/05-roadmap-and-implementation.md)**                      | Phased milestones, execution strategy, and repository layout              |
| **[06. Workflow Check Gates & Hooks](./docs/06-workflow-check-gates-and-hooks.md)**              | 4-Tier quality gate defense (PreToolUse, Lefthook, Reviewer agents)       |
| **[07. Bidirectional Sync & Overrides](./docs/07-bidirectional-sync-and-personal-overrides.md)** | 3-way merge model and `export-back` upstream extraction                   |
| **[08. Provenance & Source Lineage](./docs/08-provenance-tracking-and-source-lineage.md)**       | In-file frontmatter metadata and central `registry.lock` specification    |
| **[09. MCP Servers & Integrations](./docs/09-mcp-servers-and-tool-integrations.md)**             | Contextual MCP servers (Postgres, Playwright, Context7, GitHub)           |
| **[10. Rule Linting & Diagnostics](./docs/10-rule-linting-and-diagnostics.md)**                  | The `doctor` audit suite, dead glob detector, and budget auditor          |
| **[11. Agent Fleet Orchestration](./docs/11-agent-fleet-and-parallel-orchestration.md)**         | Concurrent multi-agent fleets, Git worktree isolation, and rebase merge   |

---

## 🧪 Testing

Run the automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 License

MIT
