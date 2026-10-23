# vasp_kpoints — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `vasp_kpoints`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `vasp_kpoints(4).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspKpoints`

KPOINTS ファイルの読み書きと、モード/グリッド/シフト/コメントの管理を行う。

既定動作
- 既存 KPOINTS があれば読み取り優先。
- 無い場合は "Monkhorst-Pack", grid=(1,1,1), shift=(0,0,0), comment="K-Points" で初期化。

Aargs:
    kpoints_name (str): KPOINTS ファイル名（絶対パス推奨）。
    auto_write (bool): True の場合、set_* 呼び出しで都度ファイルへ保存。
    _logger (XLogger): 任意のロガー（info/debug を想定）。None 可。

### `__init__`

```python
def __init__(self, kpoints_name: str='KPOINTS', *, config: Optional[Config]=None, logger: Optional[XLogger]=None, auto_write: bool=True) -> None
```

**Original docstring (source language)**

```text
Args:
    kpoints_name (str):
    logger (XLogger):
    auto_write (bool):
```

**Calls (static AST extraction):** `Config`, `XLogger`, `os.path.exists`, `self._build_kpoints`, `self.load`, `self.write`

**Instance attributes assigned directly:** `self._comment`, `self._config`, `self._grid`, `self._kpts_obj`, `self._mode`, `self._shift`, `self.logger`

**Principal conditions (static extraction):** `os.path.exists(self.kpoints_name)`

**Source location:** L53–L92（添付版）。

### `load`

```python
def load(self)
```

**Original docstring (source language)**

```text
既存の KPOINTS を読み込む
```

**Calls (static AST extraction):** `Kpoints.from_file`, `getattr`, `int`, `len`, `self.logger.info`

**Instance attributes assigned directly:** `self._comment`, `self._grid`, `self._kpts_obj`, `self._mode`, `self._shift`

**Principal conditions (static extraction):** `getattr(self._kpts_obj, 'style', None) == Kpoints.supported_modes.Gamma`; `self._kpts_obj.kpts and len(self._kpts_obj.kpts[0]) == 3`; `self._kpts_obj.kpts_shift and len(self._kpts_obj.kpts_shift) == 3`; `self.logger`

**Source location:** L94–L127（添付版）。

### `write`

```python
def write(self) -> None
```

**Original docstring (source language)**

```text
現在の内部状態を KPOINTS ファイルへ書き出す。
```

**Calls (static AST extraction):** `self._build_kpoints`, `self._kpts_obj.write_file`, `self.logger.info`

**Instance attributes assigned directly:** `self._kpts_obj`

**Principal conditions (static extraction):** `self.logger`

**Source location:** L129–L136（添付版）。

### `export_dict`

```python
def export_dict(self) -> dict
```

**Original docstring (source language)**

```text
現在の内部状態を辞書で返す（ロギング/デバッグ用）。
```

**Return expressions (static extraction):** `{'mode': self._mode, 'grid': self._grid, 'shift': self._shift, 'comment': self._comment, 'path': self.kpoints_name}`

**Source location:** L138–L146（添付版）。

### `update`

```python
def update(self, mode: Optional[str]=None, grid: Optional[Tuple[int, int, int]]=None, shift: Optional[Tuple[int, int, int]]=None, comment: Optional[str]=None) -> None
```

**Original docstring (source language)**

```text
複数項目をまとめて更新する。指定されたもののみ反映。
auto_write=True のときは更新後に書き出し。
```

**Calls (static AST extraction):** `ValueError`, `int`, `len`, `self.set_comment`, `self.set_grid`, `self.set_mode`, `self.set_shift`

**Explicitly raised exceptions:** `ValueError('grid must be a tuple of length 3')`; `ValueError('shift must be a tuple of length 3')`

**Principal conditions (static extraction):** `mode is not None`; `grid is not None`; `shift is not None`; `comment is not None`; `changed and (not self.auto_write)`; `len(grid) != 3`; `len(shift) != 3`

**Source location:** L148–L185（添付版）。

### `_build_kpoints`

```python
def _build_kpoints(self) -> Kpoints
```

**Original docstring (source language)**

```text
内部状態（mode/grid/shift/comment）に基づき Kpoints を構築する。
現行 pymatgen I/F に合わせ、automatic は使用せず gamma_automatic / monkhorst_automatic を利用。
```

**Calls (static AST extraction):** `Kpoints.gamma_automatic`, `Kpoints.monkhorst_automatic`, `list`

**Return expressions (static extraction):** `kpt`

**Principal conditions (static extraction):** `self._mode == 'Gamma'`

**Source location:** L187–L202（添付版）。

### `get_mode`

```python
def get_mode(self) -> str
```

**Original docstring (source language)**

```text
現在のモード（"Gamma" or "Monkhorst-Pack"）を返す。
```

**Return expressions (static extraction):** `self._mode`

**Source location:** L207–L209（添付版）。

### `set_mode`

```python
def set_mode(self, mode: str, auto_write: Optional[bool]=None) -> None
```

**Original docstring (source language)**

```text
モードを設定する。大文字小文字はそのまま保存するが、想定は "Gamma" / "Monkhorst-Pack"。

Args:
    mode (str):
    auto_write (bool):

Returns:
```

**Calls (static AST extraction):** `ValueError`, `self._build_kpoints`, `self.write`

**Explicitly raised exceptions:** `ValueError('mode must be "Gamma" or "Monkhorst-Pack"')`

**Instance attributes assigned directly:** `self._config.vasp_kpoints_mode`, `self._kpts_obj`, `self._mode`

**Principal conditions (static extraction):** `mode not in ('Gamma', 'Monkhorst-Pack')`; `self._config is not None`; `auto_write is None`; `auto_write`

**Source location:** L211–L240（添付版）。

### `get_grid`

```python
def get_grid(self) -> Tuple[int, int, int]
```

**Original docstring (source language)**

```text
k-point グリッド (kx, ky, kz) を返す。
```

**Return expressions (static extraction):** `self._grid`

**Source location:** L242–L244（添付版）。

### `set_grid`

```python
def set_grid(self, kx: int, ky: int, kz: int, auto_write: Optional[bool]=None) -> None
```

**Original docstring (source language)**

```text
k-point グリッド (kx, ky, kz) を設定する。

Args:
    kx:
    ky:
    kz:
    auto_write (bool):

Returns:
```

**Calls (static AST extraction):** `int`, `self._build_kpoints`, `self.write`

**Instance attributes assigned directly:** `self._config.vasp_kpoints_grid`, `self._grid`, `self._kpts_obj`

**Principal conditions (static extraction):** `self._config is not None`; `auto_write is None`; `auto_write`

**Source location:** L246–L275（添付版）。

### `get_shift`

```python
def get_shift(self) -> Tuple[int, int, int]
```

**Original docstring (source language)**

```text
シフト (sx, sy, sz) を返す。
```

**Return expressions (static extraction):** `self._shift`

**Source location:** L277–L279（添付版）。

### `set_shift`

```python
def set_shift(self, sx: int, sy: int, sz: int, auto_write: Optional[bool]=None) -> None
```

**Original docstring (source language)**

```text
シフト (sx, sy, sz) を設定する。

Args:
    sx:
    sy:
    sz:
    auto_write (bool):

Returns:
```

**Calls (static AST extraction):** `int`, `self._build_kpoints`, `self.write`

**Instance attributes assigned directly:** `self._config.vasp_kpoints_shift`, `self._kpts_obj`, `self._shift`

**Principal conditions (static extraction):** `self._config is not None`; `auto_write is None`; `auto_write`

**Source location:** L281–L310（添付版）。

### `get_comment`

```python
def get_comment(self) -> str
```

**Original docstring (source language)**

```text
先頭コメントを返す。
```

**Return expressions (static extraction):** `self._comment`

**Source location:** L312–L314（添付版）。

### `set_comment`

```python
def set_comment(self, comment: str, auto_write: Optional[bool]=None) -> None
```

**Original docstring (source language)**

```text
先頭コメントを設定する。

Args:
    comment (str):
    auto_write (bool):

Returns:
```

**Calls (static AST extraction):** `self._build_kpoints`, `self.write`

**Instance attributes assigned directly:** `self._comment`, `self._config.vasp_kpoints_comment`, `self._kpts_obj`

**Principal conditions (static extraction):** `self._config is not None`; `auto_write is None`; `auto_write`

**Source location:** L316–L341（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_kpoints
:members:
:undoc-members:
:show-inheritance:
```
