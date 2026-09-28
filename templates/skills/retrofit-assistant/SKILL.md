---
name: retrofit-assistant
description: Guides the agent through analyzing, interviewing, and retrofitting modern AI configurations into complex or polyglot codebases.
---

# Retrofit Assistant Runbook

## When to Use
- When asked to add, retrofit, or bootstrap AI configurations (`AGENTS.md`, `CLAUDE.md`, Cursor rules, Skills) in an existing codebase.
- When `ai-assist add` fails, reports low confidence, or detects a complex polyglot / monorepo project.
- When standardizing messy or obsolete prompt configurations.

---

## Step-by-Step Procedure

### Step 1: Reconnaissance
1. Run a fast directory inspection:
   ```bash
   find . -maxdepth 3 -name "package.json" -o -name "Cargo.toml" -o -name "go.mod" -o -name "pyproject.toml"
   ```
2. Inspect package dependencies to identify frameworks, test suites, and databases.
3. Check for existing rule files:
   ```bash
   ls -la AGENTS.md CLAUDE.md .cursor/rules .github/copilot-instructions.md
   ```

### Step 2: Developer Alignment
If the project has multiple frameworks or ambiguous tools (e.g. both Vitest and Jest, or Prisma and raw SQL):
- Do NOT guess silently.
- Ask 1–2 specific multiple-choice questions to confirm primary conventions and canonical commands.

### Step 3: Synthesis & Scaffolding
1. Try the standard stack profile first:
   ```bash
   ./bin/ai-assist list-stacks
   ./bin/ai-assist add --stack <detected-stack>
   ```
2. If custom tailoring is required:
   - Keep `AGENTS.md` and `CLAUDE.md` **under 80 lines**.
   - Partition file-specific conventions into `.cursor/rules/<name>.mdc` with accurate `globs`.
   - Place detailed procedures into `.agents/skills/<name>/SKILL.md`.

### Step 4: Verification
Audit the generated configuration using doctor:
```bash
./bin/ai-assist doctor
```
Ensure:
- [ ] Context budget passes (< 80 lines).
- [ ] Zero dead globs.
- [ ] Valid YAML frontmatter on all skills.
- [ ] Zero hardcoded credentials or API keys.
