# Workflow: Plan-Execute-Verify

## Purpose
Enforces a structured, four-phase engineering discipline before modifying application code, preventing premature edits and unbudgeted hallucinations.

---

## Phase 1: Research & Discovery
- **Action**: Read relevant source files, package manifests, and existing test suites.
- **Constraints**: 
  - DO NOT modify or create code files during this phase.
  - Inspect project patterns, shared utilities, and existing conventions.
  - Document all assumptions and dependencies.

## Phase 2: Technical Specification & Plan
- **Action**: Formulate a step-by-step implementation plan.
- **Components of Plan**:
  1. Files to create, modify, or delete.
  2. Potential risks or breaking changes.
  3. Acceptance criteria and verification commands to run.
- **Gate**: Present the plan to the developer for confirmation before proceeding.

## Phase 3: Atomic Execution
- **Action**: Implement changes incrementally in small, self-contained steps.
- **Per-Step Checks**:
  - Run typecheckers (`tsc --noEmit`, `mypy`, `cargo check`) after each step.
  - Ensure individual file changes do not introduce linter errors.

## Phase 4: Verification & Self-Review
- **Action**: Run the complete automated test suite (`pnpm test`, `pytest`, `cargo test`, `go test`).
- **Audit**: Run `git diff` to ensure no accidental edits, debug statements, or secrets were introduced.

