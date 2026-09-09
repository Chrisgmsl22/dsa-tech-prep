#!/usr/bin/env bash
# Run every LLD test with pytest from the repo venv.
#   Setup once:  python3 -m venv .venv && .venv/bin/python -m pip install -r requirements-dev.txt
set -eu
repo="$(cd "$(dirname "$0")/.." && pwd)"
exec "$repo/.venv/bin/pytest" "$repo/lld" -q "$@"
