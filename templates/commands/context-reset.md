# /context-reset - GSD Anti-Context-Rot Handoff

Wipe transient conversational noise and perform an atomic task handoff via persistent repository state markers.

## Instructions
Execute the **`gsd-context-reset`** workflow:

1. **Verify In-Progress Work**:
   - Check working directory status: `git status -s`.
   - Ensure all current code changes pass linters and tests before handoff.
2. **Atomic Git Commit**:
   - Commit the verified changes with a conventional commit message (`feat:`, `fix:`, `refactor:`, `test:`).
3. **Update State Marker (`STATE.md`)**:
   - Record the completed subtask summary.
   - Note any critical architectural decisions or discovered constraints.
   - Define the next discrete task item for the incoming clean session.
4. **Signal Clean Handoff**:
   - Conclude your response informing the developer that the task milestone is safely recorded in `STATE.md`, and conversational context can now be safely refreshed.
