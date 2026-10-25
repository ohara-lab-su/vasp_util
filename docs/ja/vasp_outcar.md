# vasp_outcar — 実装に基づく API Reference

対象ソース: `vasp_outcar(3).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspOutcar`

VASP OUTCAR から
  - エネルギー (free, without entropy, sigma->0)
  - 原子位置
  - 力
  - 原子ごとの磁気モーメント (s, p, d, total)
  - 全体の磁気モーメント (total)
を取り出して保持するクラス。

イオンステップの配列長は (NSW + 1) とする:
  NSW = 0 -> ステップ 0 のみ (要素数 1)
  NSW = 1 -> ステップ 0,1    (要素数 2)
  一般に -> ステップ 0..NSW (要素数 NSW+1)

### `__init__`

```python
def __init__(self, filename: str, logger: Optional[XLogger]=None) -> None
```

**既存 docstring（原文）**

```text
Args:
    filename (str):  OUTCAR (パス指定OK)
    logger:
```

**呼び出す関数・メソッド（静的抽出）:** `RuntimeError`, `XLogger`, `f.readlines`, `np.full`, `np.zeros`, `open`, `self._detect_finished`, `self._guess_nions`, `self._parse_energy`, `self._parse_magmom`, `self._parse_pos_force`, `self._read_int`, `self._shrink_ion_steps`

**明示的に送出する例外:** `RuntimeError(f'OUTCAR seems not finished: {self.filename}')`

**更新するインスタンス属性（直接代入）:** `self._logger`, `self.lines`, `self.nions`, `self.num_ion_steps`

**主な条件分岐（静的抽出）:** `not self.finished`; `self.num_ion_steps < 1`; `self.nions <= 0`

**ソース位置:** L30–L90（添付版）。

### `_read_int`

```python
def _read_int(self, key: str, default: int=0) -> int
```

**既存 docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**呼び出す関数・メソッド（静的抽出）:** `int`, `m.group`, `re.search`

**return 式（静的抽出）:** `default`; `int(m.group(1))`

**主な条件分岐（静的抽出）:** `m`

**ソース位置:** L95–L101（添付版）。

### `_guess_nions`

```python
def _guess_nions(self) -> int
```

**既存 docstring（原文）**

```text
NIONS 行が見つからない場合のフォールバック: 最初の
POSITION TOTAL-FORCE ブロックから原子数を推定する。
```

**呼び出す関数・メソッド（静的抽出）:** `len`, `line.split`

**return 式（静的抽出）:** `count`

**主な条件分岐（静的抽出）:** `'POSITION' in line and 'TOTAL-FORCE' in line`; `reading`; `'drift' in line or '--------' in line`; `len(parts) >= 6`

**ソース位置:** L103–L126（添付版）。

### `_parse_energy`

```python
def _parse_energy(self) -> None
```

**既存 docstring（原文）**

```text
"FREE ENERGIE OF THE ION-ELECTRON SYSTEM" ブロックから
free energy (TOTEN), without entropy, sigma->0 を取り出す。
```

**呼び出す関数・メソッド（静的抽出）:** `float`, `m_e0.group`, `m_sigma.group`, `m_toten.group`, `max`, `re.search`

**更新するインスタンス属性（直接代入）:** `self.actual_ion_steps`

**主な条件分岐（静的抽出）:** `ion_index >= 0`; `'FREE ENERGIE OF THE ION-ELECTRON SYSTEM' in line`; `ion_index < 0 or ion_index >= self.num_ion_steps`; `m_toten`; `m_e0`; `m_sigma`; `iter_index < self.nelm`; `iter_index > self.iter_count[ion_index]`

**ソース位置:** L131–L171（添付版）。

### `_parse_pos_force`

```python
def _parse_pos_force(self) -> None
```

**既存 docstring（原文）**

```text
"POSITION" "TOTAL-FORCE" ブロックから
位置と力を取り出す。
```

**呼び出す関数・メソッド（静的抽出）:** `len`, `line.split`, `map`, `max`

**更新するインスタンス属性（直接代入）:** `self.actual_ion_steps`

**主な条件分岐（静的抽出）:** `'POSITION' in line and 'TOTAL-FORCE' in line`; `not reading`; `'drift' in line or '--------' in line`; `len(parts) < 6`; `atom_index >= self.nions`; `ion_index >= self.num_ion_steps`; `ion_index >= 0`

**ソース位置:** L176–L219（添付版）。

### `_parse_magmom`

```python
def _parse_magmom(self) -> None
```

**既存 docstring（原文）**

```text
"magnetization (x)" ブロックから
原子ごとの (s, p, d, total) と
total magnetization を取り出す。
```

**呼び出す関数・メソッド（静的抽出）:** `float`, `len`, `line.split`, `m_tot.group`, `max`, `parts[0].isdigit`, `re.search`

**更新するインスタンス属性（直接代入）:** `self.actual_ion_steps`

**主な条件分岐（静的抽出）:** `'magnetization (x)' in line`; `not reading`; `len(parts) == 5 and parts[0].isdigit()`; `'total magnetization' in line`; `ion_index >= self.num_ion_steps`; `atom_index < self.nions`; `m_tot`

**ソース位置:** L224–L281（添付版）。

### `_shrink_ion_steps`

```python
def _shrink_ion_steps(self) -> None
```

**既存 docstring（原文）**

```text
実際に検出できたイオンステップ数まで配列を切り詰める。
NSW=0 の場合も最低 1 にする。
```

**更新するインスタンス属性（直接代入）:** `self.actual_ion_steps`, `self.energy_e0`, `self.energy_sigma0`, `self.energy_toten`, `self.forces`, `self.iter_count`, `self.magmom_atom`, `self.magmom_total`, `self.num_ion_steps`, `self.positions`

**主な条件分岐（静的抽出）:** `self.actual_ion_steps <= 0`; `self.actual_ion_steps > self.num_ion_steps`; `used < self.num_ion_steps`

**ソース位置:** L286–L308（添付版）。

### `get_ionstep_count`

```python
def get_ionstep_count(self) -> int
```

**既存 docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**return 式（静的抽出）:** `self.num_ion_steps`

**ソース位置:** L313–L314（添付版）。

### `get_iter_count`

```python
def get_iter_count(self, ionstep: int) -> int
```

**既存 docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**呼び出す関数・メソッド（静的抽出）:** `int`

**return 式（静的抽出）:** `int(self.iter_count[ionstep])`; `0`

**主な条件分岐（静的抽出）:** `ionstep < 0 or ionstep >= self.num_ion_steps`

**ソース位置:** L316–L319（添付版）。

### `get_energy`

```python
def get_energy(self, ionstep: int, iterstep: int, *, mode: str='e0') -> Optional[float]
```

**既存 docstring（原文）**

```text
指定イオンステップ・指定 iter のエネルギーを返す。

mode:
    "e0"     : energy without entropy
    "toten"  : free energy TOTEN
    "sigma0" : energy(sigma->0)
```

**呼び出す関数・メソッド（静的抽出）:** `float`, `np.isnan`

**return 式（静的抽出）:** `float(val)`; `None`

**主な条件分岐（静的抽出）:** `ionstep < 0 or ionstep >= self.num_ion_steps or iterstep < 0 or (iterstep >= self.iter_count[ionstep])`; `mode == 'e0'`; `np.isnan(val)`; `mode == 'toten'`; `mode == 'sigma0'`

**ソース位置:** L321–L355（添付版）。

### `get_energy_matrix`

```python
def get_energy_matrix(self, mode: str='e0') -> np.ndarray
```

**既存 docstring（原文）**

```text
イオンステップ × iter のエネルギー配列を返す。
未使用部分は NaN を含む。
```

**呼び出す関数・メソッド（静的抽出）:** `int`, `mat.copy`, `np.empty`, `self.iter_count.max`

**return 式（静的抽出）:** `mat.copy()`; `np.empty((0, 0), dtype=float)`; `np.empty((self.num_ion_steps, 0), dtype=float)`

**主な条件分岐（静的抽出）:** `self.num_ion_steps == 0`; `max_iter <= 0`; `mode == 'e0'`; `mode == 'toten'`; `mode == 'sigma0'`

**ソース位置:** L357–L378（添付版）。

### `get_energy_flat`

```python
def get_energy_flat(self, mode: str='e0') -> np.ndarray
```

**既存 docstring（原文）**

```text
イオンステップと iter をすべてまとめた 1 次元配列を返す。
NaN は除く。
```

**呼び出す関数・メソッド（静的抽出）:** `np.isnan`, `self.get_energy_matrix`

**return 式（静的抽出）:** `mat[~np.isnan(mat)]`

**ソース位置:** L380–L386（添付版）。

### `get_energy_ionstep`

```python
def get_energy_ionstep(self, mode: str='e0') -> np.ndarray
```

**既存 docstring（原文）**

```text
各イオンステップごとの「最後の iter のエネルギー」を
1 次元配列で返す。
```

**呼び出す関数・メソッド（静的抽出）:** `int`, `np.empty`, `np.full`, `range`

**return 式（静的抽出）:** `vals`; `np.empty(0, dtype=float)`

**主な条件分岐（静的抽出）:** `self.num_ion_steps == 0`; `n_iter <= 0`; `mode == 'e0'`; `mode == 'toten'`; `mode == 'sigma0'`

**ソース位置:** L388–L413（添付版）。

### `get_positions`

```python
def get_positions(self, ionstep: int) -> np.ndarray
```

**既存 docstring（原文）**

```text
指定イオンステップの原子位置 (nions, 3) を返す。
```

**呼び出す関数・メソッド（静的抽出）:** `np.empty`, `self.positions[ionstep].copy`

**return 式（静的抽出）:** `self.positions[ionstep].copy()`; `np.empty((0, 3), dtype=float)`

**主な条件分岐（静的抽出）:** `ionstep < 0 or ionstep >= self.num_ion_steps`

**ソース位置:** L415–L421（添付版）。

### `get_forces`

```python
def get_forces(self, ionstep: int) -> np.ndarray
```

**既存 docstring（原文）**

```text
指定イオンステップの力 (nions, 3) を返す。
```

**呼び出す関数・メソッド（静的抽出）:** `np.empty`, `self.forces[ionstep].copy`

**return 式（静的抽出）:** `self.forces[ionstep].copy()`; `np.empty((0, 3), dtype=float)`

**主な条件分岐（静的抽出）:** `ionstep < 0 or ionstep >= self.num_ion_steps`

**ソース位置:** L423–L429（添付版）。

### `get_magmom_atom`

```python
def get_magmom_atom(self, ionstep: int) -> np.ndarray
```

**既存 docstring（原文）**

```text
指定イオンステップの原子ごとの磁気モーメント
(nions, 4) を返す。列順は (s, p, d, total)。
```

**呼び出す関数・メソッド（静的抽出）:** `np.empty`, `self.magmom_atom[ionstep].copy`

**return 式（静的抽出）:** `self.magmom_atom[ionstep].copy()`; `np.empty((0, 4), dtype=float)`

**主な条件分岐（静的抽出）:** `ionstep < 0 or ionstep >= self.num_ion_steps`

**ソース位置:** L431–L438（添付版）。

### `get_magmom_total`

```python
def get_magmom_total(self, ionstep: int) -> Optional[float]
```

**既存 docstring（原文）**

```text
指定イオンステップの全体磁気モーメント total を返す。
```

**呼び出す関数・メソッド（静的抽出）:** `float`, `np.isnan`

**return 式（静的抽出）:** `float(val)`; `None`

**主な条件分岐（静的抽出）:** `ionstep < 0 or ionstep >= self.num_ion_steps`; `np.isnan(val)`

**ソース位置:** L440–L449（添付版）。

### `_detect_finished`

```python
def _detect_finished(self) -> bool
```

**既存 docstring（原文）**

```text
OUTCAR が「正常終了」しているかどうかの簡易判定を行う。

以下のような行の存在で判定する:
  - "General timing and accounting informations for this job"
  - "Voluntary context switches"

これらが末尾付近に無い場合は、未完了とみなす。
```

**呼び出す関数・メソッド（静的抽出）:** `reversed`

**return 式（静的抽出）:** `False`; `True`

**主な条件分岐（静的抽出）:** `'General timing and accounting informations for this job' in line`; `'Voluntary context switches' in line`

**ソース位置:** L451–L467（添付版）。

### `is_finalized`

```python
def is_finalized(self) -> bool
```

**既存 docstring（原文）**

```text
OUTCAR が正常終了しているかどうかを返す。
```

**呼び出す関数・メソッド（静的抽出）:** `bool`

**return 式（静的抽出）:** `bool(self.finished)`

**ソース位置:** L469–L473（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_outcar
:members:
:undoc-members:
:show-inheritance:
```
