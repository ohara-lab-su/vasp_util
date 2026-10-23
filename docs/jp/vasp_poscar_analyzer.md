# vasp_poscar_analyzer — 実装に基づく API Reference

対象ソース: `vasp_poscar_analyzer(4).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspPoscarAnalyzer`

VASP POSCARファイルの解析を行うクラス。

### `__init__`

```python
def __init__(self, poscar: VaspPoscar, logger: Optional[XLogger]=None) -> None
```

**既存 docstring（原文）**

```text
POSCARAnalyzerの初期化。

Args:
    poscar (VaspPoscar): VaspPoscar instance
```

**呼び出す関数・メソッド（静的抽出）:** `XLogger`

**更新するインスタンス属性（直接代入）:** `self._logger`, `self.poscar`

**ソース位置:** L23–L35（添付版）。

### `get_jump_distance`

```python
def get_jump_distance(self, other_analyzer: 'VaspPoscarAnalyzer', site_index: int, pbc: bool=True)
```

**既存 docstring（原文）**

```text
指定した原子サイトの2つのMDステップ間（step1→step2）のジャンプ距離（移動距離）を計算する。
同じグローバルインデックスの原子について、2つの構造間の移動距離を評価する。

Args:
    other_analyzer (VaspPoscarAnalyzer): 比較対象の構造（step2）。
    site_index (int): グローバル原子インデックス（1始まり）。
    pbc (bool): 周期境界条件を適用するか（デフォルト: True）。

Returns:
    float: 指定サイトにおける2ステップ間の実際のジャンプ距離（Å）。
```

**呼び出す関数・メソッド（静的抽出）:** `np.linalg.norm`, `other_analyzer.poscar.get_direct_position`, `self.poscar.get_direct_position`, `self.poscar.get_lattice_vectors`, `self.poscar.get_shortest_pbc_direct_vector`

**return 式（静的抽出）:** `np.linalg.norm(vec_car)`

**主な条件分岐（静的抽出）:** `pbc`

**ソース位置:** L37–L66（添付版）。

### `get_interatomic_distance`

```python
def get_interatomic_distance(self, site_idx1: int, site_idx2: int, pbc: bool=True) -> floating
```

**既存 docstring（原文）**

```text
2つの原子（グローバルサイトインデックス指定）の間の距離（オングストローム単位）を計算します。

Args:
    site_idx1 (int): 原子1のグローバルサイトインデックス（1始まり）。
    site_idx2 (int): 原子2のグローバルサイトインデックス（1始まり）。
    pbc (bool): 周期境界条件を適用するかどうか（デフォルト: True）。

Returns:
    float: cartesian norm, 原子1と原子2の間の距離（オングストローム）。
```

**呼び出す関数・メソッド（静的抽出）:** `np.linalg.norm`, `self.poscar.get_coords_direct`, `self.poscar.get_lattice_vectors`, `self.poscar.get_shortest_pbc_direct_vector`

**return 式（静的抽出）:** `np.linalg.norm(diff_car)`

**主な条件分岐（静的抽出）:** `pbc`

**ソース位置:** L68–L101（添付版）。

### `get_distance_vector`

```python
def get_distance_vector(self, index1: int, index2: int, pbc: bool=True)
```

**既存 docstring（原文）**

```text
周期境界条件を考慮した2点間の距離ベクトルと距離を計算する。

Args:
    index1 (int): 原子1のグローバルインデックス（1始まり, 1-based）。
    index2 (int): 原子2のグローバルインデックス（1始まり, 1-based）。
    pbc (bool): 周期境界条件を考慮するかどうか（デフォルト: True）。

Returns:
    Tuple[np.ndarray, float]: cartesian_norm, 距離ベクトルとそのノルム。
```

**呼び出す関数・メソッド（静的抽出）:** `np.linalg.norm`, `self.poscar.get_coords_direct`, `self.poscar.get_lattice_vectors`, `self.poscar.get_shortest_pbc_direct_vector`

**return 式（静的抽出）:** `(diff_car, diff_car_norm)`

**主な条件分岐（静的抽出）:** `pbc`

**ソース位置:** L103–L147（添付版）。

### `is_jump`

```python
def is_jump(self, other, site_index, threshold, pbc=True) -> bool
```

**既存 docstring（原文）**

```text
指定サイトが他のMDステップでジャンプしたかを判定する。

Args:
    other (VaspPoscarAnalyzer): 比較対象のPOSCARAnalyzer
    site_index (int): サイト番号（1始まり, 1-based）
    threshold (float): 距離のしきい値（Å）
    pbc (bool): 周期境界条件を考慮するか（デフォルト: True）

Returns:
    bool: ジャンプと判定された場合はTrue、そうでなければFalse
```

**呼び出す関数・メソッド（静的抽出）:** `self.get_jump_distance`

**return 式（静的抽出）:** `distance > threshold`

**ソース位置:** L149–L170（添付版）。

### `get_neighbors`

```python
def get_neighbors(self, center_global_idx: int, nn: int, target_elements: Optional[list]=None) -> list
```

**既存 docstring（原文）**

```text
指定した中心原子から対象元素のみ近接原子を探索する。

Args:
    center_global_idx (int): 中心原子のグローバルインデックス（1始まり）。
    nn (int): 取得する近接原子数。
    target_elements (Optional[list]): 対象元素のリスト。Noneなら全元素を対象。

Returns:
    list: (距離, 元素, サイト番号, グローバル番号, 直交座標) のリスト。
```

**呼び出す関数・メソッド（静的抽出）:** `neighbors_with_distance.append`, `neighbors_with_distance.sort`, `np.linalg.norm`, `range`, `self.poscar.apply_pbc_direct`, `self.poscar.get_cartesian_position`, `self.poscar.get_element_by_global_index`, `self.poscar.get_element_site_indices_by_global_index`, `self.poscar.get_fractional_position`, `self.poscar.get_num_atoms`, `self.poscar.get_shortest_pbc_direct_vector`

**return 式（静的抽出）:** `neighbors_with_distance[:nn]`

**主な条件分岐（静的抽出）:** `other_global_idx == center_global_idx`; `target_elements is not None and element not in target_elements`

**ソース位置:** L172–L233（添付版）。

### `get_nearest_neighbors`

```python
def get_nearest_neighbors(self, center_element: str, center_local_site_index: int, max_neighbors: int=5, neighbor_element: Optional[str]=None, pbc: bool=True, filter_by_element: bool=False, cutoff_distance: Optional[float]=None) -> list
```

**既存 docstring（原文）**

```text
指定原子からの近接原子を検索する。

Args:
    center_element (str): 中心原子の種類。
    center_local_site_index (int): 中心原子のサイト番号（1始まり, 1-based）。
    max_neighbors (int): 取得する近接原子数。
    cutoff_distance (float): 閾値(max_neighborsが使われなくて、かつ cutoff_distance が選ばれた時に使われる)
    neighbor_element (Optional[str]): 対象とする原子種（Noneなら全て）。
    pbc (bool): 周期境界条件を考慮するかどうか（デフォルト: True）。
    filter_by_element (bool): Trueの場合、中心元素と同じ元素のみを対象にする（デフォルト: False）。

Returns:
    list: (元素, サイト番号, グローバル番号, 距離, ベクトル) のリスト。
```

**呼び出す関数・メソッド（静的抽出）:** `candidates.append`, `candidates.sort`, `enumerate`, `np.linalg.norm`, `self.poscar.conv_direct_to_cartesian`, `self.poscar.get_atom_indices`, `self.poscar.get_coords_direct`, `self.poscar.get_element_site_indices`, `self.poscar.get_element_site_indices(symbol).index`, `self.poscar.get_global_index`, `self.poscar.get_shortest_pbc_direct_vector`, `zip`

**return 式（静的抽出）:** `[c for c in candidates if c[3] <= cutoff_distance]`; `candidates[:max_neighbors]`

**主な条件分岐（静的抽出）:** `cutoff_distance is not None`; `i == center_idx - 1`; `filter_by_element and symbol != center_element`; `neighbor_element and symbol != neighbor_element`

**ソース位置:** L235–L320（添付版）。

### `get_sorted_neighbors`

```python
def get_sorted_neighbors(self, center_element: str, center_site: int, max_neighbors: int=4, pbc: bool=True) -> list
```

**既存 docstring（原文）**

```text
指定原子の近接原子を距離順に取得する。

Args:
    center_element (str): 中心原子種。
    center_site (int): サイト番号（1始まり, 1-based）。
    max_neighbors (int): 出力する近接原子数。
    pbc (bool): 周期境界条件を考慮するかどうか（デフォルト: True）。

Returns:
    list: 近接原子のリスト。
```

**呼び出す関数・メソッド（静的抽出）:** `enumerate`, `neighbors.append`, `neighbors.sort`, `np.array`, `np.linalg.norm`, `self.poscar.conv_direct_to_cartesian`, `self.poscar.get_atom_indices`, `self.poscar.get_coords_direct`, `self.poscar.get_element_site_indices`, `self.poscar.get_global_index`, `self.poscar.get_shortest_pbc_direct_vector`, `symbol_list.index`

**return 式（静的抽出）:** `neighbors[:max_neighbors]`

**主な条件分岐（静的抽出）:** `i == center_idx - 1`; `pbc`

**ソース位置:** L322–L383（添付版）。

### `print_jump_distances`

```python
def print_jump_distances(self, other_analyzer: 'VaspPoscarAnalyzer', element: str, start_site: int, end_site: int, threshold: float, show_non_jumps: bool=True, pbc: bool=True) -> None
```

**既存 docstring（原文）**

```text
2つの構造間での原子のジャンプ距離を表示する。
この関数では周期境界条件（PBC）を考慮して、原子の移動を実際の最短経路として評価する。
この関数で指定の start から end まで調べて、ジャンプ距離を表示する

Args:
    other_analyzer (VaspPoscarAnalyzer): 比較対象のPOSCARAnalyzer。
    element (str): 対象原子種。
    start_site (int): 開始サイト番号（1始まり）。
    end_site (int): 終了サイト番号（1始まり）。
    threshold (float): しきい値（Å）。
    show_non_jumps (bool): しきい値以下の距離を表示するかどうか。
    pbc (bool): 周期境界条件を考慮するかどうか（デフォルト: True）。
```

**呼び出す関数・メソッド（静的抽出）:** `enumerate`, `print`, `self.get_jump_distance`, `self.poscar.get_element_site_indices`

**主な条件分岐（静的抽出）:** `jumped`; `show_non_jumps`

**ソース位置:** L385–L427（添付版）。

### `get_jump_distance_distribution`

```python
def get_jump_distance_distribution(self, other_analyzer: 'VaspPoscarAnalyzer', element: str, start_site: int, end_site: int, pbc: bool=True) -> List[float]
```

**既存 docstring（原文）**

```text
指定された範囲の原子における、2つのMDステップ間のジャンプ距離（分布）を計算する。

この分布は、2つのMDステップ（構造）間で各原子サイトがどれだけジャンプ（移動）したか、すなわちジャンプ距離（Å）を返す。
ここでの距離は、一般的な移動距離ではなく「2つのMDステップ間でのジャンプ距離」に限定される。

Args:
    other_analyzer (VaspPoscarAnalyzer): 比較対象。
    element (str): 対象原子種。
    start_site (int): 開始サイト番号（1始まり）。
    end_site (int): 終了サイト番号（1始まり）。
    pbc (bool): 周期境界条件を考慮するかどうか。

Returns:
    List[float]: 指定範囲内の各原子に対するジャンプ距離（Å）のリスト。
```

**呼び出す関数・メソッド（静的抽出）:** `self.get_jump_distance`, `self.poscar.get_element_site_indices`

**return 式（静的抽出）:** `jump_distances`

**ソース位置:** L429–L459（添付版）。

### `scan_md_series_for_jumps`

```python
@staticmethod
```

**既存 docstring（原文）**

```text
連続するMDステップ間で指定原子のジャンプを調査する（周期境界条件を考慮）。

Args:
    folder_path (str): POSCARファイルのあるディレクトリ。
    file_template (str): ファイル名のテンプレート（例: "POSCAR_{}"）。
    step_min (int): 比較を始めるMDステップ。
    step_max (int): 比較を終えるMDステップ。
    element (str): 対象とする原子種。
    start_site (int): サイト範囲の開始（1始まり）。
    end_site (int): サイト範囲の終了（1始まり）。
    threshold (float): ジャンプとみなす距離のしきい値。
    show_non_jumps (bool): しきい値以下の距離を表示するかどうか。

Returns:
    list[tuple[int, int, Any]]: ジャンプの情報を含むリスト。
```

**呼び出す関数・メソッド（静的抽出）:** `Poscar`, `VaspPoscarAnalyzer`, `a1.get_jump_distance`, `a1.print_jump_distances`, `enumerate`, `file_template.format`, `jump_records.append`, `os.path.exists`, `os.path.join`, `poscar1.get_element_site_indices`, `print`, `range`

**return 式（静的抽出）:** `jump_records`

**主な条件分岐（静的抽出）:** `not os.path.exists(file1) or not os.path.exists(file2)`; `jumped`; `show_non_jumps`

**ソース位置:** L462–L547（添付版）。

### `check_jump_between_two_steps`

```python
@staticmethod
```

**既存 docstring（原文）**

```text
2つのPOSCARファイル間でジャンプを検出し表示するユーティリティ。

Args:
    poscar1_path (str): 1つ目のPOSCARファイル。
    poscar2_path (str): 2つ目のPOSCARファイル。
    element (str): 対象の原子種。
    start_site (int): サイト範囲の開始（1始まり）。
    end_site (int): サイト範囲の終了（1始まり）。
    threshold (float): ジャンプ判定の距離しきい値（Å）。
    show_non_jumps (bool): しきい値以下の距離を表示するかどうか。
```

**呼び出す関数・メソッド（静的抽出）:** `Poscar`, `VaspPoscarAnalyzer`, `a1.print_jump_distances`, `print`

**ソース位置:** L550–L582（添付版）。

### `trace_site_motion_over_md_steps`

```python
@staticmethod
```

**既存 docstring（原文）**

```text
指定したサイトの原子が、各MDステップ間でどれだけ動いたかを追跡表示する。

Args:
    folder_path (str): POSCARファイルのディレクトリ。
    site_index (int): 追跡するグローバル原子インデックス（1始まり）。
    element (str): 原子種（例: "Li"）。
    step_min (int): 開始ステップ番号。
    step_max (int): 終了ステップ番号。
    file_template (str): ファイル名テンプレート（例: "POSCAR_{}"）。
    threshold (float): ジャンプとみなす距離のしきい値（Å）。
    show_non_jumps (bool): しきい値以下の距離を表示するかどうか。
```

**呼び出す関数・メソッド（静的抽出）:** `Poscar`, `VaspPoscarAnalyzer`, `a1.get_jump_distance`, `file_template.format`, `os.path.exists`, `os.path.join`, `print`, `range`

**主な条件分岐（静的抽出）:** `not os.path.exists(file1) or not os.path.exists(file2)`; `dist > threshold`; `show_non_jumps`

**ソース位置:** L585–L631（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_poscar_analyzer
:members:
:undoc-members:
:show-inheritance:
```
