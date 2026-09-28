# /doctor - Repository Health & Context Budget Audit

Run comprehensive diagnostics on the current repository's AI configurations, context budgeting, and security invariants.

## Instructions
1. Run the diagnostic engine:
   ```bash
   ./bin/ai-assist doctor
   ```
2. Verify all 5 health tiers:
   - **Context Budget**: Confirm `AGENTS.md` and `CLAUDE.md` are strictly under 80 lines (< 500 tokens).
   - **Dead Globs**: Confirm all Cursor rule glob patterns in `.cursor/rules/*.mdc` match at least one file in the repository.
   - **Skill Schemas**: Confirm all `.agents/skills/*/SKILL.md` have valid `name` and `description` YAML frontmatter.
   - **Secret Leakage**: Ensure zero hardcoded API keys (`sk_live_*`, `ghp_*`, `AKIA*`, private keys) exist in scanned configurations.
   - **Provenance Tracking**: Ensure all skills are recorded in `templates/registry.lock`.
3. Present a formatted summary of any warnings or errors found, and suggest immediate remediation steps.
