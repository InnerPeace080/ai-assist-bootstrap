# 10. Rule Linting & Diagnostics (`doctor`)

This document defines the diagnostic engine and rule linter for `ai-assist-bootstrap`. It guarantees that all generated and customized rules, skills, and configurations remain healthy, budgeted, and compliant with multi-agent standards.

---

## 1. Why Rule Linting is Necessary

As projects evolve and multiple developers add custom rules and skills:
* **Context Window Creep**: A team member adds a 200-line guideline to `AGENTS.md`, blowing past the prompt budget and slowing down the agent.
* **Dead Rules**: A Cursor rule `.cursor/rules/legacy.mdc` references globs (`src/old-components/**`) that were deleted months ago.
* **Broken Skill Metadata**: A custom `SKILL.md` is missing a `description`, preventing agents from knowing when to trigger it.
* **Contradictory Instructions**: One rule tells the agent to use `pnpm`, while another specifies `npm install`.

---

## 2. The `ai-assist-bootstrap doctor` Diagnostic Suite

Running `ai-assist-bootstrap doctor` inspects the entire AI configuration layer:

```bash
ai-assist-bootstrap doctor
```

### Diagnostic Checks Performed:

| Category           | Check                   | Severity   | Rule / Threshold                                               |
| :----------------- | :---------------------- | :--------- | :------------------------------------------------------------- |
| **Context Budget** | Global Invariant Length | ⚠️ Warning  | `AGENTS.md` / `CLAUDE.md` must be `< 80` lines.                |
| **Frontmatter**    | `SKILL.md` Schema       | ❌ Error    | Must include valid `name` (kebab-case) and `description`.      |
| **Frontmatter**    | Cursor `.mdc` Schema    | ❌ Error    | Must include `description` and valid `globs` array.            |
| **Dead Rules**     | Glob Match Verification | ⚠️ Warning  | Warns if `.mdc` globs match 0 files in the repository.         |
| **Integrity**      | Broken Markdown Links   | ⚠️ Warning  | Checks that relative links in docs/skills point to real files. |
| **Conflicts**      | Contradiction Detector  | ❌ Error    | Flags conflicting package manager or test runner commands.     |
| **Security**       | Hardcoded Secrets       | 🛑 Critical | Scans rules, skills, and MCP configs for API keys or secrets.  |
| **Provenance**     | Lineage Completeness    | ℹ️ Info     | Verifies skills have `metadata.origin_repo` and license.       |

---

## 3. Example Doctor Terminal Output

```text
ai-assist-bootstrap doctor v1.0.0
Auditing: /media/Data/Codes/shell/ai-assist-bootstrap

[✓] Context Budget: AGENTS.md (48 lines) - PASS
[✓] Context Budget: CLAUDE.md (52 lines) - PASS
[!] Context Budget: .cursor/rules/frontend.mdc (92 lines) - EXCEEDS BUDGET (> 80 lines)
    Recommendation: Split complex procedures into on-demand `.agents/skills/`

[✓] Frontmatter Schema: 26/26 skills valid
[!] Dead Glob Warning: `.cursor/rules/legacy-api.mdc`
    Glob `src/api/v1/**` matched 0 files in repository.
    Recommendation: Delete or update glob pattern.

[✓] Security Audit: Zero hardcoded secrets found in MCP configs.
[✓] Provenance Audit: 100% of community skills tracked in `registry.lock`.

Summary: 1 Error, 2 Warnings. Run `ai-assist-bootstrap lint --fix` to auto-remediate.
```

---

## 4. Automated Auto-Fix (`ai-assist-bootstrap lint --fix`)

* Auto-formats markdown and frontmatter using `prettier`.
* Normalizes glob patterns.
* Prunes dead or orphaned rule files upon developer confirmation.
* Updates `registry.lock` checksums when skills are modified.

