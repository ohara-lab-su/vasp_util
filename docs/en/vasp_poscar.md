# vasp_poscar — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `vasp_poscar`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `vasp_poscar(5).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspPoscar`

VASP POSCARファイルの解析を行うクラス。

疑似プライベート化された内部変数値は 0-base
getter でアクセスさせる外部 I/F は 1-base

### `__init__`

```python
def __init__(self, poscar_path: str, verbose: bool=False) -> None
```

**Original docstring (source language)**

```text
POSCARAnalyzerの初期化。

Args:
    poscar_path (str): POSCARファイルのパス。
```

**Calls (static AST extraction):** `self._read_poscar`

**Source location:** L21–L49（添付版）。

### `_read_poscar`

```python
def _read_poscar(self) -> None
```

**Original docstring (source language)**

```text
POSCARファイルを読み込んで構造情報を初期化する。
```

**Calls (static AST extraction):** `ValueError`, `abs`, `any`, `coord_mode.startswith`, `coord_mode_line.startswith`, `element.split`, `f.readlines`, `float`, `len`, `line.split`, `lines[1].split`, `lines[5].split`, `lines[6].split`, `lines[7].strip`, `lines[7].strip().lower`, `lines[8].strip`, `lines[8].strip().lower`, `lines[i].split`, `list`, `map`, `np.all`, `np.array`, `np.full`, `np.isfinite`, `np.linalg.det`, `np.linalg.inv`, `open`, `range`, `scale_values.copy`, `self._atom_indices.append`, `self._element_site_indices[element].append`, `sum`, `zip`

**Explicitly raised exceptions:** `ValueError('POSCAR lattice vectors must be linearly independent')`; `ValueError('POSCAR must contain three lattice vectors')`; `ValueError('POSCAR scale factor must be nonzero')`; `ValueError('POSCAR scale factors must be finite')`; `ValueError('POSCAR scale line must contain one or three numbers')`; `ValueError('Three POSCAR scale factors must be positive')`

**Instance attributes assigned directly:** `self._atom_indices`, `self._coords_direct`, `self._element_site_indices`, `self._elements_index`, `self._is_direct`, `self._lattice`, `self._scale`, `self._scale_factors`

**Principal conditions (static extraction):** `len(scale_values) != 1 and len(scale_values) != 3`; `not np.all(np.isfinite(scale_values))`; `lattice_unscaled.shape != (3, 3)`; `not np.isfinite(determinant) or abs(determinant) < 1e-14`; `len(scale_values) == 3`; `coord_mode_line.startswith('s')`; `not self._is_direct`; `any((value <= 0.0 for value in scale_values))`; `scale_value == 0.0`; `scale_value < 0.0`

**Source location:** L51–L164（添付版）。

### `apply_pbc_cartesian`

```python
def apply_pbc_cartesian(self, vec)
```

**Original docstring (source language)**

```text
cartesian に PBC 適応 --> cartesian With PBC

周期境界条件を適用して、格子ベクトル(位置ベクトル差) cartesian に
基づく最近接の変位ベクトルを返す。

vec = A-vector - B-vector (それぞれ周期境界条件を満たす)

Args:
    vec (np.ndarray): cartesian 3次元の変位ベクトル
                      シミュレーションセル内の2つの原子（または点）の
                      位置ベクトルの差(r_j − r_i) を
                      デカルト座標（通常のx, y, z座標）で表したもの

Returns:
    np.ndarray: direct 周期境界条件を考慮した変位ベクトル
```

**Calls (static AST extraction):** `np.linalg.solve`, `np.round`

**Return expressions (static extraction):** `frac`

**Source location:** L193–L215（添付版）。

### `apply_pbc_direct`

```python
def apply_pbc_direct(self, vec)
```

**Original docstring (source language)**

```text
direct --> direct with PBC

direct 座標系(vec) を入力として、周期境界条件を適当
```

**Calls (static AST extraction):** `np.round`

**Return expressions (static extraction):** `vec`

**Source location:** L217–L224（添付版）。

### `apply_pbc_shortest_direct_vector`

```python
def apply_pbc_shortest_direct_vector(self, vec_direct)
```

**Original docstring (source language)**

```text
PBC補正を適用して最短距離ベクトルを取得する。

Args:
    vec_direct (np.ndarray): フラクショナル座標系の差分ベクトル。

Returns:
    np.ndarray: PBC適用後の最短距離ベクトル（direct 系）。
```

**Calls (static AST extraction):** `np.array`, `np.linalg.norm`, `np.round`, `range`

**Return expressions (static extraction):** `shortest_vec`

**Principal conditions (static extraction):** `dist < min_dist`

**Source location:** L226–L269（添付版）。

### `get_shortest_pbc_direct_vector`

```python
def get_shortest_pbc_direct_vector(self, A_direct: np.ndarray, B_direct: np.ndarray)
```

**Original docstring (source language)**

```text
direct
PBCを考慮した最短距離ベクトルを計算する。

Args:
    A_direct (np.ndarray): A点のフラクショナル座標。
    B_direct (np.ndarray): B点のフラクショナル座標。

Returns:
    np.ndarray: direct系 PBC補正済みの最短距離ベクトル。
```

**Calls (static AST extraction):** `self.apply_pbc_shortest_direct_vector`

**Return expressions (static extraction):** `delta_direct_pbc`

**Source location:** L271–L295（添付版）。

### `is_direct`

```python
@property
```

**Original docstring (source language)**

```text
POSCARファイルの座標形式が Direct 形式かどうかを返す。

Returns:
    bool: Direct形式ならば True、そうでなければ False
```

**Return expressions (static extraction):** `self._is_direct`

**Source location:** L298–L305（添付版）。

### `get_filename`

```python
def get_filename(self) -> str
```

**Original docstring (source language)**

```text
poscar name
```

**Return expressions (static extraction):** `self._filename`

**Source location:** L307–L309（添付版）。

### `get_label`

```python
def get_label(self) -> str
```

**Original docstring (source language)**

```text
コメント
```

**Return expressions (static extraction):** `self._label`

**Source location:** L311–L313（添付版）。

### `get_comment`

```python
def get_comment(self) -> str
```

**Original docstring (source language)**

```text
コメント
```

**Return expressions (static extraction):** `self._label`

**Source location:** L315–L317（添付版）。

### `get_lattice_constant`

```python
def get_lattice_constant(self) -> float
```

**Original docstring (source language)**

```text
有効な一様倍率を返す。3成分指定時は互換値1.0を返す。
```

**Return expressions (static extraction):** `self._scale`

**Source location:** L319–L323（添付版）。

### `get_scale`

```python
def get_scale(self) -> Any
```

**Original docstring (source language)**

```text
POSCARの元のスケール指定を返す（単一値または3成分リスト）。
```

**Calls (static AST extraction):** `len`, `self._scale_specification.copy`

**Return expressions (static extraction):** `self._scale_specification[0]`; `self._scale_specification.copy()`

**Principal conditions (static extraction):** `len(self._scale_specification) == 3`

**Source location:** L325–L331（添付版）。

### `get_inv_lattice`

```python
def get_inv_lattice(self)
```

**Original docstring (source language)**

```text
scale も含めた
```

**Calls (static AST extraction):** `np.linalg.inv`

**Return expressions (static extraction):** `np.linalg.inv(self._lattice)`

**Source location:** L333–L335（添付版）。

### `get_inv_lattice_vectors`

```python
def get_inv_lattice_vectors(self)
```

**Original docstring (source language)**

```text
scale も含めた
```

**Calls (static AST extraction):** `np.linalg.inv`

**Return expressions (static extraction):** `np.linalg.inv(self._lattice)`

**Source location:** L337–L339（添付版）。

### `get_lattice_vectors`

```python
def get_lattice_vectors(self) -> np.ndarray
```

**Original docstring (source language)**

```text
格子ベクトルを返す。
(scale factor が含んでいる前提)

Returns:
    np.ndarray: 3×3の格子行列
```

**Return expressions (static extraction):** `self._lattice`

**Source location:** L341–L349（添付版）。

### `conv_direct_to_cartesian`

```python
def conv_direct_to_cartesian(self, direct_vec)
```

**Original docstring (source language)**

```text
lattice には scale が入っている前提
```

**Return expressions (static extraction):** `direct_vec @ self._lattice`

**Source location:** L351–L353（添付版）。

### `conv_cartesian_to_direct`

```python
def conv_cartesian_to_direct(self, cartesian_vec)
```

**Original docstring (source language)**

```text
lattice には scale が入っている前提
```

**Calls (static AST extraction):** `np.linalg.inv`

**Return expressions (static extraction):** `cartesian_vec @ inv_lattice`

**Source location:** L355–L358（添付版）。

### `get_elements`

```python
def get_elements(self)
```

**Original docstring (source language)**

```text
POSCAR の元素記号の一行(POSCARの行そのまま)
```

**Return expressions (static extraction):** `self._elements`

**Source location:** L360–L362（添付版）。

### `get_elements_index`

```python
def get_elements_index(self)
```

**Original docstring (source language)**

```text
POSCAR の元素記号に対応するサイトない原子数の一覧(POSCARの行そのまま)
```

**Return expressions (static extraction):** `self._elements_index`

**Source location:** L364–L366（添付版）。

### `get_atom_indices`

```python
def get_atom_indices(self) -> List[str]
```

**Original docstring (source language)**

```text
原子種(Liが3つでPが2つならば、Li,Li,Li,P,P と入る)
```

**Return expressions (static extraction):** `self._atom_indices`

**Source location:** L368–L370（添付版）。

### `get_num_atoms`

```python
def get_num_atoms(self) -> int
```

**Original docstring (source language)**

```text
このPOSCAR内の全原子数を返す。

注意:
    - この関数は原子の「個数（サイズ）」を返すものであり、インデックスではない。
    - Pythonの range() を使ってグローバルインデックスでループ処理を行う場合には、
      `range(1, poscar.get_num_atoms() + 1)` のように書いて末尾を含める必要がある。
    - これは range() の仕様によるものであり、1-based / 0-based の議論とは直接関係しない。

Returns:
    int: 総原子数
```

**Calls (static AST extraction):** `len`

**Return expressions (static extraction):** `len(self._coords_direct)`

**Source location:** L372–L385（添付版）。

### `get_coords_direct`

```python
def get_coords_direct(self, global_index: Optional[int]=None) -> Optional[np.ndarray]
```

**Original docstring (source language)**

```text
内部座標リスト（Direct座標）を返す。

Args:
    global_index (int, optional): 1始まりのグローバルインデックス。None の場合は全体を返す。

Returns:
    np.ndarray or Optional[np.ndarray]: 指定された原子の分数座標、または全体の配列
```

**Return expressions (static extraction):** `self._coords_direct`; `self._coords_direct[global_index - 1]`

**Principal conditions (static extraction):** `global_index is None`

**Source location:** L391–L406（添付版）。

### `get_direct_position`

```python
def get_direct_position(self, global_idx) -> np.ndarray
```

**Original docstring (source language)**

```text
1base で得る
```

**Calls (static AST extraction):** `self.get_fractional_position`

**Return expressions (static extraction):** `self.get_fractional_position(global_idx)`

**Source location:** L408–L410（添付版）。

### `get_fractional_position`

```python
def get_fractional_position(self, global_idx) -> np.ndarray
```

**Original docstring (source language)**

```text
指定したglobal indexに対応する分数座標を返す。

Args:
    global_idx (int): グローバルインデックス(1から)
Returns:
    np.ndarray: 分数座標 (3次元ベクトル)
```

**Return expressions (static extraction):** `self._coords_direct[global_idx - 1]`

**Source location:** L412–L422（添付版）。

### `get_cartesian_position`

```python
def get_cartesian_position(self, global_index: int) -> np.ndarray
```

**Original docstring (source language)**

```text
指定したインデックスの原子の直交座標を返す。

Args:
    global_index (int): 原子のグローバルインデックス（1始まり, 1-based）。

Returns:
    np.ndarray: 直交座標 (Å)
```

**Return expressions (static extraction):** `self._coords_direct[global_index - 1] @ self._lattice`

**Source location:** L431–L442（添付版）。

### `get_local_index_by_global_index`

```python
def get_local_index_by_global_index(self, global_idx: int) -> int
```

**Original docstring (source language)**

```text
グローバルインデックスから元素種ごとのローカルサイト番号（1始まり, 1-based）を返す。

Args:
    global_idx (int): グローバルインデックス（1始まり）

Returns:
    int: 元素種内のローカルインデックス（1始まり）
```

**Calls (static AST extraction):** `self.get_element_site_indices_by_global_index`

**Return expressions (static extraction):** `self.get_element_site_indices_by_global_index(global_idx)`

**Source location:** L448–L458（添付版）。

### `get_global_index`

```python
def get_global_index(self, element: str, site_index: int) -> int
```

**Original docstring (source language)**

```text
指定した原子種とそのサイト番号から、グローバルインデックス（1始まり）を返す。

Args:
    element (str): 原子種（例: "Li"）。
    site_index (int): 原子種内のサイト番号（1始まり, 1-based）。

Returns:
    int: 全体の原子リストにおけるグローバルインデックス（1始まり, 1-based）。
```

**Return expressions (static extraction):** `self._element_site_indices[element][site_index - 1] + 1`

**Source location:** L460–L472（添付版）。

### `get_element_by_global_index`

```python
def get_element_by_global_index(self, global_idx: int) -> str
```

**Original docstring (source language)**

```text
グローバルインデックス（1始まり）から元素を返す。

Args:
    global_idx (int): グローバルインデックス（1始まり）

Returns:
    str: 元素記号（例: "Li", "P", "S"）
```

**Calls (static AST extraction):** `IndexError`, `len`

**Explicitly raised exceptions:** `IndexError(f'global_idx {global_idx} is out of bounds (1-based)')`

**Return expressions (static extraction):** `self._atom_indices[global_idx - 1]`

**Principal conditions (static extraction):** `global_idx < 1 or global_idx > len(self._atom_indices)`

**Source location:** L478–L490（添付版）。

### `get_element_site_indices`

```python
def get_element_site_indices(self, element: str) -> List[int]
```

**Original docstring (source language)**

```text
指定された元素に対応するサイトインデックス（1始まり, 1-based）を返す。

Args:
    element (str): 原子種（例: "Li"）

Returns:
    list[int]: 指定原子種に対応する原子サイトのインデックス（1始まり, 1-based）
```

**Calls (static AST extraction):** `e.strip`, `e.strip().capitalize`, `element.strip`, `element.strip().capitalize`, `enumerate`

**Return expressions (static extraction):** `[i + 1 for i, e in enumerate(self._atom_indices) if e.strip().capitalize() == element.strip().capitalize()]`

**Source location:** L492–L509（添付版）。

### `get_element_site_indices_by_global_index`

```python
def get_element_site_indices_by_global_index(self, global_idx: int) -> int
```

**Original docstring (source language)**

```text
グローバルインデックスから元素種ごとのサイト番号（1始まり, 1-based）を返す。

Args:
    global_idx (int): グローバルインデックス（1始まり）

Returns:
    int: 元素種内でのサイト番号（1始まり）
```

**Calls (static AST extraction):** `local_list.index`, `self.get_element_by_global_index`

**Return expressions (static extraction):** `local_list.index(target) + 1`

**Source location:** L511–L524（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_poscar
:members:
:undoc-members:
:show-inheritance:
```
