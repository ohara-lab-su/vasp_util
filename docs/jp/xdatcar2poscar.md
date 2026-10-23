# xdatcar2poscar — 実装に基づく API Reference

対象ソース: `xdatcar2poscar.py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## function `xdatcar2poscar`

```python
def xdatcar2poscar(vasp_name: str, logger: Optional[XLogger]=XLogger())
```

**既存 docstring（原文）**

```text
VASP の XDATCAR ファイルを POSCAR 形式にする

Args:
    vasp_name (str): {vasp_name}.vasp
    logger (Xlogger):
```

**呼び出す関数・メソッド（静的抽出）:** `XLogger`, `datfile.split`, `datlines[6].split`, `f.close`, `f.write`, `len`, `list`, `logger.info`, `map`, `open`, `os.path.exists`, `sum`, `tmp.close`, `tmp.read`

**return 式（静的抽出）:** `True`; `False`

**主な条件分岐（静的抽出）:** `not os.path.exists('XDATCAR')`; `NSW > 1`

**ソース位置:** L37–L91（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.util.xdatcar2poscar
:members:
:undoc-members:
:show-inheritance:
```
