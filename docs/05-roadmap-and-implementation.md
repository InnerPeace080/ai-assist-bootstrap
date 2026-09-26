# 05. Roadmap & Implementation Plan

This document outlines the implementation strategy, technology evaluation for the CLI engine, repository layout, and phased execution milestones for **`ai-assist-bootstrap`**.

---

## 1. CLI Engine Evaluation

We evaluated three potential implementation approaches for the `ai-assist-bootstrap` CLI tool:

| Dimension             | Option A: Node.js / TypeScript CLI                        | Option B: Pure Bash / Shell Script         | Option C: Hybrid Architecture                 |
| :-------------------- | :-------------------------------------------------------- | :----------------------------------------- | :-------------------------------------------- |
| **Execution Command** | `npx ai-assist-bootstrap`                                 | `./bootstrap.sh` or `curl ... \| bash`     | `./bootstrap.sh` launching Node or fallback   |
| **Cross-Platform**    | Linux, macOS, Windows (native)                            | Linux, macOS, WSL                          | Linux, macOS, WSL, Windows                    |
| **Interactive UX**    | Rich terminal UI (`@clack/prompts`, colors, multi-select) | Text-based prompt menus (`select`, `read`) | Rich UI via Node if available, shell fallback |
| **Templating Engine** | Fast, flexible (Handlebars, EJS, or JS template literals) | Variable substitution (`sed`, `envsubst`)  | Robust templating engine                      |
| **Dependencies**      | Requires Node runtime                                     | Zero dependencies beyond Bash & Git        | Graceful progressive enhancement              |
| **Verdict**           | ⭐ **Recommended for Production**                          | Great for initial zero-dep launcher        | Excellent for universal distribution          |

### Recommended Implementation Strategy:
* **Core Generator**: Built with **TypeScript / Node.js** (or standalone runnable via `npx` / Bun).
* **Zero-Dep Shell Wrapper**: A lightweight `bootstrap.sh` script at the root that checks for Node/pnpm and provides a single one-line installation (`curl -fsSL https://... | bash`).

---

## 2. Target Repository Directory Structure

```
ai-assist-bootstrap/
├── bin/
│   ├── ai-assist.js                 # Executable Node CLI entrypoint
│   └── bootstrap.sh                 # Zero-dependency Shell wrapper
├── docs/                            # Complete documentation & specifications
│   ├── README.md
│   ├── 01-research-and-benchmarks.md
│   ├── 02-architecture-and-design.md
│   ├── 03-stack-profiles.md
│   ├── 04-workflows-and-skills-catalog.md
│   └── 05-roadmap-and-implementation.md
├── templates/
│   ├── common/                      # Baseline multi-agent configs
│   │   ├── AGENTS.md.tpl
│   │   ├── CLAUDE.md.tpl
│   │   ├── copilot-instructions.md.tpl
│   │   └── mcp_config.json.tpl
│   ├── stacks/                      # Stack-specific rule sets
│   │   ├── nextjs/
│   │   │   └── cursor-rules/
│   │   ├── nestjs/
│   │   │   └── cursor-rules/
│   │   ├── react-native/
│   │   │   └── cursor-rules/
│   │   └── monorepo/
│   │       └── cursor-rules/
│   ├── workflows/                   # Core agent workflows
│   │   ├── plan-execute-verify.md
│   │   ├── tdd-workflow.md
│   │   ├── git-conventions-pr.md
│   │   └── security-guardrails.md
│   └── skills/                      # Progressive disclosure skills (SKILL.md)
│       ├── nextjs-app-router/SKILL.md
│       ├── tailwind-shadcn/SKILL.md
│       ├── nestjs-module-architect/SKILL.md
│       ├── db-prisma-migration/SKILL.md
│       ├── expo-router/SKILL.md
│       ├── mobile-perf-tuning/SKILL.md
│       ├── api-testing/SKILL.md
│       └── security-audit/SKILL.md
├── src/
│   ├── index.ts                     # CLI program setup (Commander.js)
│   ├── prompt.ts                    # Interactive terminal wizard
│   ├── detector.ts                  # Auto-detector for existing projects
│   ├── compiler.ts                  # Template compiler & SSOT generator
│   └── scaffolder.ts                # Executes package manager / create-* commands
├── package.json
├── tsconfig.json
└── README.md
```

---

## 3. Phased Implementation Milestones

```mermaid
flowchart LR
    P1["Phase 1: Docs & Research"]
    P2["Phase 2: Templates & Skills"]
    P3["Phase 3: Compiler & Scaffolder"]
    P4["Phase 4: CLI Wizard & Retrofit"]
    P5["Phase 5: Verification & Testing"]

    P1 --> P2 --> P3 --> P4 --> P5
```

### Phase 1: Research, Architecture & Documentation (Completed)
- [x] Synthesize ecosystem research and competitive benchmarks.
- [x] Formulate the Progressive Disclosure & SSOT architectural model.
- [x] Author comprehensive documentation suite in `docs/`.

### Phase 2: Template & Skill Catalog Creation
- [ ] Implement canonical templates in `templates/common/` (`AGENTS.md`, `CLAUDE.md`, Copilot instructions).
- [ ] Implement scoped Cursor rules (`.mdc`) for Next.js, NestJS, React Native, and Monorepo.
- [ ] Author the 8 curated `SKILL.md` runbooks with progressive disclosure frontmatter.
- [ ] Create the standard workflow definitions (`plan-execute-verify`, `tdd-workflow`, etc.).

### Phase 3: Compiler & Scaffolding Engine
- [ ] Implement the template compiler to render target agent configurations based on selected stacks.
- [ ] Integrate stack scaffolders (`create-next-app`, `@nestjs/cli`, `create-expo-app`, `create-turbo`).
- [ ] Generate the `ai-assist.json` manifest.

### Phase 4: Interactive CLI Wizard & Retrofit Mode
- [ ] Build the interactive terminal prompt wizard (stack, tools, workflows, skills selection).
- [ ] Implement `detector.ts` to inspect existing repositories and support `ai-assist-bootstrap add` mode.
- [ ] Add the zero-dependency `bootstrap.sh` launcher script.

### Phase 5: Verification & End-to-End Testing
- [ ] Test bootstrapping fresh Next.js, NestJS, Expo, and Turborepo projects.
- [ ] Verify generated AI configurations in Claude Code, Cursor, Antigravity, and Copilot environments.
- [ ] Benchmark context token consumption to verify the Progressive Disclosure budget (< 500 tokens at baseline).

