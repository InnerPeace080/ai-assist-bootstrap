# 01. Research & Benchmarks

This document captures the landscape research, benchmark analysis, and key learnings from existing starter kits, rule repositories, and skill libraries for AI coding assistants.

---

## 1. Survey of the Current Ecosystem

The ecosystem of AI agent configurations currently falls into three primary categories:

```
                          AI Coding Configurations
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
[ Full Bootstrap Templates ]    [ Workflow Frameworks ]    [ Skill & Rule Libraries ]
- claude-code-template          - shanraisshan pattern     - anthropics/skills
- claude-code-best-practices    - obra/superpowers         - VoltAgent/awesome-skills
- creatyvin/project-template                               - awesome-cursorrules
- versoxbt/claude-initial-setup
```

---

## 2. In-Depth Analysis of Key Solutions

### A. Full Bootstrap Templates

#### 1. `scotthavird/claude-code-template`
* **Repository**: [scotthavird/claude-code-template](https://github.com/scotthavird/claude-code-template)
* **Overview**: An all-in-one starter template usable as a plugin, repository base, or devcontainer.
* **Key Features**:
  - Pre-configured slash commands, subagents, and hooks.
  - Built-in MCP (Model Context Protocol) servers.
  - Automated GitHub Workflows for `@claude` mentions in issues and pull requests, plus automated PR review.
  - **Egress Firewall**: Network sandbox restricting outbound connections to an explicit allowlist.
* **Pros**: High security posture, complete automation from local terminal to CI/CD.
* **Cons**: Monolithic, highly opinionated towards Claude Code; difficult to adapt to other AI tools or lightweight projects.

#### 2. `MuhammadUsmanGM/claude-code-best-practices`
* **Repository**: [MuhammadUsmanGM/claude-code-best-practices](https://github.com/MuhammadUsmanGM/claude-code-best-practices)
* **Overview**: Practical, lean whole-project starter kits pairing a concise `CLAUDE.md` with `.claude/` settings, skills, and hooks.
* **Key Features**:
  - 5 complete starter kits: **React**, **Next.js**, **Python**, **Go**, and **Rust**.
  - 11 focused `CLAUDE.md` templates tailored to specific project types.
  - Maintained with clean, non-bloated rules.
* **Pros**: High signal-to-noise ratio, respects context limits, clear separation by programming language.
* **Cons**: Primarily designed for manual copying, lacks an automated multi-agent synchronization layer.

#### 3. `creatyvin/project-template`
* **Repository**: [creatyvin/project-template](https://github.com/creatyvin/project-template)
* **Overview**: Multi-tool cross-compatibility template.
* **Key Features**:
  - Leverages `AGENTS.md` as the universal specification across Claude, GitHub Copilot, Cursor, OpenAI Codex, Devin, and Gemini CLI.
  - Includes `.cursor/rules/` and Copilot instruction bridges.
* **Pros**: Neutral, doesn't lock the team into a single AI client.
* **Cons**: Shallow skill definitions; lacks deep stack-specific architectural guidance and complex workflows.

#### 4. `versoxbt/claude-initial-setup`
* **Repository**: [versoxbt/claude-initial-setup](https://github.com/versoxbt/claude-initial-setup)
* **Overview**: Massive "batteries-included" setup.
* **Key Features**:
  - 75 skills, 14 subagents, 15 slash commands, 8 rules, and 6 hooks.
  - Exporters to translate setups into Cursor, Copilot, and Codex formats.
* **Pros**: Incredible variety of pre-baked capabilities.
* **Cons**: **Severe context bloat**. Injecting dozens of skills and rules exhausts prompt tokens, slows agent latency, and triggers model hallucinations.

---

### B. Workflow-Focused Frameworks

#### 1. `shanraisshan/claude-code-best-practice`
* **Repository**: [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice)
* **Core Philosophy**: Orchestration pattern of **Command → Agent → Skill**.
* **Workflow Loop**:
  $$\text{Research} \longrightarrow \text{Plan} \longrightarrow \text{Execute} \longrightarrow \text{Review} \longrightarrow \text{Ship}$$
* **Takeaway**: Workflows should enforce phased discipline. Agents should not write code before completing research and proposing a verified plan.

#### 2. `obra/superpowers`
* **Repository**: [obra/superpowers](https://github.com/obra/superpowers)
* **Core Philosophy**: TDD-centric and disciplined brainstorming workflows.
* **Workflow Loop**:
  $$\text{Brainstorm / Requirements} \longrightarrow \text{Technical Plan} \longrightarrow \text{TDD Cycle (Red/Green/Refactor)} \longrightarrow \text{Code Review}$$
* **Takeaway**: Test-Driven Development (TDD) provides verifiable truth grounds for AI agents. When agents write the test first, hallucination rates drop drastically.

---

### C. Skill & Rule Libraries (Cherry-Pick Repositories)

| Library                              | Focus                                               | Volume & Format                                | Key Benefit                                                      |
| :----------------------------------- | :-------------------------------------------------- | :--------------------------------------------- | :--------------------------------------------------------------- |
| **`anthropics/skills`**              | Official Anthropic skill repository                 | High-quality, curated `SKILL.md` files         | Baseline standard for skills syntax                              |
| **`VoltAgent/awesome-agent-skills`** | Production agent skills from real engineering teams | 1000+ skills across DevOps, DB, Cloud, Testing | Real-world tested, avoids artificial toy prompts                 |
| **`PatrickJS/awesome-cursorrules`**  | Community rules for Cursor                          | Focused `.cursorrules` and `.mdc` files        | Rich library of framework-specific rules (Next.js, NestJS, etc.) |
| **`claude-code-template` (Topics)**  | Specialized application templates (e.g. n8n)        | Domain-specific agent packs + MCP configs      | Proves the value of niche domain profiles                        |

---

## 3. Comparison Matrix

| Criterion                      | Heavyweight Kits (`versoxbt`, `scotthavird`)   | Lean Kits (`MuhammadUsmanGM`, `creatyvin`)  | **`ai-assist-bootstrap` (Our Target)**                      |
| :----------------------------- | :--------------------------------------------- | :------------------------------------------ | :---------------------------------------------------------- |
| **Context Window Consumption** | ❌ Very High (often > 20k tokens just in rules) | ⚠️ Low, but fixed                            | ✅ **Optimal (Progressive disclosure, budgeted rules)**      |
| **Multi-Agent Support**        | ⚠️ Partial (export scripts or Claude-centric)   | ⚠️ Mixed (either AGENTS only or Claude only) | ✅ **Full (Single Source of Truth compiled to all)**         |
| **Framework Tailoring**        | ❌ Generic                                      | ⚠️ Static per-language folders               | ✅ **Deep Stack Profiles (Next.js, NestJS, Expo, Monorepo)** |
| **Bootstrap Automation**       | ❌ Manual git clone / copy-paste                | ❌ Manual copy-paste                         | ✅ **Interactive CLI + Configurable manifest**               |
| **Workflow Discipline**        | ⚠️ Complex / Rigid                              | ❌ Mostly just rules, no workflows           | ✅ **Built-in Plan/TDD/PR orchestration**                    |
| **Existing Repo Retrofit**     | ❌ Difficult (assumes new clone)                | ⚠️ Manual copying                            | ✅ **Auto-detects framework and injects AI layer**           |

---

## 4. Key Takeaways & Architectural Directives

1. **Beware of Context Window Dilution**:
   * *Rule*: Global rules must be strictly budgeted (under 60-100 lines).
   * *Rule*: Detailed procedures must live in on-demand **Skills** (`SKILL.md`), loaded only when required.
   * *Rule*: Path-specific rules must use glob matching (e.g. Cursor `.mdc` or Antigravity hierarchical rules) so frontend rules don't load when editing database migrations.

2. **Single Source of Truth (SSOT)**:
   * Developers should not manage `CLAUDE.md`, `.cursor/rules/web.mdc`, `GEMINI.md`, and `AGENTS.md` independently.
   * `ai-assist-bootstrap` must define the stack rules in a clean, unified format and compile or bridge them into the target agent folders automatically.

3. **Curated Presets over Infinite Catalogs**:
   * Instead of dumping 75 generic skills, bundle the top 3-5 battle-tested skills directly relevant to the chosen tech stack (e.g., Server Actions & App Router for Next.js; Dependency Injection & DTOs for NestJS).

4. **Pair Code Scaffolding with AI Scaffolding**:
   * Running `npx create-next-app` creates a codebase with zero AI context.
   * Running an AI-only template creates rules without a codebase.
   * `ai-assist-bootstrap` connects both: initialize the application code AND configure its AI brain simultaneously.

