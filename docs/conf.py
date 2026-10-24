from pathlib import Path
import sys

DOCS_DIR = Path(__file__).resolve().parent
ROOT_DIR = DOCS_DIR.parent
sys.path.insert(0, str(ROOT_DIR / "src"))
project = "rmc_util"
root_doc = "index"
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]
autosummary_generate = True
myst_enable_extensions = ["colon_fence", "dollarmath", "amsmath"]
html_theme = "sphinx_rtd_theme"
exclude_patterns = ["_build"]
