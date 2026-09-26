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

## 6. Integration in `ai-assist-bootstrap`

When bootstrapping a project (`create` or `retrofit` mode), `ai-assist-bootstrap` will configure:
1. **Agent Tool Hook**: Interceptor script `.claude/hooks/pre-commit-gate.sh` blocking premature agent commits.
2. **Git Hook Runner**: Pre-configured `lefthook.yml` or `husky` matching the chosen stack.
3. **Reviewer Subagent Template**: Pre-configured Critic/Reviewer persona definition (`.claude/agents/code-reviewer.md` or `.agents/skills/code-review/SKILL.md`).
4. **Secret Scanner**: Out-of-the-box secret check blocking `.env` commits.

