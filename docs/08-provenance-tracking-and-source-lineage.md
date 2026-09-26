# 08. Provenance Tracking & Source Lineage

This document specifies the **Source Lineage & Provenance Tracking** system for `ai-assist-bootstrap`. When pulling, curating, and adapting rules, skills, and workflows from community repositories, this system tracks exact origins, licenses, upstream commit hashes, and personal modifications.

---

## 1. Why Provenance Tracking is Essential

In an ecosystem where thousands of skills and rules are contributed by communities (`awesome-cursorrules`, `anthropics/skills`, `VoltAgent`, `trailofbits`, `spec-kit`):
1. **Attribution & Licensing**: Open-source rules and skills have licenses (MIT, Apache-2.0, BSD). We must maintain proper attribution.
2. **Upstream Drift Detection**: When the original author improves a community skill, you need to know *what changed upstream* without losing your personal tweaks.
3. **Clarity on Ownership**: Distinguish at a glance between:
   - **Pure Upstream**: Copied directly from community with zero modifications.
   - **Forked & Customized**: Community base, but enhanced with your personal project patterns.
   - **Personal Original**: Crafted entirely by you from scratch.

---

## 2. In-File Provenance Frontmatter (`SKILL.md` & `.mdc`)

Every skill and rule file tracks its lineage directly in its YAML frontmatter header conforming to the open `SKILL.md` specification:

```yaml
---
name: nextjs-app-router
description: Deep runbook for Next.js App Router, RSC boundaries, and Server Actions.
author: "PatrickJS <patrick@cursor.directory>, customized by innerpeace080"
version: "1.3.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/PatrickJS/awesome-cursorrules"
  upstream_file: "rules/nextjs.mdc"
  upstream_commit: "8f391b4"
  source_type: "community-curated" # "community-official" | "community-curated" | "personal-original"
  lineage: "forked-and-customized" # "pure-upstream" | "forked-and-customized" | "personal-original"
  last_upstream_sync: "2026-09-26T23:15:00Z"
  customizations:
    - "Added Zod schema validation to Server Actions"
    - "Enforced React 19 RSC boundary rules"
    - "Integrated TanStack Query key factory pattern"
---

# Next.js App Router Runbook
...
```

---

## 3. Central Lineage Registry (`templates/registry.lock`)

At the root of the template engine, a machine-readable lockfile (`registry.lock`) maintains a complete **Bill of Materials (BOM)** mapping all artifacts to their upstream sources:

```json
{
  "$schema": "./schema/registry-lock.schema.json",
  "lockfileVersion": "1.0.0",
  "sources": {
    "awesome-cursorrules": {
      "name": "Awesome CursorRules",
      "repo": "https://github.com/PatrickJS/awesome-cursorrules",
      "type": "git",
      "commit": "8f391b4",
      "license": "MIT"
    },
    "anthropics-skills": {
      "name": "Anthropic Official Skills",
      "repo": "https://github.com/anthropics/skills",
      "type": "git",
      "commit": "1a2b3c4",
      "license": "Apache-2.0"
    },
    "trailofbits-config": {
      "name": "Trail of Bits Claude Code Config",
      "repo": "https://github.com/trailofbits/claude-code-config",
      "type": "git",
      "commit": "6e7f8a9",
      "license": "Apache-2.0"
    },
    "github-spec-kit": {
      "name": "GitHub Spec Kit",
      "repo": "https://github.com/github/spec-kit",
      "type": "git",
      "commit": "9b8a7c6",
      "license": "MIT"
    }
  },
  "artifacts": {
    "skills/nextjs-app-router": {
      "source": "awesome-cursorrules",
      "upstreamPath": "rules/nextjs.mdc",
      "lineage": "forked-and-customized",
      "upstreamHash": "sha256:d8a9f...",
      "localHash": "sha256:c4b3a...",
      "hasPersonalEdits": true
    },
    "skills/security-audit": {
      "source": "trailofbits-config",
      "upstreamPath": "rules/security.md",
      "lineage": "pure-upstream",
      "upstreamHash": "sha256:112233...",
      "localHash": "sha256:112233...",
      "hasPersonalEdits": false
    },
    "skills/my-payment-webhook": {
      "source": "personal",
      "lineage": "personal-original",
      "author": "innerpeace080",
      "hasPersonalEdits": true
    }
  }
}
```

---

## 4. CLI Source & Provenance Management

`ai-assist-bootstrap` provides dedicated commands to manage, audit, and sync community sources:

### 1. `ai-assist-bootstrap sources list`
Displays a clean terminal table showing all registered skills and rules with their origins and status:
```
Artifact                     Source                 Lineage                 Status
──────────────────────────────────────────────────────────────────────────────────
skills/nextjs-app-router     awesome-cursorrules    forked-and-customized   Modified (3 custom rules)
skills/security-audit        trailofbits-config     pure-upstream           Synced with upstream
skills/my-payment-webhook    personal               personal-original       Author: innerpeace080
```

### 2. `ai-assist-bootstrap sources diff <skill-name>`
Compares your customized skill against the exact original community file it was derived from:
```bash
ai-assist-bootstrap sources diff nextjs-app-router
```
* Shows a colored diff highlighting **your personal additions** vs **the original community text**.

### 3. `ai-assist-bootstrap sources check-updates`
Queries upstream community Git repositories to see if any upstream skills or rules have newer commits:
```bash
ai-assist-bootstrap sources check-updates
# Output:
# [UPDATE AVAILABLE] awesome-cursorrules updated `rules/nextjs.mdc` (commit: 9a8b7c)
# Run `ai-assist-bootstrap sources pull nextjs-app-router` to 3-way merge upstream changes.
```

### 4. `ai-assist-bootstrap sources credit`
Generates an automatic `ATTRIBUTION.md` honoring community authors, licenses, and repositories.

