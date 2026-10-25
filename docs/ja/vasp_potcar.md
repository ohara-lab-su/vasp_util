# vasp_potcar — 実装に基づく API Reference

対象ソース: `vasp_potcar(5).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspPotcarBuilder`

指定された元素リストから最適なポテンシャルを選び、
一つの POTCAR に連結して出力するクラス。

### `__init__`

```python
def __init__(self, base_dir: str='~/potpaw_PBE.64', logger: Optional[XLogger]=None)
```

**既存 docstring（原文）**

```text
Args:
    base_dir (str):
    logger (XLogger): 全てのインスタンスが同じ XLogger()
```

**呼び出す関数・メソッド（静的抽出）:** `XLogger`, `os.path.expanduser`

**更新するインスタンス属性（直接代入）:** `self._logger`, `self.base_dir`, `self.priority`

**ソース位置:** L24–L144（添付版）。

### `choose_potential`

```python
def choose_potential(self, element: str) -> str
```

**既存 docstring（原文）**

```text
最適な POTCAR のファイルパスを返す
```

**呼び出す関数・メソッド（静的抽出）:** `FileNotFoundError`, `KeyError`, `os.path.exists`, `os.path.join`

**明示的に送出する例外:** `FileNotFoundError(f'{element} に対応する POTCAR が見つかりません。')`; `KeyError(f'{element} は未登録の元素')`

**return 式（静的抽出）:** `path`

**主な条件分岐（静的抽出）:** `element not in self.priority`; `os.path.exists(path)`

**ソース位置:** L146–L158（添付版）。

### `build`

```python
def build(self, elements: Sequence[str], poscar_name: str='POTCAR') -> bool
```

**既存 docstring（原文）**

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

**呼び出す関数・メソッド（静的抽出）:** `FileNotFoundError`, `fin.read`, `fout.write`, `open`, `os.makedirs`, `os.path.dirname`, `os.path.exists`, `os.path.isfile`, `os.path.join`, `self._logger.error`, `self._logger.info`

**明示的に送出する例外:** `FileNotFoundError(f'ポテンシャルが見つかりません: {pot_src_path}')`

**return 式（静的抽出）:** `True`; `False`

**主な条件分岐（静的抽出）:** `output_dir and (not os.path.exists(output_dir))`; `not os.path.isfile(pot_src_path)`

**ソース位置:** L160–L203（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.util.make_potcar
:members:
:undoc-members:
:show-inheritance:
```
