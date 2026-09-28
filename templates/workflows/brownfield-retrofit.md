# Workflow: Brownfield Codebase Retrofit

> Methodology for analyzing, interviewing, and retrofitting modern AI configurations into complex, polyglot, or non-standard existing codebases.

## Purpose
Enables an AI agent to handle repositories that defy static deterministic script detection (e.g. polyglot architectures, monorepos, conflicting libraries, legacy prompt files) through an interactive, reasoned 4-phase lifecycle.

---

## The 4-Phase Lifecycle

### Phase 1: Deep Codebase Reconnaissance
1. **Manifest & Lockfile Sweep**:
   - Locate all `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `rebar.config` files.
   - Detect package managers (`pnpm`, `uv`, `cargo`, `go`, `yarn`).
2. **Directory Topology & Layer Mapping**:
   - Identify frontend vs backend vs shared package boundaries.
   - Identify database ORMs/clients (`prisma`, `drizzle`, `sqlalchemy`, `sqlx`, `sqlc`).
3. **Legacy Prompt Audit**:
   - Scan for obsolete or conflicting `.cursorrules`, `.cursor/rules`, `.github/copilot-instructions.md`, or unstructured prompt text files.

### Phase 2: Interactive Developer Interview
When multiple libraries or ambiguous patterns are detected, DO NOT guess. Ask targeted questions:
- Clarify canonical ORM/database client if multiple appear.
- Confirm testing framework and linter targets.
- Confirm whether monorepo subprojects should have separate scoped rules or shared invariants.

### Phase 3: Single Source of Truth (SSOT) Synthesis
1. **Global Invariants (`AGENTS.md` / `CLAUDE.md`)**:
   - Keep lean (**strictly < 80 lines**).
   - Document essential build, test, lint, and run commands.
   - Outline directory topology and non-negotiable architectural boundaries.
2. **Path-Scoped Rules (`.cursor/rules/*.mdc`)**:
   - Create rules with strict `globs` so frontend rules don't pollute backend contexts.
3. **On-Demand Skills (`.agents/skills/*/SKILL.md`)**:
   - Copy or synthesize curated runbooks for deep procedures (e.g. database migrations, API testing).

### Phase 4: Doctor Verification Gate
Before completing the retrofit, execute:
```bash
./bin/ai-assist doctor
```
- Verify: Context budget (< 80 lines on global files).
- Verify: Zero dead globs in `.cursor/rules/`.
- Verify: Valid frontmatter `name` and `description` in all skills.
- Verify: Zero leaked secrets or credentials.
