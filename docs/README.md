# ai-assist-bootstrap Documentation

Welcome to the documentation for **ai-assist-bootstrap**, a modular project generator and configuration engine designed to bootstrap modern applications with production-ready AI agent skills, rules, workflows, and tool configurations.

---

## 📚 Documentation Index

1. **[01. Research & Benchmarks](./01-research-and-benchmarks.md)**
   Comprehensive survey and analysis of existing AI agent templates, rule repositories, and skill libraries (Claude Code templates, Cursor rules, awesome-agent-skills, superpowers, etc.), analyzing their strengths, weaknesses, and key architectural lessons.

2. **[02. Architecture & System Design](./02-architecture-and-design.md)**
   Detailed design of the bootstrapping engine: Progressive Disclosure principle, Single-Source-of-Truth (SSOT) compilation model, multi-agent export strategy (`AGENTS.md`, `.cursor/rules`, `.claude/`, `.agents/skills`, Copilot), and dual-mode (`create` vs `retrofit`).

3. **[03. Stack Profiles](./03-stack-profiles.md)**
   Specifications, coding invariants, rule sets, and recommended skills for each supported project stack:
   - Next.js (Fullstack / React 19 / App Router)
   - NestJS (Enterprise Backend / TypeScript)
   - React Native & Expo (Cross-Platform Mobile)
   - Turborepo Monorepo (Multi-app / Shared packages)

4. **[04. Workflows & Skills Catalog](./04-workflows-and-skills-catalog.md)**
   In-depth specifications for core orchestration workflows (`plan-execute-verify`, `tdd-workflow`, `git-conventions-pr`, `security-guardrails`, `spec-driven-development` via Spec Kit, and `gsd-context-reset` via Get Shit Done) and catalog of stack-specific agent skills adhering to the open `SKILL.md` progressive disclosure standard.

5. **[05. Roadmap & Implementation Plan](./05-roadmap-and-implementation.md)**
   Implementation blueprints, project structure, CLI technology options (Node/TS vs Shell vs Hybrid), phase-by-phase milestones, and testing strategy.

---

## 🎯 High-Level Vision

```
+-------------------------------------------------------------------------+
|                          ai-assist-bootstrap                            |
+-------------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
   [ Project Scaffolder ]                             [ AI Engine ]
   * Next.js (App Router)                             * Rules (Scoped .mdc, AGENTS.md)
   * NestJS (Modular API)                             * Skills (Progressive SKILL.md)
   * React Native (Expo)                              * Workflows (Plan/Execute, TDD)
   * Monorepo (Turborepo + pnpm)                      * Tools & MCP (Databases, GitHub)
         |                                                   |
         +-------------------------+-------------------------+
                                   |
                                   v
             [ Ready-to-Code Production Repository ]
         Supported by Claude Code, Cursor, Antigravity,
                 Windsurf, Copilot, & Gemini CLI
```

