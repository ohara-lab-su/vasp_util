# vasp — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `vasp`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `vasp(7).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `Vasp`

RMD-DFT  のため VASP構造作成 / VASPパラメータ入力 / 実行 /解析用のクラス

### `__init__`

```python
def __init__(self, *, incar_name: str='INCAR', kpoints_name: str='KPOINTS', vasp_log: Optional[VaspLog]=None, vasp_incar: Optional[VaspIncar]=None, vasp_kpoints: Optional[VaspKpoints]=None, config: Optional[Config]=None, logger: Optional[XLogger]=None, auto_write: bool=True, vasp_name: Optional[str]=None, dft_bin: Optional[str]=None, mpi_cmd: Optional[str]=None, mpi_flag: Optional[str]=None, num_procs: Optional[int]=None, job_cmd: Optional[str]=None, make_default_input: bool=False) -> None
```

**Original docstring (source language)**

```text
config インスタンを与えると終わり

(*) 歴史的経緯で複雑になっているが、config 与えれば終わり

Args:
    incar_name (str): INCAR
    kpoints_name (str): KPOINTS
    vasp_log (VaspLog): VASP の log 解析管理 instance
    vasp_incar (VaspIncar):
    vasp_kpoints (VaspKpoints):
    config (Config): 全てのインスタンスが同じ Config
    logger (XLogger): ろがー、全てのインスタンスが同じ XLogger
    auto_write (bool):
    vasp_name (str): POSCAR などに関連する系の識別名（例: "aaa.vasp" or "POSCAR）
    dft_bin (str): 実行バイナリ（例: "vasp_std"）
    mpi_cmd (str): 例 "mpirun" (configがあればいらない)
    mpi_flag (str): 例 "-np" (configがあればいらない)
    num_procs (int): 並列数 (configがあればいらない)
    job_cmd (str): ジョブ投入コマンド（None ならローカル実行）
    make_default_input (bool): インプットファイルを自動作成(既存があるときはそっちを優先)
```

**Calls (static AST extraction):** `Config`, `VaspIncar`, `VaspKpoints`, `VaspLog`, `XLogger`, `os.path.exists`, `self._incar.set`, `self._incar_defaults.items`, `self._kpoints.set_grid`, `self._kpoints.set_mode`, `self._kpoints.set_shift`, `self._kpoints.write`, `self._logger.debug`, `self._logger.info`

**Instance attributes assigned directly:** `self._logger`, `self.dft_bin`, `self.job_cmd`, `self.mpi_cmd`, `self.mpi_flag`, `self.num_procs`

**Principal conditions (static extraction):** `config`; `vasp_name is None`; `vasp_log is None`; `vasp_incar is None`; `vasp_kpoints is None`; `make_default_input`; `not os.path.exists(self.incar_name)`; `not os.path.exists(self.kpoints_name)`; `dft_bin is not None`; `mpi_cmd is not None`

**Source location:** L44–L204（添付版）。

### `get_tag`

```python
def get_tag(self, key: str)
```

**Original docstring (source language)**

```text
INCAR の値を取得
```

**Calls (static AST extraction):** `self._incar.get`

**Return expressions (static extraction):** `self._incar.get(key)`

**Source location:** L207–L209（添付版）。

### `set_tag`

```python
def set_tag(self, key: str, value: Any) -> None
```

**Original docstring (source language)**

```text
INCAR の値を設定

Example:
    set_tag("NSW", 1)

Args:
    key (str):
    value (Any):

Returns:
    None:
```

**Calls (static AST extraction):** `isinstance`, `self._incar.set`, `str`

**Principal conditions (static extraction):** `isinstance(value, int)`; `isinstance(value, float)`

**Source location:** L211–L234（添付版）。

### `remove_tag`

```python
def remove_tag(self, key: str)
```

**Original docstring (source language)**

```text
INCAR の項目を削除
```

**Calls (static AST extraction):** `self._incar.remove`

**Source location:** L236–L238（添付版）。

### `reload_incar`

```python
def reload_incar(self)
```

**Original docstring (source language)**

```text
INCAR を再読込
```

**Calls (static AST extraction):** `self._incar.reload`

**Source location:** L240–L242（添付版）。

### `export_incar_dict`

```python
def export_incar_dict(self)
```

**Original docstring (source language)**

```text
INCAR を辞書で取得
```

**Calls (static AST extraction):** `self._incar.export_dict`

**Return expressions (static extraction):** `self._incar.export_dict()`

**Source location:** L244–L246（添付版）。

### `export_kpoints_dict`

```python
def export_kpoints_dict(self)
```

**Original docstring (source language)**

```text
KPOINTS を辞書で取得
```

**Calls (static AST extraction):** `self._kpoints.export_dict`

**Return expressions (static extraction):** `self._kpoints.export_dict()`

**Source location:** L248–L250（添付版）。

### `init`

```python
def init(self, cfg_name: Optional[str]=None) -> None
```

**Original docstring (source language)**

```text
POSCAR から cfg を作る

Args:
    cfg_name (str): 出力する cfg_name.cfg

Returns:
```

**Calls (static AST extraction):** `self._logger.info`

**Source location:** L256–L269（添付版）。

### `cat`

```python
@staticmethod
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `f.read`, `open`, `os.path.exists`, `print`

**Principal conditions (static extraction):** `os.path.exists(filename)`

**Source location:** L280–L285（添付版）。

### `preprocess`

```python
def preprocess(self, vasp_name: Optional[str]=None, element_info: Optional[Union[str, Sequence[str]]]=None) -> bool
```

**Original docstring (source language)**

```text
vasp 前処理

基本的に Vasp Class は相手がなんであれ動くようにする
それは入力が常に VASP であることを仮定していて、
相手のプログラム側の postprocess or convert してから動かすことを全手とする

*) 構造変換関係は Vasp() では自動で preprocess に入れない。誤解が生じやすい

Args:
    vasp_name (str): xxx.vasp 名前における xxxに相当する名前
    element_info (str):

Returns:
    bool:
```

**Calls (static AST extraction):** `os.getcwd`, `os.path.exists`, `os.path.join`, `self._logger.error`, `self._logger.info`, `sys.exit`

**Return expressions (static extraction):** `True`

**Principal conditions (static extraction):** `vasp_name is None`; `not os.path.exists(target_path)`

**Source location:** L287–L327（添付版）。

### `postprocess`

```python
def postprocess(self, log_dir: Optional[str]=None, cfg_name: Optional[str]=None) -> bool
```

**Original docstring (source language)**

```text
後処理

1) DATA-collect
2) BACKUP
3) CONTCAR --> POSCAR
4) CONTCAR --> CFG (for RMC_POT)


Args:
    log_dir (str): VASP_log_dir_name デフォルトは config() から dft_log_dir を取得
    cfg_name (str): POSCAR -> cfg_name.cfg (デフォルトは config() から cfg_name を取得する)

Returns:
    bool:
```

**Calls (static AST extraction):** `os.path.exists`, `os.path.getsize`, `self._logger.error`, `self._logger.info`, `self._vasp_log.backup_result`, `self._vasp_log.collect_result`, `self.contcar2cfg`, `shutil.copyfile`

**Return expressions (static extraction):** `True`; `False`

**Principal conditions (static extraction):** `log_dir is None`; `cfg_name is None`; `not os.path.exists('CONTCAR') or os.path.getsize('CONTCAR') == 0`

**Source location:** L329–L382（添付版）。

### `backup`

```python
def backup(self, log_dir: Optional[str]=None) -> bool
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `self._vasp_log.backup_result`

**Return expressions (static extraction):** `True`

**Principal conditions (static extraction):** `log_dir is None`

**Source location:** L384–L393（添付版）。

### `run`

```python
def run(self, mode: Optional[str]=None, job_cmd: Optional[str]=None, blocking: bool=True) -> bool
```

**Original docstring (source language)**

```text
VASP を実行する

local 実行
FI_PROVIDER="TCP"
I_MPI_FABRICS="shm:tcp"
I_MPI_DEBUG="5"

Args:
    mode (str): "local" dft_bin
                "mpi" mpi_cmd + mpi_flag + num_procs + dft_bin
                "job" job_cmd + dft_bin
    job_cmd (str): ジョブコマンド(mode=job時に使う)
                　　優先順番
                   instance(job_cmd=xxx)< set_job_cmd(xxx) < run(job_cmd=xxx)
    blocking (bool):  subprocessをブロッキングで起動(default: True)

Returns:
    bool: 正しく終わったデー
```

**Calls (static AST extraction):** `cmd.append`, `cmd_args.append`, `os.access`, `os.environ.copy`, `os.environ.get`, `os.environ.get('PATH', '').split`, `os.path.isfile`, `os.path.join`, `self._logger.error`, `self._logger.info`, `str`, `subprocess.run`, `sys.exit`

**Return expressions (static extraction):** `True`; `False`

**Principal conditions (static extraction):** `self._config.dft_omp_num_threads is not None`; `mode is None`; `mode == 'local'`; `mode != 'job'`; `self.dft_bin is None`; `mode == 'mpi'`; `not dft_bin_found`; `cmd_item is None`; `self.mpi_flag is not None`; `self.num_procs is not None`

**Source location:** L399–L537（添付版）。

### `set_mpi`

```python
def set_mpi(self, mpi_cmd: Optional[str]=None, mpi_flag: Optional[str]=None, num_procs: Optional[int]=None)
```

**Original docstring (source language)**

```text
MPI設定書き換え
```

**Instance attributes assigned directly:** `self._config.mpi_cmd`, `self._config.mpi_flag`, `self._config.num_procs`, `self.mpi_cmd`, `self.mpi_flag`, `self.num_procs`

**Principal conditions (static extraction):** `mpi_cmd is not None`; `num_procs is not None`; `mpi_flag is not None`

**Source location:** L543–L558（添付版）。

### `set_job_cmd`

```python
def set_job_cmd(self, job_cmd: Optional[str]=None)
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Instance attributes assigned directly:** `self._config.job_cmd`, `self.job_cmd`

**Principal conditions (static extraction):** `job_cmd is not None`

**Source location:** L560–L566（添付版）。

### `ensure_vasp5_format`

```python
def ensure_vasp5_format(self, poscar_name: str, element_info: Optional[Union[str, Sequence[str]]]=None, logger: Optional[XLogger]=XLogger()) -> bool
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `XLogger`, `ensure_vasp5_format`

**Return expressions (static extraction):** `ensure_vasp5_format(poscar_name, element_info, logger=logger)`

**Principal conditions (static extraction):** `element_info is None`

**Source location:** L572–L584（添付版）。

### `make_potential`

```python
@staticmethod
```

**Original docstring (source language)**

```text
VaspPotcarBuilder クラスを使って POTCAR を生成

Args:
    elements (list):  Li Mn O など
    output (str): ディクトリ付きならば bb/POTCAR などと書けばいい

Returns:
```

**Calls (static AST extraction):** `VaspPotcarBuilder`, `builder.build`

**Return expressions (static extraction):** `True`

**Source location:** L587–L608（添付版）。

### `convert_to_cfg`

```python
@staticmethod
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `convert_to_cfg`

**Return expressions (static extraction):** `True`

**Source location:** L611–L615（添付版）。

### `contcar2cfg`

```python
def contcar2cfg(self, cfg_name: Optional[str]=None) -> bool
```

**Original docstring (source language)**

```text
convert CONTCAR to CFG

Args:
    cfg_name (str):

Returns:
    bool:
```

**Calls (static AST extraction):** `contcar2cfg`, `self._logger.info`, `str`

**Return expressions (static extraction):** `True`

**Principal conditions (static extraction):** `cfg_name is None`

**Source location:** L621–L640（添付版）。

### `poscar2cfg`

```python
def poscar2cfg(self, cfg_name: str='aaa') -> bool
```

**Original docstring (source language)**

```text
Convert VASP POSCAR を RMC CFG 形式に変換する
POSCAR の名前は固定、aaa.cfg ファイル名に変換

Args:
    cfg_name: str = "aaa": Name of the output file without extension.

Returns:
    bool: 正しく終わったデー
```

**Calls (static AST extraction):** `poscar2cfg`, `self._logger.info`

**Return expressions (static extraction):** `poscar2cfg(cfg_name)`

**Source location:** L642–L658（添付版）。

### `xdatcar2poscar`

```python
def xdatcar2poscar(self, vasp_name: Optional[str]=None) -> bool
```

**Original docstring (source language)**

```text
Copy XDATCAR to a new file with the specified name (... .vasp).
最終結果だけならば CONTCAR で十分

Args:
    vasp_name (str): {vasp_name}.vasp
Returns:
    bool: 正しく終わったデー
```

**Calls (static AST extraction):** `self._logger.info`, `str`, `xdatcar2poscar`

**Return expressions (static extraction):** `xdatcar2poscar(str(vasp_name))`

**Principal conditions (static extraction):** `vasp_name is None`

**Source location:** L660–L677（添付版）。

### `pdb2poscar`

```python
@staticmethod
```

**Existing docstring:** なし（以下はコード構造からの機械的抽出であり、仕様を保証しません）。

**Calls (static AST extraction):** `read`, `write`

**Source location:** L680–L684（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp
:members:
:undoc-members:
:show-inheritance:
```
