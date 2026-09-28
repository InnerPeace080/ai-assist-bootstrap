# Workflow: Git Conventions & PR Generation

## Commit Conventions
All commit messages must adhere to the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```text
<type>(<scope>): <short summary>

[optional body explaining motivation and architectural rationale]

[optional footer(s), e.g. Closes #123]
```

### Allowed Types:
- `feat`: New user-facing or API feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavioral change
- `test`: Adding or improving tests
- `docs`: Documentation updates
- `perf`: Performance improvements
- `chore`: Build tooling, dependency bumps, auxiliary configuration

---

## Pull Request Description Standard
When preparing a PR, the agent generates:
1. **Summary of Changes**: Concise bullet points explaining the diff.
2. **Motivation / Why**: The architectural reason or user story addressed.
3. **Verification Proof**: Command outputs (e.g., test runner pass, typecheck clean, lint clean).
4. **Breaking Changes**: Explicitly stated if any API or schema changes occur.

