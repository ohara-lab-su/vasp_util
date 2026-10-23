# xdatcar2poscar — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `xdatcar2poscar`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `xdatcar2poscar.py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## function `xdatcar2poscar`

```python
def xdatcar2poscar(vasp_name: str, logger: Optional[XLogger]=XLogger())
```

**Original docstring (source language)**

```text
VASP の XDATCAR ファイルを POSCAR 形式にする

Args:
    vasp_name (str): {vasp_name}.vasp
    logger (Xlogger):
```

**Calls (static AST extraction):** `XLogger`, `datfile.split`, `datlines[6].split`, `f.close`, `f.write`, `len`, `list`, `logger.info`, `map`, `open`, `os.path.exists`, `sum`, `tmp.close`, `tmp.read`

**Return expressions (static extraction):** `True`; `False`

**Principal conditions (static extraction):** `not os.path.exists('XDATCAR')`; `NSW > 1`

**Source location:** L37–L91（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.util.xdatcar2poscar
:members:
:undoc-members:
:show-inheritance:
```
