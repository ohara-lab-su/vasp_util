#!/usr/bin/env bash
set -euo pipefail

DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DOCS_DIR/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/src/vasp_util"
BUILD_DIR="$DOCS_DIR/_build/html"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "ERROR: Python package not found: $SOURCE_DIR" >&2
  exit 1
fi

export PYTHONPATH="$ROOT_DIR/src:${PYTHONPATH:-}"

# Generate API pages independently for each language.
sphinx-apidoc --force --module-first -o "$DOCS_DIR/en/api/generated" "$SOURCE_DIR"
sphinx-apidoc --force --module-first -o "$DOCS_DIR/ja/api/generated" "$SOURCE_DIR"

# The English documentation IS the site root; no separate landing page.
sphinx-build -b html -c "$DOCS_DIR" -D language=en "$DOCS_DIR/en" "$BUILD_DIR"
# Independent navigation trees for each language.
sphinx-build -b html -c "$DOCS_DIR" -D language=en "$DOCS_DIR/en" "$BUILD_DIR/en"
sphinx-build -b html -c "$DOCS_DIR" -D language=ja "$DOCS_DIR/ja" "$BUILD_DIR/ja"
