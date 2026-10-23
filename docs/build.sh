#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$ROOT_DIR/src"
PKG_NAME="vasp_util"

export PYTHONPATH="$SRC_DIR:${PYTHONPATH:-}"

rm -rf "$SCRIPT_DIR/_build" "$SCRIPT_DIR/api"
mkdir -p "$SCRIPT_DIR/api" "$SCRIPT_DIR/_static"

sphinx-apidoc -o "$SCRIPT_DIR/api" "$SRC_DIR/$PKG_NAME" -f --module-first
sphinx-build -b html "$SCRIPT_DIR" "$SCRIPT_DIR/_build/html"
: > "$SCRIPT_DIR/_build/html/.nojekyll"

echo "Documentation built at docs/_build/html"
