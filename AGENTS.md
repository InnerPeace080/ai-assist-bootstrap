# AGENTS.md - ai-assist-bootstrap Development Rules

## 1. The Golden Rule: Real-World Grounding

* **ALWAYS research the internet first**: Before writing any new rule, stack profile, skill runbook, CLI command, or configuration template, query the web or official repositories.
* **NEVER make up or hallucinate**: Do not guess CLI commands, API signatures, framework invariants, or community conventions.
* **Grounded in Verified Standards**: Every configuration must align with official documentation or battle-tested repositories (e.g. `github/spec-kit`, `open-gsd/gsd-core`, `awesome-cursorrules`, `claude-code-best-practices`, `trailofbits/claude-code-config`).

---

## 2. Core Architectural Principles

* **Context Budgeting**: Keep global instructions lean (< 80 lines). Never flood the model's context window with unbudgeted prompts.
* **Progressive Disclosure**:
  * Global invariants live in `AGENTS.md` / `CLAUDE.md`.
  * Scoped rules live in `.cursor/rules/*.mdc` (restricted by file `globs`).
  * Complex runbooks live in on-demand `.agents/skills/<name>/SKILL.md` files.
* **Single Source of Truth (SSOT)**: Maintain canonical template definitions that compile into target agent formats (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `.agents/skills/`, and GitHub Copilot).
* **Dual-Mode Operation**:
  * `create`: Greenfield scaffolding (code + AI configurations from scratch).
  * `retrofit` / `add`: Brownfield detection and injection into existing codebases.
* **Bidirectional Sync & Evolution**: Support non-destructive 3-way updates from upstream templates, personal override layers, and `export-back` commands to extract working project rules into a central library.
* **Provenance & Lineage Tracking**: Every imported rule or skill must track its origin, license, upstream commit hash, and personal modification history in frontmatter metadata and `registry.lock`.



---

## 3. Supported Stacks (10 Profiles)

1. **Next.js**: React 19, App Router, Server Components vs Client Components boundary, Server Actions, Zod.
2. **NestJS**: TypeScript, modular architecture, DTO validation, Dependency Injection, Prisma / TypeORM.
3. **React Native & Expo**: Expo Router, NativeWind, mobile performance (`FlatList`/`FlashList`), SafeArea.
4. **Monorepo**: Turborepo + `pnpm` workspaces, strict package boundaries, shared types/contracts.
5. **React.js SPA**: Vite, TanStack Query v5 (query key factories, no `useEffect` fetching), Zustand for UI state.
6. **Golang**: Go 1.23+, `internal/` package privacy, explicit `%w` error wrapping, structured concurrency with `context.Context`, table tests (`go test -race`).
7. **Python**: Python 3.12+, FastAPI, Pydantic v2, `uv` package manager (`uv run`), `ruff` linter/formatter, SQLAlchemy 2.0 async.
8. **Rust**: Rust 1.83+ (2021 Edition), Axum, Tokio, `thiserror` (domain errors), `anyhow` (binaries), zero `.unwrap()` in production, `cargo clippy`.
9. **Erlang**: OTP 26+, `rebar3`, supervision trees ("let it crash"), GenServer callback separation, Dialyzer `-spec` types.
10. **Shell Scripting**: Bash 5+ / POSIX, `set -euo pipefail`, quoting rules, `shellcheck`, `shfmt`, modular `bin/` + `lib/`, `bats-core` testing.


---

## 4. Workflow Standards

* **Spec-Driven Development (SDD)**: Anchoring execution to `.specify/` specs and `CONSTITUTION.md` (Spec Kit).
* **Anti-Context-Rot**: Breaking large tasks into discrete phases executed in clean subagent contexts; tracking progress in `STATE.md` (GSD).
* **Workflow Check Gates & Hooks**: Enforce multi-tier gates before commits (agent `PreToolUse` hooks, Lefthook git hooks, reviewer subagent convergence checks, secret scanners).
* **Verification First**: Verify changes using stack test suites before committing.
* **Conventional Commits**: Format commits with `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
* **Design-First Phase**: Always finalize architecture and specifications in `docs/` before modifying templates, code, or scripts.
* **Reliable File Operations**: Avoid IDE GUI diff replacement tools that trigger desynchronization/approval errors; apply file changes directly and deterministically.

