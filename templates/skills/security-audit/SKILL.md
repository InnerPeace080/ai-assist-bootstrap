---
name: security-audit
description: Automated security inspection runbook for secret leaks, vulnerable dependencies, SQL/command injection, and PreToolUse safety gates.
author: "Trail of Bits / OWASP Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/trailofbits/claude-code-config"
  upstream_file: "plugins/security/README.md"
  source_type: "community-curated"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Multi-tier secret scanning (Gitleaks, regex patterns)"
    - "PreToolUse gate prevention rules"
    - "Dependency audit command matrix"
---

# Security Audit & Pre-Commit Guardrails Runbook

## When to Use
Use this skill when auditing source code for security vulnerabilities, inspecting files before committing, configuring pre-commit hooks, or reviewing AI-generated code.

---

## 1. Secrets Detection Checklist

Before staging or committing any code, verify:
- [ ] No plaintext API keys (e.g. `sk_live_...`, `ghp_...`, `AKIA...`) in source files.
- [ ] `.env*` files are strictly added to `.gitignore` (except `.env.example`).
- [ ] Private keys (`id_rsa`, `*.pem`, `*.key`) are never staged.
- [ ] Run `gitleaks protect --staged --verbose` or `gitleaks detect` locally.

---

## 2. Injection Prevention Standards

| Vulnerability | Prevention Pattern | Forbidden Anti-Pattern |
| :--- | :--- | :--- |
| **SQL Injection** | Parameterized queries (`$1`, `?`), ORM query builders | String concatenation in SQL statements (`f"SELECT * FROM users WHERE id = {id}"`) |
| **Command Injection** | Use argument arrays (`subprocess.run(["ls", path])`) | Shell invocation with untrusted input (`shell=True`, `os.system("rm " + path)`) |
| **Path Traversal** | Validate resolved canonical path with `os.path.realpath` / `fs.realpath` | Accepting raw `../../` paths from user parameters |
| **XSS** | Contextual auto-escaping in templates, sanitize raw HTML | `dangerouslySetInnerHTML`, `v-html` without DOMPurify |

---

## 3. Dependency Vulnerability Audits

Run the stack-appropriate audit command before closing any task:

- **Node / TypeScript**: `pnpm audit` (or `npm audit --audit-level=high`)
- **Python**: `uv run pip-audit` (or `pip-audit -r requirements.txt`)
- **Rust**: `cargo audit`
- **Go**: `govulncheck ./...`
- **Erlang**: `rebar3 hex audit`

---

## 4. PreToolUse Agent Guardrails

AI agents operating under this repository must abort tool execution if a command matches dangerous operations:
- `rm -rf /` or recursive deletion on root or workspace root.
- `git push --force` or `git push -f` to protected branches (`main`, `master`).
- Direct execution of raw curl pipes to shell (`curl ... | sh` or `curl ... | bash`) without checksum validation.
- Outputting decrypted `.env` contents to logs or transcripts.

