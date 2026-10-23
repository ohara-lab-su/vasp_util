"""Sphinx configuration for the source-based bilingual documentation."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
project = "vasp_util"
master_doc = "index"
language = "en"
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build"]
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.viewcode"]
html_theme = "sphinx_rtd_theme"
myst_enable_extensions = ["colon_fence"]
html_static_path = []
