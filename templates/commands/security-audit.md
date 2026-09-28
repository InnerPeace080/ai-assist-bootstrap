# /security-audit - Full Repository Security Audit

Execute an end-to-end security compliance audit across the codebase.

## Instructions
Execute the security audit checklist following `templates/skills/security-audit/SKILL.md`:

1. **Secret & Credential Scanning**:
   - Check for committed `.env*` files or unignored environment secrets.
   - Scan for regex patterns matching live Stripe API keys (`sk_live_*`), GitHub Personal Access Tokens (`ghp_*`), AWS Access Keys (`AKIA*`), and cryptographic private keys.

2. **Dependency Vulnerability Audit**:
   - Run stack-specific package audit commands:
     - Node/TS: `pnpm audit` / `npm audit`
     - Python: `uv run pip-audit` / `pip audit`
     - Rust: `cargo audit`
     - Go: `govulncheck ./...`

3. **Injection & Dangerous Execution Sweeps**:
   - Search for unparameterized raw SQL queries and string interpolations in database calls.
   - Audit dynamic command execution (`eval`, `exec`, `subprocess.Popen(..., shell=True)`, `system()`).
   - Verify all user inputs pass through validation schemas (e.g. Zod, Pydantic v2, class-validator).

4. **Git Hook & PreToolUse Validation**:
   - Verify that pre-commit hooks (`Lefthook` / `Husky`) are installed and active to guard against accidental secret commits.

5. **Report**:
   - Present a prioritized table of findings categorized by severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, with exact file locations and remediation steps.
