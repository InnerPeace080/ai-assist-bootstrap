# ai-assist-bootstrap

> **Bootstrap modern software projects (Next.js, NestJS, React Native, Monorepos) with production-ready AI skills, rules, workflows, and tool configurations.**

---

## 🚀 Overview

`ai-assist-bootstrap` bridges the gap between modern application code scaffolding and AI-assisted development. Instead of having to manually configure prompt files, skills, and rules across different AI tools, `ai-assist-bootstrap` provides an automated, modular, and context-budgeted system for teams using:

* **Claude Code** (`CLAUDE.md`, `.claude/` skills, commands, hooks)
* **Cursor** (`.cursor/rules/*.mdc` with scoped glob matching)
* **Antigravity / Gemini CLI** (`AGENTS.md`, `.agents/skills/*/SKILL.md`)
* **GitHub Copilot** (`.github/copilot-instructions.md`)
* **Windsurf & Devin** (Universal `AGENTS.md`)

---

## ⚡ Key Highlights

1. **Context Budgeting & Progressive Disclosure**: Prevents "prompt bloat" by enforcing lean global rules (< 75 lines) and loading detailed runbooks (`SKILL.md`) on demand.
2. **Single Source of Truth (SSOT)**: Write rules once; compile and synchronize them across all target AI assistants.
3. **Dual Mode**:
   - **`create`**: Scaffold new projects from scratch (Next.js, NestJS, Expo, Turborepo Monorepo) pre-wired with AI configs.
   - **`retrofit` / `add`**: Detect tech stack in an existing project and inject tailored AI rules and skills without altering business logic.
4. **Structured Workflows**: Built-in orchestration patterns:
   - `plan-execute-verify`: Phased discipline (Research → Plan → Atomic Execution → Review).
   - `tdd-workflow`: Test-driven development for verifiable code changes.
   - `git-conventions-pr`: Conventional commits and structured pull request descriptions.
   - `security-guardrails`: Secret isolation, audit hooks, and command sandboxing.

---

## 📖 Documentation Suite

The complete research, specifications, and guides are organized in the [`docs/`](./docs/README.md) directory:

| Document                                                                         | Description                                                                                                                        |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **[01. Research & Benchmarks](./docs/01-research-and-benchmarks.md)**            | Comparative analysis of existing templates (`claude-code-template`, `claude-code-best-practices`, `versoxbt`, `superpowers`, etc.) |
| **[02. Architecture & Design](./docs/02-architecture-and-design.md)**            | System design, Progressive Disclosure model, compiler pipeline, and `ai-assist.json` manifest                                      |
| **[03. Stack Profiles](./docs/03-stack-profiles.md)**                            | Rules, invariants, and skills for Next.js, NestJS, React Native (Expo), and Turborepo                                              |
| **[04. Workflows & Skills Catalog](./docs/04-workflows-and-skills-catalog.md)**  | Core agent workflows (`plan-execute`, `tdd`, `git`) and curated `SKILL.md` runbooks                                                |
| **[05. Roadmap & Implementation Plan](./docs/05-roadmap-and-implementation.md)** | Architecture evaluation, directory structure, milestones, and implementation phases                                                |

---

## 📁 Repository Structure

```
ai-assist-bootstrap/
├── docs/                            # Comprehensive documentation suite
│   ├── README.md
│   ├── 01-research-and-benchmarks.md
│   ├── 02-architecture-and-design.md
│   ├── 03-stack-profiles.md
│   ├── 04-workflows-and-skills-catalog.md
│   └── 05-roadmap-and-implementation.md
├── templates/                       # Modular AI configurations & skills
│   ├── common/                      # AGENTS.md, CLAUDE.md, copilot
│   ├── stacks/                      # Next.js, NestJS, React Native, Monorepo
│   ├── workflows/                   # Plan/Execute, TDD, Git/PR, Security
│   └── skills/                      # Progressive SKILL.md runbooks
├── bin/                             # CLI entrypoints (Node CLI & shell runner)
├── src/                             # Scaffolder, detector, compiler, and CLI wizard
└── README.md
```

---

## 📄 License

MIT

