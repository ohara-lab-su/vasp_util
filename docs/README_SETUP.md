# Documentation deployment

Place the `docs/` directory and the two root README files in the repository. Do not overwrite `src/vasp_util/`. The existing GitHub Actions Pages workflow runs `bash docs/build.sh`; this invokes `docs/generate_api.py` before Sphinx.

The top-level `docs/index.md` defaults to English and links to `docs/en/index.md` and `docs/jp/index.md`. Both languages contain a usage guide, preserved detailed method-by-method analysis, and an automatically generated API reference. The API generator writes only to `docs/{en,jp}/generated_api/` and the corresponding `api_reference.md`.

Sphinx dependencies: `sphinx`, `myst-parser`, `sphinx-rtd-theme`. Autodoc additionally needs importable project runtime dependencies. The source-based static inventory remains available even if imports fail. The detailed English source-analysis pages retain Japanese docstrings verbatim; those are not translated descriptions.
