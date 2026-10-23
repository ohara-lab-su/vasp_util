"""Regenerate bilingual API inventories from the installed source tree."""
from __future__ import annotations
import ast
from pathlib import Path
ROOT: Path = Path(__file__).resolve().parent.parent
SOURCE: Path = ROOT / "src" / "vasp_util"
DOCS: Path = ROOT / "docs"

def signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    try:
        return ast.unparse(node).split("\n", 1)[0].rstrip(":")
    except (ValueError, TypeError):
        return node.name

def generate() -> None:
    if not SOURCE.is_dir():
        raise FileNotFoundError(f"Missing source directory: {SOURCE}")
    paths = sorted(p for p in SOURCE.rglob("*.py") if p.name != "__init__.py")
    if not paths:
        raise RuntimeError("No source modules found")
    for lang in ("en", "jp"):
        target = DOCS / lang / "generated_api"
        target.mkdir(parents=True, exist_ok=True)
        names: list[str] = []
        for path in paths:
            relative = path.relative_to(SOURCE).with_suffix("")
            name = "_".join(relative.parts)
            names.append(name)
            module = "vasp_util." + ".".join(relative.parts)
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            rows = [f"# {module}", "", f"Source: `src/vasp_util/{path.relative_to(SOURCE)}`", ""]
            for item in tree.body:
                if isinstance(item, ast.ClassDef):
                    rows.extend([f"## class `{item.name}`", ""])
                    if ast.get_docstring(item):
                        rows.extend([ast.get_docstring(item), ""])
                    for method in item.body:
                        if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            rows.extend([f"### `{item.name}.{method.name}`", "", "```python", signature(method), "```", ""])
                            if ast.get_docstring(method):
                                rows.extend([ast.get_docstring(method), ""])
                            rows.extend([f"Source lines: {method.lineno}–{method.end_lineno}", ""])
                elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    rows.extend([f"## function `{item.name}`", "", "```python", signature(item), "```", ""])
                    if ast.get_docstring(item):
                        rows.extend([ast.get_docstring(item), ""])
                    rows.extend([f"Source lines: {item.lineno}–{item.end_lineno}", ""])
            # Sphinx autodoc reads live code. Static inventory remains usable if imports fail.
            rows.extend(["## Live API (autodoc)", "", "```{eval-rst}", f".. automodule:: {module}", "   :members:", "   :undoc-members:", "   :private-members:", "   :special-members: __init__", "```", ""])
            (target / f"{name}.md").write_text("\n".join(rows), encoding="utf-8")
        title = "API Reference" if lang == "en" else "API リファレンス"
        (DOCS / lang / "api_reference.md").write_text(f"# {title}\n\nRegenerated from `src/vasp_util/` at every build. Original source-language docstrings are preserved.\n\n```{{toctree}}\n:maxdepth: 2\n\n" + "\n".join(f"generated_api/{n}" for n in names) + "\n```\n", encoding="utf-8")
    print(f"Generated {len(paths)} modules in en and jp")

if __name__ == "__main__":
    generate()
