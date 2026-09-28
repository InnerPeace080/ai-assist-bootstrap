#!/usr/bin/env bash
# ai-assist-bootstrap launcher
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
chmod +x "${SCRIPT_DIR}/bin/ai-assist"
exec "${SCRIPT_DIR}/bin/ai-assist" "$@"

