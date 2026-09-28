# 02. Architecture & System Design

This document details the architectural blueprint of **`ai-assist-bootstrap`**, explaining how it bridges project code generation with multi-agent AI configurations while strictly respecting LLM context limits.

---

## 1. Core Architecture Diagram

```
                                ai-assist-bootstrap
                                         │
        ┌────────────────────────────────┴────────────────────────────────┐
        ▼                                                                 ▼
[ CLI & Configuration Layer ]                                   [ Project Analyzer ]
  * Interactive CLI Wizard (Clack/Inquirer)                       * Framework Detector
  * Flag-driven CLI (`--stack`, `--agents`)                       * Monorepo Layout Inspector
  * Manifest reader (`ai-bootstrap.config.json`)                  * Existing AI Config Audit
        │                                                                 │
        └────────────────────────────────┬────────────────────────────────┘
                                         ▼
                             [ Orchestration Engine ]
                                         │
            ┌────────────────────────────┴────────────────────────────┐
            ▼                                                         ▼
  [ Project Scaffolder ]                                    [ AI Config Compiler ]
  * Next.js / NestJS / Expo / Turbo                          * Rule Synthesizer
  * Package manager setup (pnpm, npm, bun)                   * Skill Extractor (Progressive)
  * Dependency & tooling install                             * Workflow Injector (TDD, Plan)
            │                                                         │
            └────────────────────────────┬────────────────────────────┘
                                         ▼
                             [ Generated Codebase ]
                                         │
      ┌──────────────────────┬───────────┴───────────┬──────────────────────┐
      ▼                      ▼                       ▼                      ▼
  AGENTS.md           .cursor/rules/             .claude/             .agents/skills/
(Universal Root)     (Scoped .mdc rules)      (CLAUDE.md, cmds)      (SKILL.md standard)
```

---

## 2. Core Architectural Pillars

### Pillar 1: Progressive Disclosure (Context Budgeting)

One of the most frequent reasons AI agents perform poorly in large codebases is **context window exhaustion**. When 5,000 to 10,000 tokens of static rules are injected into every prompt turn, the model:
- Has less headroom for actual code and file search results.
- Suffers from instruction degradation (ignoring critical rules).
- Becomes slower and significantly more expensive per query.

`ai-assist-bootstrap` enforces a 3-tier hierarchy:

```
+-------------------------------------------------------------------------+
| Level 1: Global Rules (Always Loaded)                                   |
| Length: 40 - 75 lines max.                                              |
| Contains: Core invariants, git format, safety bounds, package manager.  |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
| Level 2: Scoped Path Rules (Glob-Triggered)                             |
| Length: 20 - 50 lines per rule.                                         |
| Active only when the agent views/edits matching files                   |
| Example: `.cursor/rules/server-actions.mdc` -> `app/**/actions/**/*.ts` |
+-------------------------------------------------------------------------+
                                    │
                                    ▼
+-------------------------------------------------------------------------+
| Level 3: Progressive Skills (On-Demand Runbooks)                         |
| Length: 50 - 250 lines per skill.                                       |
| Injected into context ONLY when explicitly activated by name            |
| Example: `skills/db-migrate/SKILL.md` (loaded only when doing migrations)|
+-------------------------------------------------------------------------+
```

---

### Pillar 2: Single Source of Truth (SSOT) Multi-Agent Compiler

Teams frequently switch between or combine multiple AI coding tools:
- **Cursor** for inline completions, diff editing, and agentic Composer.
- **Claude Code** or **Antigravity CLI** for terminal-based planning, refactoring, and multi-file tasks.
- **GitHub Copilot** in IDEs and CI environments.
- **Windsurf** and **Devin** in agentic pipelines.

Instead of writing separate, drifting configuration files, `ai-assist-bootstrap` maintains modular templates and compiles them into tool-specific targets:

| Target File                       | Format & Standard                                         | Supported By                                            | Purpose                                                        |
| :-------------------------------- | :-------------------------------------------------------- | :------------------------------------------------------ | :------------------------------------------------------------- |
| `AGENTS.md`                       | Universal Markdown                                        | Antigravity, Cursor, Copilot, Devin, Gemini CLI, Claude | Canonical root project instructions and directory guide        |
| `CLAUDE.md`                       | Anthropic Markdown                                        | Claude Code                                             | Terminal agent rules, test/build commands, guidelines          |
| `.cursor/rules/*.mdc`             | Cursor MDC with YAML frontmatter (`globs`, `alwaysApply`) | Cursor                                                  | Targeted, path-scoped rules for frontend, backend, styles      |
| `.agents/skills/*/SKILL.md`       | Progressive Disclosure Markdown with frontmatter          | Antigravity, Claude Code, Agent SDKs                    | On-demand complex runbooks (TDD, migration, deployment)        |
| `.github/copilot-instructions.md` | Markdown                                                  | GitHub Copilot                                          | Repository-level Copilot chat and completion instructions      |
| `mcp_config.json`                 | JSON standard                                             | Claude Code, Antigravity, Cursor (MCP clients)          | Local and external tool servers (filesystem, Postgres, GitHub) |

---

### Pillar 3: Dual-Mode Operation (`create` vs `retrofit`)

`ai-assist-bootstrap` operates in two modes:

#### 1. Greenfield Creation (`create`)
* The user specifies the stack (e.g. Next.js App Router, NestJS API, React Native Expo, or Turborepo Monorepo).
* Scaffolds the official project structure using recommended modern tooling (`pnpm`, TypeScript, ESLint, Prettier).
* Injects the tailored AI configuration pack directly into the new project.
* Result: A ready-to-run repository equipped with code and AI configurations from commit zero.

#### 2. Brownfield Retrofit (`add` / `init`)
* Runs inside an **existing** codebase.
* **Deterministic Heuristic Pass**:
  - Inspects `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, and dependency trees via `src/detector.py`.
  - Automatically identifies framework, language, package manager, and test suites.
  - Injects standard AI configurations without modifying application source code.
* **Complex Polyglot & Edge-Case Architecture ("Brain vs. Hands")**:
  - Complex real-world codebases (e.g., hybrid Next.js + FastAPI microservices, custom internal tooling, conflicting legacy prompt files) often defy static heuristic scripts.
  - **The "Brain" (On-Demand Skill & Workflow)**: Rather than polluting global context with permanent setup instructions, an on-demand Skill (`retrofit-assistant`) and Workflow (`brownfield-retrofit`) guide the AI agent through a 4-phase reasoning cycle (Reconnaissance $\to$ Developer Interview $\to$ SSOT Synthesis $\to$ Doctor Audit).
  - **The "Hands" (CLI & MCP Tool Layer)**: The agent executes `./bin/ai-assist` CLI commands (or calls `ai-assist mcp-server` tools) to compile configurations, validate context budgets (< 80 lines), and ensure zero secret leaks.

---

## 3. Configuration Manifest (`ai-assist.json`)

When generated, a lightweight manifest is saved at the root:

```json
{
  "$schema": "https://raw.githubusercontent.com/ai-assist-bootstrap/schema/main/config.schema.json",
  "version": "1.0.0",
  "project": {
    "name": "my-saas-app",
    "type": "nextjs",
    "packageManager": "pnpm"
  },
  "targets": [
    "agents-md",
    "cursor",
    "claude",
    "antigravity",
    "copilot"
  ],
  "workflows": [
    "plan-execute-verify",
    "tdd-workflow",
    "git-conventions-pr"
  ],
  "skills": [
    "nextjs-app-router",
    "tailwind-shadcn",
    "security-audit"
  ],
  "mcp": {
    "enabled": ["filesystem", "postgres"]
  }
}
```

This manifest allows:
1. Re-syncing rules when `ai-assist-bootstrap update` is run.
2. Adding new skills on-the-fly (`ai-assist-bootstrap add-skill stripe-integration`).
3. Seamless onboarding for team members.

