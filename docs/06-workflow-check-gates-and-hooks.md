# 06. Workflow Check Gates & Agent Hooks

This document specifies the multi-tier **Quality Check Gates** and **Agent Hooks** system designed for `ai-assist-bootstrap`. It ensures that neither primary agents nor subagents can commit code, merge branches, or finalize tasks without passing deterministic verification.

---

## 1. The Need for Quality Check Gates

While instruction prompts (`CLAUDE.md`, `AGENTS.md`) provide guidelines, LLMs can still occasionally suffer from:
* **Premature Commits**: Committing code before running tests or typechecks.
* **Secret Leakage**: Accidentally staging `.env`, private keys, or API tokens.
* **Regression Bugs**: Breaking existing features without verifying test suites.
* **Destructive Shell Commands**: Running `git push --force` or dropping database tables.

To solve this, `ai-assist-bootstrap` implements a **4-Tier Defense-in-Depth Quality Gate Architecture**:

```
+───────────────────────────────────────────────────────────────────────────+
|                  4-Tier Agent Quality Gate Architecture                   |
+───────────────────────────────────────────────────────────────────────────+

  [ Tier 1: Agent Pre-Tool Hooks ]
    * Claude Code `PreToolUse` hook intercepts `git commit` / bash calls.
    * Antigravity `hooks.json` pre-tool validation.
    * Returns exit code 2 / block signal if gate conditions are not met.
                        │
                        ▼
  [ Tier 2: Repository Git Hooks ]
    * Native Git / Husky / Lefthook / `pre-commit` runner.
    * Secret scanner (`gitleaks`, `secretlint`).
    * Automated linter (`eslint`, `ruff`, `golangci-lint`, `cargo clippy`, `shellcheck`).
    * Typecheck (`tsc --noEmit`, `mypy`, `cargo check`).
                        │
                        ▼
  [ Tier 3: Gatekeeper / Reviewer Subagents ]
    * Independent Reviewer subagent in fresh context.
    * Audits diff against spec (Convergence check from Spec Kit).
    * Signs off on acceptance criteria before task handoff.
                        │
                        ▼
  [ Tier 4: CI/CD & Safe-Outputs ]
    * GitHub Agentic Workflows (`gh-aw`) with `safe-outputs`.
    * Automated PR test runner; prevents direct push to protected branches.
```

---

## 2. Tier 1: Agent Pre-Tool & Post-Tool Hooks

Agent hooks intercept tool execution directly inside the AI runner's runtime (Claude Code, Antigravity, etc.).

### Claude Code Hooks Architecture
Configured in `.claude/settings.json` or `.claude/hooks/`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "./.claude/hooks/pre-tool-gate.sh"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "FileEdit",
        "command": "./.claude/hooks/post-edit-format.sh"
      }
    ]
  }
}
```

#### How the Gate Interceptor Works (`pre-tool-gate.sh`):
1. Claude Code passes tool call payload (command string) as JSON via `stdin`.
2. The gate script checks if the command contains `git commit` or `git push`:
   - If attempting `git commit`:
     - Checks if tests have been run and passed in the current session.
     - Runs fast typecheck and linter.
     - Checks for unstaged/untracked secret files (`.env*`, `*.pem`, `id_rsa`).
   - If verification fails:
     - Exits with status `2` (Blocking Signal).
     - Prints structured error to `stderr`: `[GATE BLOCKED] Cannot commit: 2 test failures detected in auth.service.spec.ts`.
     - The agent is prevented from executing the commit and is forced to fix the test.

---

## 3. Tier 2: Repository Git Quality Gates (Lefthook / Husky)

Git hooks provide deterministic enforcement at the repository level. Even if an agent bypasses tool hooks, Git itself will refuse the commit.

### Recommended Tool: `Lefthook` (Fast, cross-platform, zero-dependency binary) or `pre-commit`

#### `lefthook.yml` Configuration Template:
```yaml
pre-commit:
  parallel: true
  commands:
    secrets-audit:
      run: gitleaks protect --staged --verbose
    lint:
      glob: "*.{js,ts,jsx,tsx,py,go,rs,sh}"
      run: ./scripts/lint-staged.sh {staged_files}
    typecheck:
      run: ./scripts/typecheck.sh

pre-push:
  commands:
    test-suite:
      run: ./scripts/quick-test.sh
    no-force-main:
      run: |
        branch="$(git rev-parse --abbrev-ref HEAD)"
        if [ "$branch" = "main" ] || [ "$branch" = "master" ]; then
          echo "Direct pushes to main branch are forbidden."
          exit 1
        fi
```

---

## 4. Tier 3: Subagent Verification Gates (Gatekeeper / Critic Pattern)

In multi-agent systems (e.g. GSD, BMAD, Antigravity subagents), the **Coder Agent** and **Reviewer Agent** are strictly separated.

```
       [ Coder Subagent ]
        Writes code to meet task requirement
              │
              ▼
   [ Subagent Completion Signal ]
              │
              ▼
  [ GATEKEEPER / REVIEWER SUBAGENT ] ──(Spins up in clean context)
    1. Reads Spec & Acceptance Criteria
    2. Runs `git diff` against base branch
    3. Runs stack test suite
    4. Audits code for security & edge cases
              │
         ┌────┴────┐
      [PASS]     [FAIL]
         │         │
         │         ▼
         │   [Rejection Notice]
         │   Returns explicit issue list to Coder Subagent
         │   (Coder fixes defects; gate re-runs)
         ▼
[ Authorized Order to Commit ]
  Reviewer signs off -> Commits atomic diff -> Updates STATE.md
```

### Why Subagent Gates are Superior:
* **Context Isolation**: The Reviewer subagent runs in a fresh context, free from the conversational rationalizations and biases accumulated by the Coder subagent.
* **Deterministic Convergence**: Directly enforces the **Convergence Phase** from GitHub Spec Kit, verifying that the implementation matches the original `.specify/specs/` document.

---

## 5. Tier 4: CI/CD Safe-Outputs (GitHub Agentic Workflows)

When agents operate in autonomous pipelines (e.g. GitHub Actions with `gh-aw`):
* Agents are given **read-only** access to the target repository.
* Operations that modify code are restricted to **Safe-Outputs**:
  - The agent generates a suggested patch / branch and opens a Pull Request.
  - Automated CI test suites execute on the PR.
  - Human or automated CODEOWNERS must approve before any merge to production.

---

## 6. Agent Harness Workflow & Custom Gateway Script (Agent Checkpoint)

In production agentic architectures (e.g. automated evaluation suites, SWE-bench runners, continuous coding bots, and parallel fleet execution), agents operate within an outer **Agent Harness**. 

The harness is the runtime scaffolding that drives the agent through a task's full lifecycle. Rather than allowing the agent to self-declare completion or push changes unchecked, the harness enforces a deterministic **Agent Checkpoint Step** via a **User-Customizable Gateway Script**.

```
+─────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    AGENT HARNESS WORKFLOW                                       |
+─────────────────────────────────────────────────────────────────────────────────────────────────+

  [ Task Ingestion ] ──> [ Plan Phase ] ──> [ Atomic Execution ] 
                                                   │
                                                   ▼
                                     ┌───────────────────────────┐
                                     │   AGENT CHECKPOINT STEP   │
                                     │ (Invokes Gateway Script)  │
                                     └─────────────┬─────────────┘
                                                   │
                         ┌─────────────────────────┴─────────────────────────┐
                         ▼                                                   ▼
                [ Exit 0: PASS ]                                    [ Exit != 0: REJECTED ]
                         │                                                   │
                         ▼                                                   ▼
           ┌───────────────────────────┐                       ┌───────────────────────────┐
           │ Record State Checkpoint   │                       │ Structured Feedback Loop  │
           │ Update .agents/checkpoint │                       │ Harness feeds stderr/logs │
           │ Advance to Commit/PR/Next │                       │ Agent self-corrects       │
           └───────────────────────────┘                       │ (Retry budget: 1..3)      │
                                                               └─────────────┬─────────────┘
                                                                             │
                                                                   ┌─────────┴─────────┐
                                                                   ▼                   ▼
                                                            [ Retries Left ]    [ Budget Exceeded ]
                                                            Agent refines code  Rollback to Last Good
                                                            Re-runs checkpoint  Checkpoint & Escalate
```

### 6.1 The Gateway Script Contract

The Gateway Script (e.g., `./scripts/agent-checkpoint-gateway.sh` or `.agents/checkpoints/gateway.sh`) is a user-defined executable that acts as the ultimate gatekeeper for the checkpoint step.

#### Execution Context & Environment Variables
When the harness reaches an agent checkpoint, it invokes the gateway script with standard environment variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `AGENT_TASK_ID` | Identifier of the active task or ticket | `task-auth-042` |
| `AGENT_PHASE` | Current harness execution phase | `implementation`, `refactor`, `pre-commit` |
| `AGENT_CHECKPOINT_NAME` | Name of the milestone or gate being evaluated | `unit-tests-and-lint`, `contract-verification` |
| `GIT_BASE_COMMIT` | Base Git commit hash before the agent began edits | `a1b2c3d` |
| `HARNESS_RETRY_COUNT` | Current retry attempt index (0-indexed) | `1` |

#### Standardized Exit Code Semantics

The gateway script must follow deterministic exit code conventions:

* **Exit Code `0` (`CHECKPOINT_PASS`)**:
  - The checkpoint criteria are fully satisfied (e.g., all tests pass, zero lint errors, schema matches specification).
  - The harness records the checkpoint snapshot and allows the workflow to progress to the next phase or finalize the commit.
* **Exit Code `2` (`CHECKPOINT_BLOCKED_RETRYABLE`)**:
  - Verification failed, but the failure is recoverable (e.g., test assertion failure, typecheck error, unformatted file).
  - The harness intercepts `stdout` and `stderr`, formats the output as structured diagnostic feedback (`[CHECKPOINT GATEWAY FAILED] ...`), and presents it back to the agent for self-correction.
* **Exit Code `1` or `>2` (`CHECKPOINT_FATAL_HALT`)**:
  - Unrecoverable or security policy violation (e.g., secret detected, forbidden dependency added, destructive file operation).
  - The harness halts immediately, aborts the task, rolls back changes, and alerts a human operator (Human-in-the-Loop escalation).

---

### 6.2 Checkpoint State Persistence & Rollback Mechanics

To prevent context rot and cascading regressions:
1. **Checkpoint Lock (`.agents/checkpoints/checkpoint.lock`)**:
   - Stores the timestamp, current git SHA, task ID, and passing test summary when a checkpoint passes.
2. **Deterministic Rollback**:
   - If an agent fails the gateway check repeatedly and exhausts its retry budget (`maxRetries`, default: 3):
   - The harness rolls back uncommitted working directory edits to the last passing checkpoint:
     ```bash
     git reset --hard "$LAST_GOOD_CHECKPOINT_SHA"
     git clean -fd
     ```
   - This prevents corrupted state from poisoning subsequent subagents or tasks.

---

### 6.3 Configuration in `ai-assist.json`

Users configure their custom gateway script and checkpoint policy in `ai-assist.json`:

```json
{
  "$schema": "./schema/config.schema.json",
  "project": {
    "name": "my-nestjs-backend",
    "type": "nestjs"
  },
  "harness": {
    "enabled": true,
    "gatewayScript": "./scripts/agent-checkpoint-gateway.sh",
    "checkpointDir": ".agents/checkpoints",
    "maxRetries": 3,
    "timeoutSeconds": 300,
    "rollbackOnFailure": true,
    "strictMode": true
  }
}
```

---

### 6.4 Reference Implementation: Custom Gateway Script

Below is a reference implementation of `scripts/agent-checkpoint-gateway.sh` designed for NestJS projects:

```bash
#!/usr/bin/env bash
# scripts/agent-checkpoint-gateway.sh
# Custom Agent Checkpoint Gateway Script for NestJS Projects
set -euo pipefail

echo "============================================================"
echo " [GATEWAY] Evaluating Agent Checkpoint: ${AGENT_CHECKPOINT_NAME:-default}"
echo " Task ID: ${AGENT_TASK_ID:-unknown} (Attempt: ${HARNESS_RETRY_COUNT:-0})"
echo "============================================================"

# Step 1: Secret Scan on Uncommitted / Staged Edits
echo "--> Step 1/4: Scanning for hardcoded secrets..."
if git diff --cached -S"sk_live_" -S"ghp_" -S"AKIA" --quiet; then
  echo "    [OK] No common secret patterns detected in diff."
else
  echo "    [FATAL] Detected possible secret token in git diff!" >&2
  exit 1 # Fatal Halt
fi

# Step 2: Strict Typechecking
echo "--> Step 2/4: Running TypeScript strict compilation..."
if ! pnpm exec tsc --noEmit; then
  echo "    [FAIL] TypeScript compilation failed. Fix type errors above." >&2
  exit 2 # Retryable Block
fi

# Step 3: Lint & Formatting
echo "--> Step 3/4: Checking ESLint rules..."
if ! pnpm lint; then
  echo "    [FAIL] ESLint reported violations. Fix lint rules before checkpoint." >&2
  exit 2 # Retryable Block
fi

# Step 4: Unit Test Suite
echo "--> Step 4/4: Running automated test suite..."
if ! pnpm test -- --bail; then
  echo "    [FAIL] Unit tests failed. Fix failing test cases." >&2
  exit 2 # Retryable Block
fi

echo "============================================================"
echo " [GATEWAY] All Checkpoint Gates Passed Successfully!"
echo "============================================================"
exit 0
```

---

## 7. Integration in `ai-assist-bootstrap`

When bootstrapping or retrofitting a project (`create` or `retrofit` mode), `ai-assist-bootstrap` will configure:
1. **Agent Tool Hook**: Interceptor script `.claude/hooks/pre-commit-gate.sh` blocking premature agent commits.
2. **Git Hook Runner**: Pre-configured `lefthook.yml` or `husky` matching the chosen stack.
3. **Custom Gateway Script**: Scaffolds `scripts/agent-checkpoint-gateway.sh` linked in `ai-assist.json` for deterministic harness checkpoints.
4. **Reviewer Subagent Template**: Pre-configured Critic/Reviewer persona definition (`.claude/agents/code-reviewer.md` or `.agents/skills/code-review/SKILL.md`).
5. **Secret Scanner**: Out-of-the-box secret check blocking `.env` commits.


