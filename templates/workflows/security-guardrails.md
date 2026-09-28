# Workflow: Security Guardrails & Secret Isolation

## Purpose
Enforces non-negotiable security boundaries to prevent secret leakage, data exfiltration, and unsafe tool execution.

---

## 1. Secret Protection
- **Blocked Files**: Never read, print, stage, or commit:
  - `.env*`, `local.env`, `credentials.json`
  - Private SSH/TLS keys (`*.pem`, `*.key`, `id_rsa`)
  - Cloud provider credentials (`~/.aws/credentials`, `gcloud` keys)
- **Sanitization**: When generating code examples, always use placeholders (`YOUR_API_KEY`, `postgres://user:pass@localhost:5432/db`).

---

## 2. Unsafe Execution Boundaries
- **Destructive Commands**: Require explicit developer confirmation for:
  - `rm -rf`, `git reset --hard`, `git push --force`
  - Database dropping (`DROP DATABASE`, `DROP TABLE`)
  - Running raw strings through `eval` or shell interpretation without quoting.

---

## 3. Dependency Auditing
- After adding or updating dependencies, run the package security auditor:
  - Node: `pnpm audit`
  - Python: `uv run pip-audit` / safety
  - Rust: `cargo audit`
  - Go: `govulncheck ./...`

