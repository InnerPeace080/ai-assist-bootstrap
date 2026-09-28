# 11. Agent Fleet & Parallel Orchestration

> **Architectural blueprint and implementation plan for coordinating concurrent multi-agent fleets, isolated Git worktrees, and automated branch integration in `ai-assist-bootstrap`.**

---

## 1. Overview & Motivation

As AI coding agents evolve beyond single-turn conversational assistants, engineering workflows are shifting from **sequential single-agent execution** to **parallel agent fleets** (teams of specialized agents collaborating on decoupled tasks).

### The Limits of Single-Agent Sessions

* **Serial Bottleneck**: Complex fullstack features (e.g. database migration + backend API + frontend UI + E2E tests) take excessive time when executed sequentially by a single agent.
* **Self-Grading Bias**: When the same agent writes code and verifies it, it tends to validate its own flawed assumptions.

### The Agent Fleet Solution
An **Agent Fleet** decomposes features into independent subtasks executed in parallel by specialized worker agents operating within **isolated Git worktrees**. A central Coordinator agent delegates work, monitors liveness, and an Integration worker reconciles branches through deterministic quality gates.

```
                             +-----------------------------------+
                             |     Fleet Coordinator / Lead      |
                             |   (Task Decomposition & Queue)    |
                             +-----------------------------------+
                                    |              |            |
                 +------------------+              |            +------------------+
                 v                                 v                               v
    +-------------------------+       +-------------------------+       +-------------------------+
    |     Backend Worker      |       |     Frontend Worker     |       |     Testing Worker      |
    |  .worktrees/task-api    |       |  .worktrees/task-ui     |       |  .worktrees/task-qa     |
    |  (Branch: feat/api)     |       |  (Branch: feat/ui)      |       |  (Branch: feat/qa)      |
    +-------------------------+       +-------------------------+       +-------------------------+
                 \                                 |                               /
                  \                                v                              /
                   +------------>  +-------------------------------+  <----------+
                                   |  Gatekeeper / Reviewer Agent  |
                                   |   (Independent Verification)  |
                                   +-------------------------------+
                                                   |
                                                   v
                                   +-------------------------------+
                                   |  Integration / Rebase Worker  |
                                   |   (Rebase, Merge & Teardown)  |
                                   +-------------------------------+
                                                   |
                                                   v
                                   +-------------------------------+
                                   |    Mainline Repository Git    |
                                   +-------------------------------+
```

---

## 2. Core Architectural Pattern: "One Task, One Branch, One Worktree"

The foundation of safe parallel agent execution is **filesystem and runtime isolation**. AI agents writing concurrently to the same working directory cause race conditions, corrupted git indexes, and conflicting file overwrites.

### 2.1 Git Worktree Isolation


```bash
# Coordinator creates isolated worktree for a task
git worktree add .worktrees/feat-api -b feat/api origin/main

# Worker agent executes task entirely inside .worktrees/feat-api/
cd .worktrees/feat-api
# ... agent implements code, runs tests, commits ...

# Coordinator or Integrator cleans up worktree after merge
git worktree remove --force .worktrees/feat-api

```

### 2.2 Runtime & Port Multiplexing

Worktrees isolate the filesystem, but shared runtime resources must also be isolated:
* **Port Allocation**: Assign dynamic non-colliding ports for dev servers (e.g. Worker 1 on port 3001, Worker 2 on port 3002).
* **Test Databases**: Use isolated SQLite files per worktree, or prefixed schemas in PostgreSQL (`test_feat_api`).
* **Environment Variables**: Provide worktree-specific `.env.local` files configured automatically by the orchestrator.

---

## 3. Fleet Topologies & Agent Personas

| Role                    | Persona / Capabilities        | Primary Responsibilities                                                                                                                   |
| :---------------------- | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **Fleet Coordinator**   | `Lead Architect`              | Decomposes user request into a Directed Acyclic Graph (DAG) of decoupled tasks; assigns tasks; tracks dependency order; monitors timeouts. |
| **Backend Worker**      | `API & Systems Specialist`    | Implements domain models, database migrations, controllers, and services inside backend worktree.                                          |
| **Frontend Worker**     | `UI/UX & Client Specialist`   | Implements components, pages, client state, and responsive styles inside frontend worktree.                                                |
| **QA / Test Worker**    | `Test Automation Engineer`    | Generates unit tests, integration test suites, and regression checks inside testing worktree.                                              |
| **Gatekeeper / Critic** | `Security & Quality Reviewer` | Spins up in clean context to audit each worker's pull request or branch against requirements and check gates.                              |
| **Integration Worker**  | `Release Engineer`            | Sequentially rebases approved branches onto main, executes full integration test suites, resolves conflicts, and deletes worktrees.        |

---

## 4. Inter-Agent Communication & State Protocol

To maintain coordination without unbounded context growth, the fleet communicates through structured state files and reactive messaging.


```
.fleet/
├── fleet.json              # Fleet configuration, concurrency caps, model mappings
├── queue/                  # Pending tasks waiting for dependency resolution
│   └── task-001.json
├── active/                 # Currently running tasks assigned to active worktrees

│   └── task-002-api.json
└── completed/              # Verified tasks ready for integration
    └── task-000-schema.json
```

### 4.2 Task Specification Contract (`.fleet/queue/task-*.json`)

```json
{
  "taskId": "task-002-api",
  "title": "Implement REST API for User Profiles",
  "assignedRole": "backend-worker",
  "dependencies": ["task-000-schema"],
  "worktreePath": ".worktrees/task-002-api",
  "branch": "feat/user-profiles-api",

  "scopeGlobs": ["src/api/**", "src/models/**"],
  "testCommand": "pytest tests/api",
  "status": "pending"
}
```

### 4.3 Reactive Event Wakeup (No Busy-Polling)

* Agents do not run busy-polling loops in terminals.
* Workers notify the Coordinator upon task completion via event signals or file write handoffs.
* The Coordinator uses event hooks or one-shot liveness timers to wake up when subtasks complete.

---

## 5. Branch Integration & Conflict Reconciliation Strategy

When multiple worker agents complete tasks in parallel, branches must be integrated safely into the mainline without regressing other features.

```mermaid
sequenceDiagram
    participant C as Fleet Coordinator
    participant W1 as Backend Worker
    participant W2 as Frontend Worker
    participant G as Gatekeeper Critic
    participant I as Integrator Worker

    C->>W1: Dispatch task-001 in worktree 1
    C->>W2: Dispatch task-002 in worktree 2
    W1->>W1: Complete code & unit tests
    W1->>G: Request Gatekeeper Audit (feat/api)
    G-->>W1: Quality Gate PASS
    W1->>C: Signal task-001 complete
    C->>I: Enqueue feat/api for integration
    I->>I: Rebase feat/api onto main & run full test suite
    I-->>C: Merged to main
    W2->>W2: Complete UI code
    W2->>G: Request GatekeeperAudit (feat/ui)

    G-->>W2: Quality Gate PASS
    C->>I: Enqueue feat/ui for integration
    I->>I: Rebase feat/ui onto updated main
   *Note over I: If conflict occurs, spawn Conflict Resolver Subagent
   *I-->>C: Merged to main & cleaned worktrees
```*

### Conflict Resolution Policy

1. **Dependency Ordering**: Core contracts, types, and database schemas are integrated first; consumers (frontend/APIs) are integrated second.
2. **Automated 3-Way Rebase**: Integrator attempts `git rebase main` on the worker branch.
3. **Conflict Resolver Subagent**: If Git encounters a conflict, a dedicated resolver subagent is spawned with access to:
   * Base common ancestor commit.
   * Mainline changes.
   * Worker branch changes.
4. **Verification Gate**: The full test suite (`npm test`, `cargo test`, `go test`, `pytest`) must pass on the integrated commit before pushing to main.

---

## 6. Resource Governance & Safety Controls

| Safety Control            | Mechanism                                     | Limit / Threshold                                                                   |
| :------------------------ | :-------------------------------------------- | :---------------------------------------------------------------------------------- |
| **Max Concurrent Agents** | Configured in `.fleet/fleet.json`             | Default: 3 parallel workers (configurable up to 8).                                 |
| **Per-Agent Token Cap**   | Enforced by model selection / subagent config | Prevents runaway worker billing on stuck loops.                                     |
| **Liveness Heartbeat**    | Timeout watchdog                              | If worker produces zero file changes in 10 minutes, terminate and release worktree. |
| **Secret Scanning**       | Pre-commit hook & Doctor audit                | Scans all worktrees before branch integration.                                      |

| **Clean Teardown** | Coordinator teardown script | Prunes dead worktrees (`git worktree prune`) and deletes temporary branches. |

---

## 7. Framework Support & Target Agent Mappings

`ai-assist-bootstrap` serves as the unifying configuration engine across multiple agent runners. Here is how the fleet specification maps to leading multi-agent frameworks:


### 7.1 Claude Code Agent Teams (Anthropic)

* **Underlying Mechanism**: Native Agent Teams (powered by Anthropic's `TeammateTool`) combined with `claude --worktree <name>`.
* **Mapping**:
  * Coordinator maps to the Claude Code **Team Lead**.

  * Worker subtasks map to Claude Code **Teammates** operating within `.claude/worktrees/<task>/`.
  * `ai-assist-bootstrap` outputs `.claude/teams/` definitions and hook configurations for team lifecycle events.

### 7.2 Google Antigravity Subagent System

* **Underlying Mechanism**: Built-in subagent invocation (`invoke_subagent`) with first-class workspace virtualization.

* **Mapping**:
  * Workers use `Workspace: 'share'` (which automatically shares the parent repository via Git worktree semantics) or `Workspace: 'branch'` (providing an isolated cloned branch).
  * Direct communication via `send_message`, lifecycle management via `manage_subagents` (`list`, `kill`, `kill_all`), and wakeups via reactive notifications or `schedule`.

### 7.3 ccswarm (Rust Worktree Orchestrator)


* **Underlying Mechanism**: Dedicated background orchestration daemon managing Git worktrees for specialized agent pools.
* **Mapping**:
  * Compiles `.fleet/` task definitions directly into ccswarm task queues.
  * Enforces the "Sangha" evidence-backed verification and objection gate before code is merged.

### 7.4 OpenHands / SWE-agent
* **Underlying Mechanism**: Micro-agent architecture running inside `LocalWorkspace` or containerized `DockerWorkspace`.
* **Mapping**:
  * Direct filesystem path binding to `.worktrees/<task-id>`.
  * Guarantees agents do not execute destructive branch-switch operations (`git checkout` / `git switch`) across shared directories.

### 7.5 Universal Git Worktree Runner (Cursor, Windsurf, Aider, Terminal Multiplexers)
* **Underlying Mechanism**: Standard POSIX `git worktree` commands orchestrated by the `ai-assist fleet` CLI helper or custom shell scripts.
* **Mapping**:
  * Compatible with any AI assistant capable of running in a specified working directory.
  * Developers can launch separate terminal tabs, Cursor Composer windows, or background processes pointing to individual worktree directories.

### 7.6 Programmatic Orchestration Engines (LangGraph, CrewAI, AutoGen, Swarms, Ray)
For teams writing programmatic Python agent pipelines to automate codebase development:
* **LangGraph**: Use a **Supervisor Node** state graph where routing transitions dynamically provision and assign `.worktrees/task-*` directories, using conditional edges to trigger the Gatekeeper Reviewer before merging.
* **CrewAI**: Map worker personas (`Backend Specialist`, `Frontend Specialist`) to a `Crew` with `process=Process.hierarchical`, where the `manager_llm` delegates tasks with explicit worktree path parameters.
* **AutoGen (AG2)**: Use `GroupChatManager` for collaborative multi-turn debate between the Coder Worker and Gatekeeper Critic before signaling merge readiness.
* **Swarms**: Deploy `HierarchicalSwarm` or `AgentRearrange` to fan out tasks across parallel worker agents bound to isolated worktree directories.
* **Ray**: Run high-concurrency worker pools as distributed Ray Actors, where each actor runs in a dedicated sandboxed worktree across cluster nodes (ideal for massive regression testing and SWE-bench sweeps).

---

## 8. Phased Implementation Roadmap


##* Phase 1: Workflow Specification & Templates (Immediate)
*
- *x] Author comprehensive architecture design in `docs/11-agent-fleet-and-parallel-orchestration.md`.
* [ ] Create canonical workflow template in `templates/workflows/agent-fleet-orchestration.md`.
* [ ] Update `docs/04-workflows-and-skills-catalog.md` and `docs/05-roadmap-and-implementation.md`.

### Phase 2: Worktree Management Automation

- [ ] Add `src/fleet.py` module with commands:
  * `ai-assist fleet init`: Scaffolds `.fleet/` directory and `.worktrees/` in `.gitignore`.
  * `ai-assist fleet spawn <role> <task-name>`: Creates branch, initializes worktree, and configures subagent instructions.
  * `ai-assist fleet integrate <branch>`: Runs rebase, verification gate, and worktree cleanup.
  * `ai-assist fleet clean`: Prunes stale worktrees and cleans temporary branch artifacts.

### Phase 3: Diagnostics & Doctor Integration

- [ ] Extend `src/doctor.py` to audit fleet health:
  * Detect orphaned worktrees not tracked in `.fleet/`.
  * Detect branch drift between active worktrees and `main`.
  * Verify `.worktrees/` is present in `.gitignore`.
