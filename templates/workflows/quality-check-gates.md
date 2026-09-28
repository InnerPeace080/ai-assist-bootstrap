# Workflow: Quality Check Gates & Pre-Commit Interceptors

## Purpose
Enforces non-bypassable, machine-validated verification gates before any commit, merge, or task completion can proceed.

---

## The 4-Tier Gate Check:

1. **Tier 1 (Agent PreToolUse Hook)**:
   - Intercepts `git commit` and `git push` tool calls inside agent runners (Claude Code, Antigravity).
   - If tests or linters fail, exits with status `2` (Blocking Signal).
2. **Tier 2 (Repository Git Hook)**:
   - Enforced by `Lefthook` or `Husky` at the OS git level.
   - Runs `gitleaks` secret audit, linters, and typechecks on staged files.
3. **Tier 3 (Reviewer Subagent Gate)**:
   - A dedicated Reviewer Subagent spins up in clean context to inspect the diff against requirements.
   - Authorizes or rejects the "Order to Commit".
4. **Tier 4 (CI/CD Safe-Outputs)**:
   - Agents open PRs with automated CI checks; protected branches disallow direct pushes.

