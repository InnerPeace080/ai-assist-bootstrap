# Workflow: Spec-Driven Development (SDD)

> Modeled after GitHub Spec Kit (`github/spec-kit`)

## Purpose
Transitions software development from informal "vibe coding" into disciplined, verified engineering anchored to persistent, repository-native specifications.

---

## 5-Phase Lifecycle

```
[ 1. Constitution ] ──> [ 2. Specify ] ──> [ 3. Plan ] ──> [ 4. Tasks ] ──> [ 5. Implement & Converge ]
```

### Phase 1: Constitution (`CONSTITUTION.md`)
- Defines non-negotiable architectural invariants (e.g. strict TypeScript, zero `any`, required transactions, strict accessibility).
- Checked before designing any feature.

### Phase 2: Specification (`.specify/specs/<feature>.md`)
- Captures *What* and *Why*. Focuses on user stories and acceptance criteria (Given/When/Then).
- Independent of implementation details.

### Phase 3: Architectural Plan (`.specify/plans/<feature>.md`)
- Captures *How*. Outlines database schema modifications, API contracts, dependency choices, and performance budgets.

### Phase 4: Task Breakdown (`.specify/tasks/<feature>.md`)
- Decomposes the plan into dependency-ordered, atomic checklist tasks.

### Phase 5: Implement & Converge
- Execute task checklist incrementally.
- Run formal **Convergence Check** verifying generated code matches the acceptance criteria in the original spec.

