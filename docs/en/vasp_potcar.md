# vasp_potcar — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `vasp_potcar`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `vasp_potcar(5).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspPotcarBuilder`

指定された元素リストから最適なポテンシャルを選び、
一つの POTCAR に連結して出力するクラス。

### `__init__`

```python
def __init__(self, base_dir: str='~/potpaw_PBE.64', logger: Optional[XLogger]=None)
```

**Original docstring (source language)**

```text
Args:
    base_dir (str):
    logger (XLogger): 全てのインスタンスが同じ XLogger()
```

**Calls (static AST extraction):** `XLogger`, `os.path.expanduser`

**Instance attributes assigned directly:** `self._logger`, `self.base_dir`, `self.priority`

**Source location:** L24–L144（添付版）。

### `choose_potential`

```python
def choose_potential(self, element: str) -> str
```

**Original docstring (source language)**

```text
最適な POTCAR のファイルパスを返す
```

**Calls (static AST extraction):** `FileNotFoundError`, `KeyError`, `os.path.exists`, `os.path.join`

**Explicitly raised exceptions:** `FileNotFoundError(f'{element} に対応する POTCAR が見つかりません。')`; `KeyError(f'{element} は未登録の元素')`

**Return expressions (static extraction):** `path`

**Principal conditions (static extraction):** `element not in self.priority`; `os.path.exists(path)`

**Source location:** L146–L158（添付版）。

### `build`

```python
def build(self, elements: Sequence[str], poscar_name: str='POTCAR') -> bool
```

**Original docstring (source language)**

```text
指定元素リストから POTCAR を構築して出力する。

判定規則:
  - poscar_name が区切り記号で終わる、または実在するディレクトリ -> ディレクトリ扱い（中に POTCAR）
  - 上記以外 -> ファイル扱い（親ディレクトリを作成）

Args:
    elements (list[str])::
    poscar_name (str):

Returns:
    bool:
```

**Calls (static AST extraction):** `FileNotFoundError`, `fin.read`, `fout.write`, `open`, `os.makedirs`, `os.path.dirname`, `os.path.exists`, `os.path.isfile`, `os.path.join`, `self._logger.error`, `self._logger.info`

**Explicitly raised exceptions:** `FileNotFoundError(f'ポテンシャルが見つかりません: {pot_src_path}')`

**Return expressions (static extraction):** `True`; `False`

**Principal conditions (static extraction):** `output_dir and (not os.path.exists(output_dir))`; `not os.path.isfile(pot_src_path)`

**Source location:** L160–L203（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.util.make_potcar
:members:
:undoc-members:
:show-inheritance:
```
