---
name: shell-script-architecture
description: Modular Bash architecture (bin/ + lib/), getopts parsing, trap signal cleanup, and ShellCheck remediation.
author: "POSIX & Bash Community & ai-assist-bootstrap"
version: "1.0.0"
license: "MIT"
metadata:
  origin_repo: "https://github.com/bats-core/bats-core"
  upstream_file: "README.md"
  source_type: "official-grounded"
  lineage: "curated"
  last_upstream_sync: "2026-09-26T23:40:00Z"
  customizations:
    - "Modular bin/ and lib/ separation pattern"
    - "trap EXIT INT TERM resource cleanup"
    - "POSIX getopts standard pattern"
---

# Modular Shell Script Architecture Runbook

## When to Use
Use this skill when designing, authoring, or refactoring Bash and POSIX shell scripts, command-line utilities, installation scripts, or automated pipelines.

---

## 1. Directory Structure

```text
├── bin/
│   └── my-tool           # Executable entrypoint (chmod +x)
├── lib/
│   ├── utils.sh          # Logging, color formatting, environment helpers
│   └── commands.sh       # Subcommand business logic
├── test/
│   └── my-tool.bats      # Hermetic bats-core tests
├── .shellcheckrc
└── Makefile
```

---

## 2. Standard Script Boilerplate (`bin/my-tool`)

Always enforce strict error settings and resolve library paths relative to script source:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Determine canonical script root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Source reusable libraries
# shellcheck source=../lib/utils.sh
source "${ROOT_DIR}/lib/utils.sh"

# Trap cleanup for temporary files
TMP_DIR="$(mktemp -d)"
cleanup() {
    rm -rf "${TMP_DIR}"
}
trap cleanup EXIT INT TERM

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] <COMMAND>

Commands:
  run       Execute main task
  doctor    Verify environment dependencies

Options:
  -v, --verbose    Enable verbose debug output
  -h, --help       Show this help message
EOF
    exit 1
}

# Parse options
VERBOSE=0
while getopts ":vh-:" opt; do
    case "${opt}" in
        v) VERBOSE=1 ;;
        h) usage ;;
        -)
            case "${OPTARG}" in
                verbose) VERBOSE=1 ;;
                help) usage ;;
                *) echo "Unknown option --${OPTARG}" >&2; usage ;;
            esac
            ;;
        \?) echo "Invalid option -${OPTARG}" >&2; usage ;;
    esac
done
shift $((OPTIND - 1))
```

---

## 3. ShellCheck Common Pitfalls & Rules

- **Always quote variables**: Use `"${VAR}"` instead of `$VAR` to avoid word splitting and glob expansion (SC2086).
- **Separate declaration and assignment**: When capturing command output in local variables, declare first to preserve exit codes (SC2155):
  ```bash
  # BAD: hides exit code of command
  local output="$(some_command)"

  # GOOD:
  local output
  output="$(some_command)"
  ```
- **Use `[[ ... ]]` over `[ ... ]` in Bash**: Better handling of strings, logical operators (`&&`, `||`), and pattern matching.

---

## 4. Verification & Testing
- **Linting**: `shellcheck bin/* lib/*.sh`
- **Formatting**: `shfmt -d -i 2 -ci bin/ lib/`
- **Unit Tests**: `bats test/*.bats`

