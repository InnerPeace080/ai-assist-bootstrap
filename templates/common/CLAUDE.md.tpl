# CLAUDE.md - {{PROJECT_NAME}} Guidelines

## Commands
- Install: `{{INSTALL_CMD}}`
- Dev Server: `{{DEV_CMD}}`
- Run Tests: `{{TEST_CMD}}`
- Lint: `{{LINT_CMD}}`
- Typecheck: `{{TYPECHECK_CMD}}`
- Build: `{{BUILD_CMD}}`

## Architecture & Conventions
- Stack: {{STACK_SUMMARY}}
- Package Manager: `{{PACKAGE_MANAGER}}`
- Testing Framework: {{TEST_FRAMEWORK}}

## Code Invariants
{{STACK_RULES}}

## Workflow & Safety Rules
- Verify changes with `{{TEST_CMD}}` and `{{LINT_CMD}}` before finishing.
- Never commit secret files (`.env*`, private keys, certificates).
- Follow conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.

