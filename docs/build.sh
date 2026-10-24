#!/usr/bin/env bash
set -euo pipefail
DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DOCS_DIR/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/src/vasp_util"
if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: Python package not found: $SOURCE_DIR" >&2
  exit 1
fi
export PYTHONPATH="$ROOT_DIR/src:${PYTHONPATH:-}"
mkdir -p "$DOCS_DIR/en/api/generated" "$DOCS_DIR/jp/api/generated"
sphinx-apidoc --force --module-first -o "$DOCS_DIR/en/api/generated" "$SOURCE_DIR"
sphinx-apidoc --force --module-first -o "$DOCS_DIR/jp/api/generated" "$SOURCE_DIR"
sphinx-build -b html -c "$DOCS_DIR" "$DOCS_DIR" "$DOCS_DIR/_build/html"
