# Workflow: Test-Driven Development (TDD)

## Purpose
Anchors AI code generation to verifiable automated test feedback. Eliminates guesswork by proving failure before writing implementation code.

---

## The Red-Green-Refactor Loop

```
  [ 1. Write Test ] ──> [ 2. Run Test (Must Fail: RED) ] ──> [ 3. Write Minimal Code ] ──> [ 4. Run Test (Must Pass: GREEN) ] ──> [ 5. Refactor ]
```

### Step 1: Write Test First
- Create or update test files *before* touching application logic.
- Cover normal paths, edge cases, boundary conditions, and error states.

### Step 2: Verify Expected Failure (RED)
- Run the test suite: verify that the test fails *specifically for the reason you expect* (confirming that the test actually exercises the intended logic).

### Step 3: Minimal Implementation
- Write only the minimal production code necessary to satisfy the test.
- Avoid premature optimizations or speculative functionality ("YAGNI").

### Step 4: Verify Success (GREEN)
- Execute the test suite again: all tests must pass with zero failures.

### Step 5: Clean Refactor
- Clean up variable names, extract duplicated logic, and optimize while keeping all tests passing.

