# 09. MCP Servers & Tool Integrations

This document defines how `ai-assist-bootstrap` configures, scaffolds, and manages **Model Context Protocol (MCP)** tool servers across Claude Code, Cursor, Antigravity, and Windsurf.

---

## 1. Why MCP Servers Matter for Coding Agents

Traditional LLMs only see the static text files in their prompt. With **MCP (Model Context Protocol)**, agents gain dynamic execution powers:
* **Live Database Inspection**: Query tables, inspect schemas, and verify migrations directly (PostgreSQL, SQLite, Prisma MCP) instead of guessing.
* **Browser & UI Verification**: Launch headless browsers (Playwright MCP) to test rendered components, visual layouts, and network requests.
* **Live Documentation**: Fetch version-exact framework documentation (Context7 MCP) to prevent hallucinated API methods.
* **Repository Automation**: Create PRs, review issues, and trigger CI runs (GitHub MCP).

---

## 2. Multi-Agent MCP Configuration Mapping

Different AI tools place their MCP configurations in different paths. `ai-assist-bootstrap` generates and synchronizes them from a single source:

| AI Tool                      | Project-Level Config Path      | Global Config Path                    |
| :--------------------------- | :----------------------------- | :------------------------------------ |
| **Cursor**                   | `<project>/.cursor/mcp.json`   | `~/.cursor/mcp.json`                  |
| **Claude Code**              | `<project>/.claude/mcp.json`   | `~/.claude/settings.json`             |
| **Antigravity / Gemini CLI** | `<project>/mcp_config.json`    | `~/.gemini/config/mcp_config.json`    |
| **Windsurf**                 | `<project>/.windsurf/mcp.json` | `~/.codeium/windsurf/mcp_config.json` |

---

## 3. Curated Stack-Specific MCP Presets

When bootstrapping a stack, `ai-assist-bootstrap` includes tailored MCP configurations:

### 1. Database Inspection MCP (for NestJS, Python, Go, Rust)
Enables the agent to inspect table schemas, column types, and test queries safely in read-only mode:

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### 2. Browser & UI Testing MCP (for Next.js, React SPA)
Enables the agent to take screenshots, run Playwright E2E tests, and inspect console logs:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    }
  }
}
```

### 3. Documentation MCP (Context7 - Universal)
Fetches live, version-specific documentation for React 19, Next.js 15, FastAPI, Axum, etc.:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "context7-mcp-server"]
    }
  }
}
```

### 4. GitHub MCP (Universal)
Enables automated PR drafting, issue linking, and commit verification:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

---

## 4. Security & Credential Isolation

To prevent exposing database credentials or API keys to git:
1. **Environment Variable Injection**: Config files use `${ENV_VAR}` interpolations; keys are NEVER hardcoded into `mcp.json`.
2. **Read-Only Guards**: Database MCP servers default to read-only database user credentials.
3. **Secret Scan Gate**: Checked by Tier 2 pre-commit hooks (`gitleaks`) to ensure `mcp.json` never commits plain text secrets.

---

## 5. Self-Bootstrapping: `ai-assist mcp-server` vs. On-Demand Skills

When an AI agent is tasked with setting up or retrofitting a complicated repository, a common architectural question arises: **Should `ai-assist-bootstrap` expose its own MCP server to guide the agent, or rely on an on-demand Skill / Workflow?**

### The Architectural Trade-Off

| Feature                | MCP Server (`ai-assist mcp-server`)                                                                                             | On-Demand Skill (`retrofit-assistant`)                                                                        |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------ |
| **Role**               | **Infrastructure & Tooling Layer** (The "Hands")                                                                                | **Reasoning & Methodology Layer** (The "Brain")                                                               |
| **Setup Friction**     | ❌ **High ("Chicken-and-Egg")**: The user/agent must configure and launch an MCP server *before* their codebase is bootstrapped. | ✅ **Zero**: Plain Markdown file. Any agent reads it instantly via progressive disclosure.                     |
| **Context Overhead**   | ⚠️ Tool schemas sit in prompt on every turn (~200 tokens).                                                                       | ✅ **Zero baseline**: Loaded strictly on-demand when the retrofit task begins.                                 |
| **Handling Ambiguity** | ❌ Tools return structured data/errors; cannot navigate polyglot trade-offs or interview users.                                  | ✅ **Superior**: Instructs the agent on how to inspect ASTs, resolve conflicting libraries, and ask questions. |
| **Execution Safety**   | ✅ Structured typed JSON-RPC parameters.                                                                                         | ⚠️ Agent executes bash commands (`./bin/ai-assist`) or modifies files directly.                                |

### The Hybrid Solution: "Skill as the Brain, CLI/MCP as the Hands"

1. **The Brain (On-Demand Skill & Workflow)**:
   - Provide [`templates/skills/retrofit-assistant/SKILL.md`](../templates/skills/retrofit-assistant/SKILL.md) and [`templates/workflows/brownfield-retrofit.md`](../templates/workflows/brownfield-retrofit.md).
   - The skill is **never preloaded permanently** in `AGENTS.md` (which would violate the <80-line context budget). It triggers on-demand when the agent is asked to analyze or retrofit the repo.
   - It guides the agent through 4 phases: Reconnaissance $\to$ Developer Interview $\to$ SSOT Synthesis $\to$ Doctor Audit.

2. **The Hands (CLI & MCP Tool Layer)**:
   - In standard environments (Antigravity, Claude Code, Cursor with terminal), the agent executes `./bin/ai-assist` commands.
   - For sandboxed IDEs or agents lacking terminal execution privileges, `ai-assist` exposes an optional `ai-assist mcp-server` providing:
     - `ai_assist_list_stacks()`: Returns supported stack profiles and invariants.
     - `ai_assist_get_template(stack_id)`: Fetches stack configuration templates.
     - `ai_assist_search_skills(query)`: Finds relevant on-demand `SKILL.md` runbooks.
     - `ai_assist_compile(config)`: Programmatically compiles files.
     - `ai_assist_doctor(project_dir)`: Runs diagnostics on generated configs.


