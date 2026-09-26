# 04. Workflows & Skills Catalog

This document defines the structured agent workflows and modular skill catalog provided by **`ai-assist-bootstrap`**.

---

## 1. Core Agent Workflows

Workflows establish behavioral guardrails for AI agents, transforming ad-hoc code generation into a disciplined, verifiable engineering process.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Core Agentic Workflows                          │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. Plan-Execute    │ 2. TDD Cycle       │ 3. Git & Review              │
│    Research        │    Write Test      │    Conventional Commits      │
│    Spec & Plan     │    Verify Failure  │    Automated Self-Review     │
│    Step Execution  │    Write Code      │    PR Summary Generation     │
│    Verification    │    Pass & Refactor │                              │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

---

### Workflow 1: `plan-execute-verify`


**Goal**: Prevent "cowboy coding" where an agent prematurely edits files without understanding system constraints.

* **Phase 1: Research & Discovery**
  * Read relevant files, dependencies, and configuration.
  * Check existing patterns, shared utilities, and conventions.
  * Never modify code during this phase.
* **Phase 2: Technical Specification & Plan**
  * Write a phased implementation plan.
  * Identify breaking changes, risks, and edge cases.
  * Present the plan to the developer for feedback/confirmation.
* **Phase 3: Atomic Execution**
  * Implement step-by-step in small, verifiable chunks.
  * Run typechecks (`tsc --noEmit`) and linter (`eslint`) after each step.
* **Phase 4: Verification & Self-Review**
  * Execute test suites (`pnpm test`).
  * Run git diff to audit changes against unintended edits.

---


### Workflow 2: `tdd-workflow`

**Goal**: Maximize AI correctness by anchoring code changes to automated test feedback.

```
       [ 1. Write Test ]
              │
              ▼
  [ 2. Run Test -> Must Fail (RED) ]
              │
              ▼
    [ 3. Implement Minimal Code ]
              │
              ▼
  [ 4. Run Test -> Must Pass (GREEN) ]
              │
              ▼
       [ 5. Refactor Cleanly ]
```

* **Rules**:
  1. The agent must create or update test cases *before* altering business logic.
  2. The test must fail for the expected reason (confirming the test actually tests the requirement).
  3. Write only the minimal implementation required to turn the test green.
  4. Refactor code for readability and performance while keeping tests passing.

---


### Workflow 3: `git-conventions-pr`

***oal**: Maintain a clean, auditable version control history.
*
* ***ommit Message Standard**:
  * *ollow [Conventional Commits](https://www.conventionalcommits.org/):
    * `feat(scope): ...`
    * `fix(scope): ...`
    * `refactor(scope): ...`
  * * `test(scope): ...`
    * `docs(scope): ...`
  * * `chore(scope): ...`
  * Body must explain the *why*, not just the *what*.
* **Pull Request Template Generator**:
  * Includes summary of changes, motivation, testing proofs (command outputs / screenshots), and checklist (tests passing, linter clean, docs updated).


---

### Workflow 4: `security-guardrails`

**Goal**: Enforce local security and privacy boundaries on AI agent operations.

* **Secret Detection**: Block agent tools from reading or printing `.env*`, private keys (`id_rsa`), or AWS/cloud credentials.
* **Command Sandboxing**: Require confirmation for destructive operations (`rm -rf`, `DROP TABLE`, `git push --force`).
* **Dependency Hygiene**: Check newly introduced packages against known CVE databases (`pnpm audit`).


---

### Workflow 5: `spec-driven-development` (from GitHub Spec Kit)

**Goal**: Eliminate "vibe coding" on non-trivial features by anchoring execution to persistent, versionable specifications.

``*
[ 1. Constitution ] ──> [ 2. Specify (What/Why) ] ──> [ 3. Plan (How) ] ──> [ 4. Tasks (Checklist) ] ──> [ 5. Implement & Converge ]
``*

* **Constitution (`CONSTITUTION.md`)**:
  * Encodes immutable team architectural principles (e.g., zero runtime `any`, strict accessibility, DB transactions for multi-row writes).
* **Specification (`.specify/specs/<feature>.md`)**:
  * Focuses on *user value* and *acceptance criteria* (Given/When/Then), not raw code.
* **Technical Plan (`.specify/plans/<feature>.md`)**:
  * Outlines architecture, schema changes, API endpoints, and dependency decisions.
* **Task Decomposition (`.specify/tasks/<feature>.md`)**:
  * Breaks work down into atomic, testable items with explicit dependencies.
* **Convergence Phase**:

  * Formal comparison between the generated code and the original specification before marking the feature complete.

---

### Workflow 6: `gsd-context-reset` (from Get Shit Done / Open GSD)

**Goal**: Eliminate "Context Rot" in long agentic coding sessions through fresh-context subagent execution.

* **The Problem**: After 10+ turns of code generation, diffing, and error fixing, the context window fills with noise. The model's attention degrades, leading to circular loops and hallucinations.
* **The GSD Solution**:
  1. **Persistent State Markers**: Progress is tracked in `.gsd/STATE.md` and `ROADMAP.md` in the repository, NOT in the ephemeral chat history.
  2. **Isolated Task Execution**: Instead of running an entire 5-step feature in one long chat, each task is dispatched to a **clean, fresh subagent context**.
  3. **Atomic State Handoff**: The subagent reads the state marker, completes its single focused task, commits its diff, updates `STATE.md`, and terminates cleanly.
* **Lifecycle**:
  $$\text{Discuss} \longrightarrow \text{Plan} \longrightarrow \text{Execute (Fresh Subagent Context)} \longrightarrow \text{Verify} \longrightarrow \text{Ship}$$

---

### Workflow 7: `quality-check-gates` (Automated Commit & Handoff Enforcement)

**Goal**: Prevent premature commits, secret leaks, and unverified code changes using deterministic tool hooks and reviewer subagents.

* **Multi-Tier Defense**:
  1. **Pre-Tool Interceptors**: Agent runtime hooks (`PreToolUse`, `hooks.json`) intercept `git commit` or `git push` commands. If test suites or typechecks fail, the hook returns exit code `2` to block execution.
  2. **Repository Git Hooks**: `Lefthook` runs staged secret audits (`gitleaks`), linters, and typechecks directly at the git level.
  3. **Gatekeeper / Reviewer Subagent**: The coder subagent cannot commit until an independent Reviewer subagent (spawned in clean context) verifies the diff against requirements and marks the quality gate as `PASS`.
* **Full Specification**: See [06. Workflow Check Gates & Agent Hooks](./06-workflow-check-gates-and-hooks.md).

---

## 2. The `SKILL.md` Standard

All skills generated by `ai-assist-bootstrap` adhere to the open `SKILL.md` format supported by Antigravity, Claude Code, and modern agent runners.

### Structure of a Skill

```markdown
---
name: skill-name
description: Clear, 1-2 sentence description explaining when and why the agent should activate this skill.
---

# Skill Title

## When to Use
Trigger conditions explaining the precise scenarios requiring this runbook.

## Step-by-Step Procedure
1. Step 1...
2. Step 2...

## Best Practices & Anti-Patterns
- DO: ...

- DON'T: ...

## Code Examples
```language
// Practical reference implementation
```

```

### Why This Format?
* **Zero Context Cost when Inactive**: The agent only reads the `name` and `description` in its system index (~20 tokens per skill).
* **Deep Knowledge on Demand**: When the agent recognizes a task matching the skill's description, it fetches the full file dynamically.

---

## 3. Catalog of Curated Skills

| Skill Name                  | Scope               | Description                                                                                                     |
| :-------------------------- | :------------------ | :-------------------------------------------------------------------------------------------------------------- |
| `nextjs-app-router`         | Next.js             | Deep runbook for Next.js App Router: layouts, parallel/intercepting routes, Server Actions, and revalidation.   |
| `tailwind-shadcn`           | Next.js / Web       | Guide for building accessible UI components using Tailwind CSS and Radix/shadcn primitives.                     |
| `nestjs-module-architect`   | NestJS              | Standardized procedure to generate modules, services, controllers, and DTOs with strict validation.             |
| `db-prisma-migration`       | Backend             | Best practices for Prisma schema modeling, index optimization, transactions, and zero-downtime migrations.      |
| `expo-router`               | React Native        | File-based navigation patterns, typed routing, modal stacks, and deep link configuration in Expo.               |
| `mobile-perf-tuning`        | React Native        | Optimization runbook for FlatList/FlashList, memory leaks, and native UI thread performance.                    |
| `api-testing`               | Backend / Fullstack | Creating deterministic unit tests and Supertest/Vitest integration tests with mocked DB state.                  |
| `security-audit`            | General             | Automated security checklist: secret leakage, SQL injection prevention, input sanitization, and CVE audits.     |
| `vite-react-spa`            | React.js            | SPA directory layout, code-splitting with `React.lazy`/`Suspense`, and bundle optimization with Vite.           |
| `tanstack-query-v5`         | React.js            | Query keys factory pattern, mutations, optimistic updates, and cache invalidation best practices.               |
| `tailwind-component-design` | React.js / Web      | Designing reusable UI components using Tailwind, class-variance-authority (`cva`), and ARIA states.             |
| `go-idiomatic-architecture` | Golang              | Standard layout (`cmd/`, `internal/`), constructor pattern, and clean package boundaries.                       |
| `go-concurrency-patterns`   | Golang              | Worker pools, channel synchronization, errgroup, and graceful shutdown handling.                                |
| `sqlc-database`             | Golang              | Type-safe Go code generation from raw SQL queries, transactions, and migration management.                      |
| `fastapi-pydantic-v2`       | Python              | FastAPI router structuring, Pydantic v2 validation, dependency injection, and OpenAPI customization.            |
| `sqlalchemy2-alembic`       | Python              | Async SQLAlchemy 2.0 ORM modeling with `Mapped[]`, relationship loading strategies, and Alembic migrations.     |
| `pytest-asyncio`            | Python              | Asynchronous test fixtures, transaction rollbacks for database isolation, and HTTPX async testing.              |
| `rust-axum-web`             | Rust                | Axum routing, state extractors, Tower middleware composition, and type-safe HTTP error responses.               |
| `rust-error-handling`       | Rust                | Strong domain error enums via `thiserror`, application-level `anyhow::Result`, and panic avoidance.             |
| `sqlx-compile-time`         | Rust                | Compile-time SQL query validation, offline preparation, connection pools, and transactional safety.             |
| `erlang-otp-design`         | Erlang              | Supervision tree topologies, application specifications (`.app.src`), and fault-tolerant restarts.              |
| `erlang-genserver`          | Erlang              | `gen_server` callbacks, state transition safety, message queuing, and timeout management.                       |
| `erlang-testing`            | Erlang              | EUnit test suites, Common Test distributed node testing, and process mocking with `meck`.                       |
| `shell-script-architecture` | Shell Script        | Modular `bin/` + `lib/` layout, robust `getopts` argument parsing, help generation, and signal trap lifecycles. |
| `shellcheck-remediation`    | Shell Script        | Diagnosing and remediating ShellCheck warnings (SC2086, SC2155, SC2046, unquoted parameters, subshell issues).  |
| `bats-testing`              | Shell Script        | Hermetic unit testing using `bats-core`, exit status assertions, output matching, and binary mocking.           |



