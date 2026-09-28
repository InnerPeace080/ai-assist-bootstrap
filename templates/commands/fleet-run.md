# /fleet-run - Parallel Multi-Agent Fleet Execution

Decompose a feature request into a DAG of decoupled subtasks and orchestrate execution across isolated Git worktrees.

## Instructions
Execute the **`agent-fleet-orchestration`** workflow:

1. **Feature Task Decomposition (DAG)**:
   - Break down the feature description into independent subtasks with clear boundary contracts (e.g. `task-01-schema`, `task-02-api`, `task-03-ui`, `task-04-qa`).
2. **Worktree Provisioning ("One Task, One Branch, One Worktree")**:
   - Provision dedicated Git worktrees for parallel worker agents:
     ```bash
     git worktree add .worktrees/<task-id> -b feat/<task-id> origin/main
     ```
   - Assign non-colliding dev ports and isolated test database names.
3. **Independent Gatekeeper Verification**:
   - Each worker must complete its task and submit its diff to an independent Gatekeeper/Critic agent in a clean context.
4. **Sequential Integration & Rebase**:
   - Rebase approved task branches sequentially onto `main`.
   - Run the full test suite on each rebased commit.
   - If conflicts arise, spawn a Conflict Resolver subagent with 3-way diff context.
5. **Teardown**:
   - Clean up worktrees upon merge:
     ```bash
     git worktree remove --force .worktrees/<task-id>
     git branch -d feat/<task-id>
     ```
