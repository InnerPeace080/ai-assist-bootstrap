# /retrofit - Brownfield Codebase Retrofit

Launch the interactive 4-phase codebase reconnaissance, developer alignment interview, and AI configuration synthesis.

## Instructions
Execute the **`brownfield-retrofit`** workflow:

### Phase 1: Deep Reconnaissance
1. Scan the repository for build manifests and package managers:
   ```bash
   find . -maxdepth 3 -name "package.json" -o -name "Cargo.toml" -o -name "go.mod" -o -name "pyproject.toml" -o -name "rebar.config"
   ```
2. Map directory topology (frontend, backend, monorepo packages, test suites).
3. Identify existing or conflicting prompt files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules`).

### Phase 2: Developer Alignment Interview
If the codebase uses multiple frameworks or ambiguous libraries (e.g., both Vitest and Jest, or Prisma and raw SQL):
- Do NOT guess silently.
- Ask 1–2 specific multiple-choice questions to confirm primary conventions and canonical build/test commands.

### Phase 3: Single Source of Truth (SSOT) Synthesis
1. Attempt standard stack injection first:
   ```bash
   ./bin/ai-assist add --stack <detected-stack>
   ```
2. Tailor configurations:
   - Ensure `AGENTS.md` and `CLAUDE.md` are **strictly under 80 lines**.
   - Partition file-specific conventions into `.cursor/rules/<name>.mdc` with precise `globs`.
   - Install matching on-demand `.agents/skills/<name>/SKILL.md` runbooks.

### Phase 4: Doctor Verification Gate
Run `./bin/ai-assist doctor` and verify zero errors or warnings before marking the task complete.
