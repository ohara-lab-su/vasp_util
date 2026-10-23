"""Sphinx configuration for vasp_util."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

project = "vasp_util"
language = "ja"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
autosummary_generate = True
myst_enable_extensions = ["deflist", "attrs_block", "substitution", "colon_fence", "linkify"]
myst_linkify_fuzzy_links = True
myst_heading_anchors = 3

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "private-members": True,
}
autodoc_typehints = "description"
autodoc_preserve_defaults = True
add_module_names = False

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
}
html_static_path = ["_static"]
