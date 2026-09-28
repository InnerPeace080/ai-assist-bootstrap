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
  * Pre-configured slash commands, subagents, and hooks.
  * Built-in MCP (Model Context Protocol) servers.
  * Automated GitHub Workflows for `@claude` mentions in issues and pull requests, plus automated PR review.
  * **Egress Firewall**: Network sandbox restricting outbound connections to an explicit allowlist.
* **Pros**: High security posture, complete automation from local terminal to CI/CD.
* **Cons**: Monolithic, highly opinionated towards Claude Code; difficult to adapt to other AI tools or lightweight projects.

#### 2. `MuhammadUsmanGM/claude-code-best-practices`

* **Repository**: [MuhammadUsmanGM/claude-code-best-practices](https://github.com/MuhammadUsmanGM/claude-code-best-practices)
* **Overview**: Practical, lean whole-project starter kits pairing a concise `CLAUDE.md` with `.claude/` settings, skills, and hooks.
* **Key Features**:
  * 5 complete starter kits: **React**, **Next.js**, **Python**, **Go**, and **Rust**.
  * 11 focused `CLAUDE.md` templates tailored to specific project types.
  * Maintained with clean, non-bloated rules.
* **Pros**: High signal-to-noise ratio, respects context limits, clear separation by programming language.
* **Cons**: Primarily designed for manual copying, lacks an automated multi-agent synchronization layer.

#### 3. `creatyvin/project-template`

* **Repository**: [creatyvin/project-template](https://github.com/creatyvin/project-template)
* **Overview**: Multi-tool cross-compatibility template.
* **Key Features**:
  * Leverages `AGENTS.md` as the universal specification across Claude, GitHub Copilot, Cursor, OpenAI Codex, Devin, and Gemini CLI.
  * Includes `.cursor/rules/` and Copilot instruction bridges.
* **Pros**: Neutral, doesn't lock the team into a single AI client.
* **Cons**: Shallow skill definitions; lacks deep stack-specific architectural guidance and complex workflows.

#### 4. `versoxbt/claude-initial-setup`

* **Repository**: [versoxbt/claude-initial-setup](https://github.com/versoxbt/claude-initial-setup)
* **Overview**: Massive "batteries-included" setup.
* **Key Features**:
  * 75 skills, 14 subagents, 15 slash commands, 8 rules, and 6 hooks.
  * Exporters to translate setups into Cursor, Copilot, and Codex formats.
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

### D. Spec-Driven & Context-Engineering Frameworks

#### 1. `github/spec-kit` (Spec Kit / `specify-cli`)

* **Repository**: [github/spec-kit](https://github.com/github/spec-kit)
* **Core Philosophy**: **Spec-Driven Development (SDD)** — eliminating "vibe coding" by anchoring agent actions to formal, persistent specifications.
* **The 5-Phase Workflow**:
  $$\text{Constitution} \longrightarrow \text{Specify (What/Why)} \longrightarrow \text{Plan (Architecture)} \longrightarrow \text{Tasks (Checklist)} \longrightarrow \text{Implement \& Converge}$$
* **Key Innovations**:
  * **`.specify/` Directory**: Version-controlled specifications, requirements, and acceptance criteria live directly in the repo.
  * **Constitution**: Codifies non-negotiable architectural principles (e.g., "Must use strict TypeScript", "No external telemetry without approval") before any code or feature is designed.
  * **Convergence Verification**: Post-implementation verification comparing the generated code against the original spec to prevent feature drift.
  * **Broad Agent Compatibility**: Works across 30+ AI agents (Claude Code, Cursor, GitHub Copilot, Gemini CLI, Amazon Q).
* **Takeaway for `ai-assist-bootstrap`**: Provide native compatibility with Spec-Driven Development (SDD) templates, enabling teams to scaffold `.specify/` constitutions and spec templates.

#### 2. Get Shit Done (`GSD` / `open-gsd`)

* **Repository**: [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core) (formerly `get-shit-done-cc`)
* **Core Philosophy**: **Combating "Context Rot"** through Meta-Prompting and Fresh Subagent Execution.
* **The Problem It Solves**: In long chat sessions, the LLM context window fills with obsolete tool calls, conversational chatter, and stale diffs. The model becomes sluggish, repeats mistakes, and forgets core constraints.
* **Key Innovations**:
  * **Fresh Context per Task**: Instead of executing all steps in one monolithic conversation, GSD spins up clean, isolated subagent contexts for each discrete task.
  * **Persistent State Tracking**: Maintains high-level state in lightweight repository files (`STATE.md`, `ROADMAP.md`), allowing fresh agents to instantly orient themselves without dragging along hundreds of previous chat turns.
  * **Phased Lifecycle**: `Discuss` → `Plan` → `Execute (Fresh Context)` → `Verify` → `Ship`.
* **Takeaway for `ai-assist-bootstrap`**: Incorporate GSD's context-reset philosophy into our workflow runner. When tackling multi-step feature implementation, isolate subtasks into clean subagent contexts rather than polluting a single session.

#### 3. `bmad-code-org/BMAD-METHOD` (Agile AI-Driven Development)

* **Repository**: [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
* **Core Philosophy**: **"Agents as Code" & Persona-Based Agile Simulation**.
* **Key Innovations**:
  * Defines specialized agile personas (Product Manager, Solution Architect, Lead Developer, QA / Test Architect TEA) in YAML/Markdown config.
  * **BMad Loop**: Automated execution loop that drives an agent through user stories, code generation, testing, and atomic git commits.
  * Multi-phase structured development: Analysis → Planning → Solutioning → Implementation.
* **Takeaway for `ai-assist-bootstrap`**: Provide persona-based role definitions in our subagent directory (`.claude/agents/`, `.agents/`) tailored to stack tasks (e.g. Architect, DB Specialist, Security Reviewer).

#### 4. `github/agentic-workflows` (`gh-aw` / GitHub Next)

* **Official Project**: Native GitHub Actions AI automation
* **Core Philosophy**: **Repository-Native CI/CD AI Orchestration**.
* **Key Innovations**:
  * Defined in simple Markdown files combining YAML frontmatter (triggers, tools, permissions) with natural language prompts.
  * Compiled into deterministic `.lock.yml` GitHub Actions workflows using the `gh-aw` CLI.
  * Enforces **"Safe-Outputs"**: Agents propose changes (PRs, issues, comments) with human-in-the-loop review rather than having unrestricted repo push permissions.
* **Takeaway for `ai-assist-bootstrap`**: Generate ready-to-use GitHub Actions agentic workflows for automated PR reviews, dependency audits, and issue triage.

---

### E. Multi-IDE Rule Managers & Context Compressing Tools

#### 1. `he-yufeng/RuleForge` & `tecnomanu/agent-rules-kit`

* **Repositories**: [he-yufeng/RuleForge](https://github.com/he-yufeng/RuleForge), [tecnomanu/agent-rules-kit](https://github.com/tecnomanu/agent-rules-kit)
* **Core Function**: Codebase scanners that detect project dependencies and generate synchronized rules across **Cursor**, **Claude Code**, **Copilot**, **Windsurf**, **Cline**, **Gemini**, and **Aider**.
* **Takeaway**: Confirms high community demand for cross-IDE synchronization. However, these tools are rule-only; they do not scaffold application code or provide structured skill runbooks.

#### 2. `yamadashy/repomix` (Context Packing & Compression)

* **Repository**: [yamadashy/repomix](https://github.com/yamadashy/repomix)
* **Core Function**: Converts entire repositories into AI-friendly, token-efficient context representations (XML/Markdown/JSON).
* **Key Features**: Tree-sitter code compression (`--compress`), secret redaction via Secretlint, and native Model Context Protocol (MCP) server support.
* **Takeaway**: Include Repomix configuration presets in bootstrapped projects so agents can quickly inspect whole-repo context without manual copy-pasting.

#### 3. `trailofbits/claude-code-config`

* **Repository**: [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)
* **Core Function**: Production-grade, security-focused configuration maintained by Trail of Bits.
* **Key Features**: Hardened verification harnesses, defensive coding guidelines, automated security audits, and strict tool-usage boundaries.
* **Takeaway**: Incorporate Trail of Bits security invariant patterns into our `security-guardrails` workflow and baseline rules.

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

5. **Spec-Driven Discipline (from Spec Kit)**:
   * "Vibe coding" leads to technical debt and missed requirements.
   * By providing versionable specification templates (`CONSTITUTION.md`, `.specify/`), the agent always has clear, immutable acceptance criteria and architectural non-negotiables before it writes code.

6. **Combat "Context Rot" via Fresh Subagent Contexts (from GSD)**:
   * Monolithic, long-running agent chats inevitably decay in reasoning quality.
   * Workflows should encourage decomposing tasks into discrete phases, resetting context or using fresh subagent invocations, and recording persistent milestones in state files (`STATE.md`, `ROADMAP.md`).

---

## 5. Research Benchmark: Agent Fleet Frameworks & Worktree Orchestrators

As AI engineering workflows scale, single-agent architectures are being superseded by **Agent Fleets** executing tasks in parallel. Below is an analysis of leading industry implementations, frameworks, and isolation primitives:

### 1. Claude Code Agent Teams & `TeammateTool` / `--worktree` (Anthropic)
* **Architecture**: A hierarchical Team Lead agent coordinates specialized Teammates (Frontend, Backend, QA, Docs).
* **Isolation**: Supported natively via `claude --worktree <name>`, provisioning isolated directories (`.claude/worktrees/<name>/`) and dedicated Git branches sharing the root object store.
* **Coordination Primitives**: 13 internal lifecycle operations in `TeammateTool` (spawning, joining, shared task list, plan approval/rejection, direct & broadcast messaging).
* **Key Takeaway for `ai-assist-bootstrap`**: Generate standard Team Lead and Teammate prompt profiles, plus automated worktree bootstrap hooks so teams can launch with zero setup friction.

### 2. `ccswarm` (Open-Source Rust Worktree Orchestrator)
* **Architecture**: A Rust-based orchestration daemon governing specialized agent pools (Frontend, Backend, DevOps, QA) using strict Git worktree isolation.
* **Core Philosophy**: **"Sangha" Product Core**—shared acceptance criteria, evidence-backed objections, and recorded architectural decisions before merging.
* **Key Takeaway for `ai-assist-bootstrap`**: Adopt the "One Task, One Branch, One Worktree" discipline and evidence-backed objection gates in our multi-agent workflows.

### 3. Google Antigravity Subagent System
* **Architecture**: Dynamic subagent invocation (`invoke_subagent`) with first-class workspace virtualization (`Workspace: 'inherit' | 'branch' | 'share'`).
* **Isolation**: `'share'` creates a shared repository worktree directory, while `'branch'` provisions an isolated branch workspace.
* **Coordination Primitives**: Reactive wakeup messaging (`send_message`), lifecycle governance (`manage_subagents`: `list`, `kill`, `kill_all`), and one-shot liveness timers (`schedule`).
* **Key Takeaway for `ai-assist-bootstrap`**: Support native declarative workspace mapping (`Workspace: 'share'`) in generated subagent configs.

### 4. OpenHands & SWE-agent (All-Hands AI)
* **Architecture**: Autonomous coding agents operating over abstracted `LocalWorkspace` and `DockerWorkspace` environments.
* **Multi-Agent Isolation**: Parallel agents operate in dedicated `git worktree` checkouts to prevent file race conditions and `git checkout` index lockups.
* **Key Takeaway for `ai-assist-bootstrap`**: Explicitly enforce the rule that parallel agents must never execute `git checkout` or `git switch` across worktrees; all branch binding must happen during worktree provisioning.

### 5. Multi-Agent Fleet Comparison Matrix

| Framework / Tool          | Isolation Primitive         | Topology                                                 | Communication                                    | Conflict Resolution                                         |
| :------------------------ | :-------------------------- | :------------------------------------------------------- | :----------------------------------------------- | :---------------------------------------------------------- |
| **Claude Code Teams**     | `.claude/worktrees/*`       | Lead + Teammates                                         | Shared Task List + Direct/Broadcast Messaging    | Lead Review + Manual Merge                                  |
| **ccswarm**               | Git Worktrees               | Pool of Specialists                                      | File Event Bus & Sangha Objections               | Evidence-backed verification gate                           |
| **Google Antigravity**    | `branch` / `share` Worktree | Parent + Subagent Fleet                                  | Reactive Wakeup (`send_message`)                 | Parent Synthesis & Commit Gate                              |
| **OpenHands / SWE-agent** | Worktrees + Docker          | Planner + Worker Agents                                  | Workspace Event Bus                              | Automated Test Suite Gate                                   |
| **`ai-assist-bootstrap`** | **SSOT Worktree Manager**   | **Coordinator + Worker Fleet + Gatekeeper + Integrator** | **`.fleet/` Contracts & Reactive Event Signals** | **Sequential Rebase Pipeline + Conflict Resolver Subagent** |

---

## 6. Programmatic Multi-Agent Frameworks: CrewAI, LangGraph, AutoGen, Swarms & Ray

In addition to developer-facing CLI tools (Claude Code, Antigravity, Cursor), the broader AI ecosystem provides programmatic frameworks for building custom multi-agent orchestration engines. When deploying agent fleets for automated software engineering (SWE), these frameworks serve as potential execution drivers:

| Library / Tool    | Primary Model           | Manager Mechanism                        | Best Use Case                                                       | Fit for SWE Agent Fleets                                                                                  |
| :---------------- | :---------------------- | :--------------------------------------- | :------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------- |
| **LangGraph**     | Directed graphs & state | Supervisor node / State routing          | Production workflows needing deterministic control & custom routing | ⭐ **Highest**: Cyclic graph state machine fits `plan-execute-verify` and rebase loops perfectly.          |
| **CrewAI**        | Role-based teams        | Built-in `manager_llm` / `manager_agent` | Rapid prototyping of goal-driven agent squads                       | **High**: Role specialization (Coder, Reviewer, QA) is natural, but requires external worktree isolation. |
| **AutoGen (AG2)** | Conversational agents   | `GroupChatManager` / Selector            | Collaborative reasoning, debate, and multi-turn negotiation         | **Medium-High**: Ideal for Gatekeeper-Coder debate rounds and multi-agent consensus before commits.       |
| **Swarms**        | Topologies & DSLs       | `HierarchicalSwarm` / Flow DSL           | High-throughput concurrent agent pipelines                          | **Medium**: Good for fan-out worker pools, requires custom git and file isolation hooks.                  |
| **Ray**           | Distributed Actors      | Master actor / Queue scheduler           | High-scale parallel agent fleets spanning multiple nodes/GPUs       | **Enterprise Scale**: Indispensable for running 50+ parallel SWE-bench instances across cluster workers.  |

### The Critical Gap: Filesystem & Git Governance
While frameworks like LangGraph and CrewAI provide powerful routing and conversation state machines, **they are agnostic to filesystem concurrency and Git mechanics**. When multiple agents execute terminal commands or edit code simultaneously:
1. They risk corrupting the single `.git/index.lock`.
2. They overwrite uncommitted changes across parallel tasks.
3. They fail to handle branch rebase conflicts automatically.

**The Role of `ai-assist-bootstrap`**:
`ai-assist-bootstrap` provides the missing repository-level substrate for these frameworks: the **"One Task, One Branch, One Worktree"** lifecycle, standard task contracts (`.fleet/queue/*.json`), scoped Cursor/Antigravity rules, and deterministic quality gates.


