# Documentation build

`build.sh` generates the English and Japanese Sphinx sites and also builds the root `index.html` directly from `en/index.md`. No standalone `docs/index.html` is maintained. The root build differs only in the relative URLs of its language badges.

Outputs: `_build/html/index.html`, `_build/html/en/index.html`, `_build/html/ja/index.html`.
