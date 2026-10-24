#!/usr/bin/env bash
set -euo pipefail
DOCS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$DOCS_DIR/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/src/vasp_util"
OUTPUT_DIR="$DOCS_DIR/_build/html"
if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Python package not found: $SOURCE_DIR" >&2
  exit 1
fi
export PYTHONPATH="$ROOT_DIR/src:${PYTHONPATH:-}"
rm -rf "$OUTPUT_DIR"
for LANG_CODE in en jp; do
  sphinx-apidoc --force --module-first --no-toc -o "$DOCS_DIR/$LANG_CODE/api/generated" "$SOURCE_DIR"
  if [[ "$LANG_CODE" == "jp" ]]; then
    SPHINX_LANG=ja
  else
    SPHINX_LANG=en
  fi
  sphinx-build -b html -c "$DOCS_DIR" -D "language=$SPHINX_LANG" "$DOCS_DIR/$LANG_CODE" "$OUTPUT_DIR/$LANG_CODE"
done
python - "$OUTPUT_DIR" <<'PYINNER'
from pathlib import Path
import sys
root = Path(sys.argv[1])
page = (root / "en" / "index.html").read_text(encoding="utf-8")
if "<head>" not in page:
    raise RuntimeError("Unexpected Sphinx HTML: missing <head>")
page = page.replace("<head>", '<head>\n<base href="en/">', 1)
(root / "index.html").write_text(page, encoding="utf-8")
(root / ".nojekyll").touch()
PYINNER
