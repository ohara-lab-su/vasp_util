# vasp_incar — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `vasp_incar`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `vasp_incar(4).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspIncar`

VASP INCAR 編集を一元管理するクラス。
pymatgen.Incar による値操作と、コメント保持を両立する。

主な特徴:
    - 既存INCARファイルを安全に読み込み、コメント/空行を保持。
    - 値の追加・更新・削除をサポート。
    - pymatgen.Incar 互換インターフェース (get/set/remove/export)。

### `__init__`

```python
def __init__(self, incar_name: str='INCAR', *, config: Optional[Config]=None, logger: Optional[XLogger]=None, auto_write: bool=True) -> None
```

**Original docstring (source language)**

```text
Args:
    incar_name (str):
    logger (XLogger):
    auto_write (bool):
```

**Calls (static AST extraction):** `Config`, `Incar`, `XLogger`, `os.path.abspath`

**Source location:** L25–L53（添付版）。

### `init`

```python
def init(self) -> None
```

**Original docstring (source language)**

```text
INCAR を一度だけ初期化する。

RmcPotDat.init() と同じ役割を持つ。

- 既存 INCAR がある場合:
  そのファイルを読み込み、現在の入力として使用する。
  ファイル内容は変更しない。
- INCAR がない場合:
  空の INCAR を新規作成し、それを現在の入力として使用する。
- 一度初期化済みの場合:
  何もしない。

このメソッドは入力ファイルを確定するだけであり、
INCAR タグの変更は set()/set_tag() が担当する。
```

**Calls (static AST extraction):** `os.path.exists`, `self._logger.info`, `self.create_incar_file`, `self.load`

**Principal conditions (static extraction):** `self._initialized`; `os.path.exists(self.incar_name)`

**Source location:** L55–L81（添付版）。

### `_ensure_initialized`

```python
def _ensure_initialized(self) -> None
```

**Original docstring (source language)**

```text
未初期化の場合だけ init() を実行する。
```

**Calls (static AST extraction):** `self.init`

**Principal conditions (static extraction):** `not self._initialized`

**Source location:** L83–L86（添付版）。

### `create_incar_file`

```python
def create_incar_file(self) -> bool
```

**Original docstring (source language)**

```text
空の INCAR を新規作成する。

Returns:
    新規作成した場合は True。
    既に INCAR が存在する場合は上書きせず False。
```

**Calls (static AST extraction):** `Incar`, `open`, `os.path.exists`, `self._logger.info`

**Return expressions (static extraction):** `True`; `False`

**Instance attributes assigned directly:** `self._incar`, `self._lines`

**Principal conditions (static extraction):** `os.path.exists(self.incar_name)`

**Source location:** L92–L108（添付版）。

### `load`

```python
def load(self) -> None
```

**Original docstring (source language)**

```text
ファイルを読み込み、pymatgen.Incarとテキスト行を両方保持
```

**Calls (static AST extraction):** `Incar.from_file`, `f.readlines`, `open`, `self._logger.info`

**Instance attributes assigned directly:** `self._incar`, `self._initialized`, `self._lines`

**Source location:** L110–L120（添付版）。

### `write`

```python
def write(self) -> None
```

**Original docstring (source language)**

```text
内部linesを書き戻し
```

**Calls (static AST extraction):** `f.writelines`, `open`, `self._logger.info`

**Source location:** L122–L126（添付版）。

### `_find_line_index`

```python
def _find_line_index(self, tag: str) -> Optional[int]
```

**Original docstring (source language)**

```text
指定タグの行番号を返す
実際の INCAR に、指定のタグがどの行にあるのか？を調べる
```

**Calls (static AST extraction):** `enumerate`, `line.split`, `line.split('=')[0].strip`, `line.split('=')[0].strip().upper`, `line.strip`, `line.strip().startswith`, `tag.upper`

**Return expressions (static extraction):** `None`; `i`

**Principal conditions (static extraction):** `'=' in line and (not line.strip().startswith('#'))`; `key == tag_upper`

**Source location:** L131–L145（添付版）。

### `_format_line`

```python
@staticmethod
```

**Original docstring (source language)**

```text
整形ルール統一
```

**Return expressions (static extraction):** `f'{tag:<15} = {value}\n'`

**Source location:** L148–L150（添付版）。

### `_resolve_auto_write`

```python
def _resolve_auto_write(self, auto_write: Optional[bool]) -> bool
```

**Original docstring (source language)**

```text
メソッド単位の自動保存指定を解決する。

None の場合だけ、インスタンス生成時の auto_write を使用する。
```

**Calls (static AST extraction):** `bool`

**Return expressions (static extraction):** `bool(auto_write)`; `self.auto_write`

**Principal conditions (static extraction):** `auto_write is None`

**Source location:** L152–L159（添付版）。

### `get`

```python
def get(self, tag: str, default: Any=None) -> Any
```

**Original docstring (source language)**

```text
値取得。存在しない場合はdefaultを返す。

Args:
    tag (str):
    default (Any):

Returns:
    Any:
```

**Calls (static AST extraction):** `self._ensure_initialized`, `self._incar.get`

**Return expressions (static extraction):** `self._incar.get(tag, default)`

**Source location:** L164–L180（添付版）。

### `get_tag`

```python
def get_tag(self, tag: str, default: Any=None) -> Any
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `self.get`

**Return expressions (static extraction):** `self.get(tag, default)`

**Source location:** L182–L183（添付版）。

### `set`

```python
def set(self, tag: str, value: Any, *, auto_write: Optional[bool]=True) -> None
```

**Original docstring (source language)**

```text
値設定。コメント保持したまま編集。

Args:
    tag (str):  INCAR のキー
    value (Any):  value

Returns:
    None:
```

**Calls (static AST extraction):** `self._ensure_initialized`, `self._find_line_index`, `self._format_line`, `self._lines.append`, `self._logger.info`, `self._resolve_auto_write`, `self.write`

**Instance attributes assigned directly:** `self._config.vasp_incar_tags`

**Principal conditions (static extraction):** `idx is not None`; `self._config is not None`; `self._resolve_auto_write(auto_write)`; `self._config.vasp_incar_tags is None`

**Source location:** L185–L226（添付版）。

### `set_tag`

```python
def set_tag(self, tag: str, value: Any, *, auto_write: Optional[bool]=True) -> None
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `self.set`

**Source location:** L228–L235（添付版）。

### `remove`

```python
def remove(self, tag: str, *, auto_write: Optional[bool]=True) -> None
```

**Original docstring (source language)**

```text
指定タグを削除
```

**Calls (static AST extraction):** `self._config.vasp_incar_tags.pop`, `self._ensure_initialized`, `self._find_line_index`, `self._logger.info`, `self._resolve_auto_write`, `self.write`

**Principal conditions (static extraction):** `idx is not None`; `tag in self._incar`; `self._config is not None and self._config.vasp_incar_tags is not None`; `self._resolve_auto_write(auto_write)`

**Source location:** L237–L258（添付版）。

### `reload`

```python
def reload(self) -> None
```

**Original docstring (source language)**

```text
再読込（外部修正反映）
```

**Calls (static AST extraction):** `self.load`

**Source location:** L260–L262（添付版）。

### `export_dict`

```python
def export_dict(self) -> Dict[str, Any]
```

**Original docstring (source language)**

```text
内部Incar辞書を返す
```

**Calls (static AST extraction):** `dict`, `self._ensure_initialized`

**Return expressions (static extraction):** `dict(self._incar)`

**Source location:** L264–L267（添付版）。

### `diff_with`

```python
def diff_with(self, other: 'VaspIncar') -> Dict[str, Tuple[Any, Any]]
```

**Original docstring (source language)**

```text
2つの VaspIncar インスタンスを比較し、値が異なるタグのみを返す。

コメント行や元の行順序は比較対象に含めず、
内部で保持している ``pymatgen.Incar`` 辞書
（``self._incar`` と ``other._incar``）の値だけで比較を行う。

Args:
    other (VaspIncar):
        比較対象となる VaspIncar インスタンス。

Returns:
    Dict[str, Tuple[Any, Any]]:
        値が異なるタグだけを含む辞書。
        キーがタグ名、値は ``(self 側の値, other 側の値)`` のタプル。
```

**Calls (static AST extraction):** `other._ensure_initialized`, `other._incar.get`, `other._incar.keys`, `self._ensure_initialized`, `self._incar.get`, `self._incar.keys`, `set`, `sorted`

**Return expressions (static extraction):** `diff`

**Principal conditions (static extraction):** `v1 != v2`

**Source location:** L269–L300（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_incar
:members:
:undoc-members:
:show-inheritance:
```
