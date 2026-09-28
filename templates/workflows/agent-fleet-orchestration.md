# Workflow: Agent Fleet & Parallel Worktree Orchestration

> Modeled after the **"One Task, One Branch, One Worktree"** standard and battle-tested multi-agent orchestrators (`ccswarm`, Claude Code Agent Teams, Antigravity Subagents).

## Purpose
Enables teams of specialized AI agents (Frontend, Backend, QA, Docs) to execute tasks concurrently on a shared repository without file collisions, branch interference, or conversational context rot.

---

## Core Rules & Invariants

1. **One Task, One Branch, One Worktree**:
   - Every concurrent task MUST be provisioned with its own dedicated Git worktree:
     ```bash
     git worktree add .worktrees/<task-id> -b feat/<task-id> origin/main
     ```
   - Parallel agents must NEVER execute `git checkout` or `git switch` inside existing worktrees.

2. **Decoupled Task Decomposition (DAG)**:
   - The **Fleet Coordinator** decomposes user requirements into independent subtasks with explicit inputs and outputs.
   - Core contracts, schemas, and API interfaces must be established before UI or client worker tasks begin.

3. **Runtime & Port Isolation**:
   - Each worker must be assigned unique ports and isolated test database names/schemas to prevent runtime lock contention.

4. **Independent Gatekeeper Verification**:
   - A worker agent cannot mark a task as complete or request integration until an independent **Gatekeeper / Reviewer** subagent (operating in a clean context) passes the diff against acceptance criteria.

5. **Sequential Integration & Rebase Pipeline**:
   - Approved task branches are merged sequentially into `main`:
     ```bash
     git checkout main && git pull
     git rebase main feat/<task-id>
     ```
   - The full verification test suite must pass on the rebased commit.
   - If a merge conflict occurs, a dedicated **Conflict Resolver** subagent is spawned with 3-way context to reconcile differences.

6. **Automatic Worktree Teardown**:
   - Once a task branch is integrated and pushed, the worktree is removed:
     ```bash
     git worktree remove --force .worktrees/<task-id>
     git branch -d feat/<task-id>
     ```
