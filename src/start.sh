#!/bin/sh

SCRIPT_DIR=$(dirname "$0")
uv run alembic upgrade head
uv run python "${SCRIPT_DIR}/main.py"
