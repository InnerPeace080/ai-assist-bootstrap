# /export-back - Export Refined Rule/Skill Upstream

Extract a project-refined skill or rule and save it back to your personal global library (`~/.ai-assist/`) or the central upstream repository.

## Usage
`/export-back <item-name> [--to-git] [--to-local-repo <path>] [--push]`

## Instructions
1. Extract the target item name from arguments: `$ARGUMENTS`.
2. Execute the export-back command:
   ```bash
   ./bin/ai-assist export-back $ARGUMENTS
   ```
3. **Security Sanitization Gate**:
   - The CLI will scan the source file for sensitive credentials (API tokens, private keys, live secrets).
   - If secrets are detected, the export is blocked automatically. Remove sensitive information before retrying.
4. Report the destination path and git commit status to the developer.
