# Workflow: GSD Anti-Context-Rot Execution

> Modeled after Get Shit Done / Open GSD (`open-gsd/gsd-core`)

## Purpose
Eliminates cognitive degradation and hallucination loops ("Context Rot") in long AI coding sessions through isolated subagent task passes and persistent repository state tracking.

---

## Core Principles

1. **Persistent State Markers (`STATE.md`)**:
   - High-level progress, current task index, and architecture decisions are recorded in `STATE.md`, NOT stored in transient chat context.
2. **Fresh Subagent per Task**:
   - When executing a multi-step feature, spawn a **clean subagent** for each task.
   - The subagent reads `STATE.md`, executes its single discrete task, validates changes, and terminates.
3. **Atomic Handoff**:
   - Subagent commits its diff and updates `STATE.md` before exiting.
   - Prevents stale tokens, discarded tool outputs, and conversational drift from polluting future tasks.

