# 07. Bidirectional Sync & Personal Overrides

This document defines how `ai-assist-bootstrap` handles the continuous evolution of AI rules and skills, enabling developers to merge upstream updates with personal preferences, and **extract project-refined rules back into a central library**.

---

## 1. The Core Problem: Rule & Skill Drift

In real-world development:
1. **Upstream Evolution**: Upstream best practices, stack rules, and CLI tools improve continuously (e.g. Next.js 16 updates, new linter flags, security patches).
2. **Local Customization**: Developers refine rules and skills *inside their working project* (adding project-specific business rules, fixing agent anti-patterns, creating custom skills).
3. **The Danger of Overwriting**: If a tool simply copies new templates over existing files, all manual personal customizations are lost.
4. **The "Silo" Problem**: A brilliant skill written while solving a tough problem in `project-A` stays trapped in `project-A` instead of being reusable across future projects.

---

## 2. The 3-Tier Layered Configuration Hierarchy

`ai-assist-bootstrap` resolves conflicts by separating rules into three distinct layers:

```
+───────────────────────────────────────────────────────────────────────────+
| Layer 3: Project-Specific Overrides (Highest Priority)                    |
| Location: <project-root>/.cursor/rules/, AGENTS.md, .claude/              |
| Scope: Current repository only. Codifies domain logic & project nuance.   |
+───────────────────────────────────────────────────────────────────────────+
                                     │ Overrides
                                     ▼
+───────────────────────────────────────────────────────────────────────────+
| Layer 2: User Personal Global Layer (Medium Priority)                     |
| Location: ~/.ai-assist/ (or ~/.config/ai-assist/)                         |
| Scope: All projects on developer's machine. Contains personal preferences |
| (favorite linters, prompt tone, personal skills library).                 |
+───────────────────────────────────────────────────────────────────────────+
                                     │ Overrides
                                     ▼
+───────────────────────────────────────────────────────────────────────────+
| Layer 1: Upstream Recommended Presets (Base Layer)                        |
| Location: ai-assist-bootstrap official templates / registry               |
| Scope: Battle-tested community standards for Next.js, Go, Rust, etc.      |
+───────────────────────────────────────────────────────────────────────────+
```

---

## 3. Downstream Updates: 3-Way Merge (The Copier/Cruft Model)

When you run `ai-assist-bootstrap update`, the tool does **NOT** blindly overwrite files. It executes an automated **3-Way Git Merge** inspired by `copier` and `cruft`:

```
               [ BASE ]
        (Original template state
         recorded at init/manifest)
                 /    \
                /      \
      [ UPSTREAM ]    [ LOCAL ]
    (New template      (Your modified working
     from registry)     project with personal edits)
                \      /
                 \    /
               [ 3-WAY MERGE ]
         (Preserves personal edits +
          incorporates upstream improvements)
```

### How It Works:
1. **Manifest Tracking**: When a project is bootstrapped, `ai-assist.json` records the template version and checksums:
   ```json
   {
     "templateVersion": "1.2.0",
     "templateCommit": "a1b2c3d",
     "profile": "nextjs"
   }
   ```
2. **Diff Calculation**:
   - Calculates $\Delta_1$: What changed between `BASE` and `UPSTREAM`.
   - Calculates $\Delta_2$: What changed between `BASE` and `LOCAL` (user customizations).
3. **Smart Reconciliation**:
   - Automatically merges non-conflicting sections.
   - If a direct conflict occurs (e.g. both modified the same rule line), standard conflict markers (`<<<<<<< LOCAL ... >>>>>>> UPSTREAM`) or `.rej` files are presented with an interactive resolution CLI.

---

## 4. The "Update-Back" Loop: Extracting Rules from Working Projects

To bring rules, skills, or workflows developed inside a working project back into your reusable personal library OR directly into the central **`ai-assist-bootstrap` Git repository**:

```
                                  [ Working Project ]
                                           │
                         ┌─────────────────┴─────────────────┐
                         ▼                                   ▼
             [ Destination 1: Personal ]         [ Destination 2: Git Repo ]
             Saved to `~/.ai-assist/skills/`     Pushed to `ai-assist-bootstrap`
             (Available on your machine)         (Available across all devices/team)
```

---

### Upstream Git Repository Configuration

In `ai-assist.json` (or your global `~/.ai-assist/config.json`), configure your upstream Git repository settings:

```json
{
  "upstream": {
    "gitRemote": "git@github.com:innerpeace080/ai-assist-bootstrap.git",
    "localRepoPath": "/media/Data/Codes/shell/ai-assist-bootstrap",
    "defaultBranch": "main"
  }
}
```

---

### CLI Commands for Upstream Extraction:

#### 1. Exporting Back to Central Git Repository (`--to-git`)

If you have write access to the central `ai-assist-bootstrap` repository (or want to submit a PR), use the `--to-git` flag:

```bash
# 1. Direct Commit & Push (when you have repo access)
ai-assist-bootstrap export-back payment-webhook-handler --to-git --push
# Action: Commits to templates/skills/payment-webhook-handler/ in the Git repo
# Commit message: feat(skills): update payment-webhook-handler from my-project

# 2. Pull Request Workflow (via GitHub CLI `gh`)
ai-assist-bootstrap export-back server-actions-rule --to-git --pr
# Action: Creates branch 'update/server-actions', pushes, and runs `gh pr create`

# 3. Local Linked Repo Shortcut (Instant Dev)
ai-assist-bootstrap export-back my-new-skill --to-local-repo /media/Data/Codes/shell/ai-assist-bootstrap
# Action: Directly copies files into the local template directory for inspection
```

#### 2. Exporting to Local Personal Library (`~/.ai-assist/`)
For machine-local personal preferences that don't belong in the central repository:
```bash
ai-assist-bootstrap export-back custom-db-helper
# Saved to ~/.ai-assist/skills/custom-db-helper/SKILL.md
```

#### 3. Inspecting Differences (`ai-assist-bootstrap diff`)
Displays a colored diff showing how your current project's rules differ from the base upstream repository:
```bash
ai-assist-bootstrap diff --upstream
# Output:
# [MODIFIED] .cursor/rules/nextjs.mdc (+14 lines personal query invalidations)
# [NEW SKILL] .agents/skills/stripe-webhooks/SKILL.md (not yet upstreamed)
```

#### 4. Snapshoting a Complete Preset (`save-preset`)
Saves the entire combination of stack rules, check gates, and skills as a named reusable preset:
```bash
# Save locally
ai-assist-bootstrap save-preset my-fintech-stack

# Save directly to the upstream Git repo as an official stack preset
ai-assist-bootstrap save-preset my-fintech-stack --to-git --push
```

---

### Safety & Secret Sanitization Guardrail

Before any rule or skill is pushed back to the Git repository, `ai-assist-bootstrap` automatically executes a **pre-export sanitization audit**:
* Scans for project-specific secrets, company domain names, private API keys, and internal IP addresses.
* Prompts the developer: *"Found company name 'AcmeCorp' in rule text. Replace with generic placeholder before pushing to public Git? (Y/n)"*
* Ensures the central Git template library stays pristine and generic.


---

## 5. Automated Agent Learning (`/learn` Hook)

When an AI agent solves a complex bug or is corrected by the developer during a coding session, it shouldn't forget that lesson on the next session.

1. Developer triggers: `/learn "Always run rebar3 dialyzer before closing Erlang PRs"`
2. The agent analyzes the rule:
   - If it's **project-specific**: Appends it to `<project-root>/AGENTS.md` under `# Project Learnings`.
   - If it's a **personal global habit**: Uses `ai-assist-bootstrap` to append to `~/.ai-assist/global-rules.md`.
3. The next time `ai-assist-bootstrap update` runs, this rule is preserved through the 3-way merge model.

