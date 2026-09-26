# ai-assist-bootstrap Documentation

Welcome to the documentation for **ai-assist-bootstrap**, a modular project generator and configuration engine designed to bootstrap modern applications with production-ready AI agent skills, rules, workflows, and tool configurations.

---

## 📚 Documentation Index

1. **[01. Research & Benchmarks](./01-research-and-benchmarks.md)**
   Comprehensive survey and analysis of existing AI agent templates, rule repositories, and skill libraries (Claude Code templates, Cursor rules, awesome-agent-skills, superpowers, etc.), analyzing their strengths, weaknesses, and key architectural lessons.

2. **[02. Architecture & System Design](./02-architecture-and-design.md)**
   Detailed design of the bootstrapping engine: Progressive Disclosure principle, Single-Source-of-Truth (SSOT) compilation model, multi-agent export strategy (`AGENTS.md`, `.cursor/rules`, `.claude/`, `.agents/skills`, Copilot), and dual-mode (`create` vs `retrofit`).

3. **[03. Stack Profiles](./03-stack-profiles.md)**
   Specifications, coding invariants, rule sets, and recommended skills for 10 supported project stacks:
   - **Next.js** (Fullstack / React 19 / App Router)
   - **NestJS** (Enterprise Backend / TypeScript)
   - **React Native & Expo** (Cross-Platform Mobile)
   - **Turborepo Monorepo** (Multi-app / Shared packages)
   - **React.js SPA** (Vite / TanStack Query / Zustand)
   - **Golang** (Go 1.23+ / Chi / sqlc / Table Tests)
   - **Python** (FastAPI / Pydantic v2 / uv / SQLAlchemy 2)
   - **Rust** (Cargo / Axum / Tokio / sqlx / thiserror)
   - **Erlang** (OTP 26+ / rebar3 / Supervision Trees)
   - **Shell Scripting** (Bash 5+ / POSIX / shellcheck / bats-core)

4. **[04. Workflows & Skills Catalog](./04-workflows-and-skills-catalog.md)**
   In-depth specifications for core orchestration workflows (`plan-execute-verify`, `tdd-workflow`, `git-conventions-pr`, `security-guardrails`, `spec-driven-development` via Spec Kit, and `gsd-context-reset` via Get Shit Done) and catalog of 26 stack-specific agent skills adhering to the open `SKILL.md` progressive disclosure standard.

5. **[05. Roadmap & Implementation Plan](./05-roadmap-and-implementation.md)**
   Implementation blueprints, project structure, CLI technology options (Node/TS vs Shell vs Hybrid), phase-by-phase milestones, and testing strategy.

6. **[06. Workflow Check Gates & Agent Hooks](./06-workflow-check-gates-and-hooks.md)**
   Multi-tier quality gate defense architecture: agent tool hooks (`PreToolUse`, `hooks.json`), repository Git hooks (`Lefthook` / `Husky`), gatekeeper/reviewer subagents, and CI/CD safe-outputs.

7. **[07. Bidirectional Sync & Personal Overrides](./07-bidirectional-sync-and-personal-overrides.md)**
   Continuous evolution architecture: 3-way merge model (`copier`/`cruft` pattern) for non-destructive upstream updates, 3-tier configuration hierarchy (Base → Personal Global → Project Local), and `export-back` / `save-preset` CLI commands to extract working project rules into a central library.

8. **[08. Provenance Tracking & Source Lineage](./08-provenance-tracking-and-source-lineage.md)**
   Tracking community origins, upstream commit hashes, licenses, and personal modification history via in-file YAML frontmatter and central `registry.lock` bill of materials.

9. **[09. MCP Servers & Tool Integrations](./09-mcp-servers-and-tool-integrations.md)**
   Dynamic tool integrations across Claude Code, Cursor, and Antigravity: PostgreSQL/SQLite schema inspectors, Playwright browser test runners, Context7 live docs, and GitHub automation.

10. **[10. Rule Linting & Diagnostics (`doctor`)](./10-rule-linting-and-diagnostics.md)**
    Automated health diagnostic suite (`ai-assist-bootstrap doctor`): context budgeting audits (< 80 lines), dead glob detection, schema validation, and contradiction checks.





---

## 🎯 High-Level Vision

```
+-------------------------------------------------------------------------+
|                          ai-assist-bootstrap                            |
+-------------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
   [ Project Scaffolder ]                             [ AI Engine ]
   * Next.js, React SPA, Expo                         * Rules (Scoped .mdc, AGENTS.md)
   * NestJS, Golang, Python, Rust, Erlang, Shell      * Skills (Progressive SKILL.md)
   * Monorepo (Turborepo + pnpm)                      * Workflows (Plan/Execute, TDD)
   * Tooling (pnpm, uv, cargo, rebar3, go, bats)      * Tools & MCP (Databases, GitHub)
         |                                                   |
         +-------------------------+-------------------------+

                                   |
                                   v
             [ Ready-to-Code Production Repository ]
         Supported by Claude Code, Cursor, Antigravity,
                 Windsurf, Copilot, & Gemini CLI
```

