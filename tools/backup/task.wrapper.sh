#!/usr/bin/env bash
set -euo pipefail

echo "DEPRECATED: tools/task.sh has been retired." >&2
echo "Use 'python3 tools/taskclient.py --next' to pick the next task." >&2
echo "Use 'python3 tools/taskclient.py --create ...' to create a task." >&2
exit 1
