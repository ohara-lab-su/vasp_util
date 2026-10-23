# vasp_log — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `vasp_log`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `vasp_log(3).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspLog`

VASP の出力ファイルを計算後に整理・解析するクラス

### `__init__`

```python
def __init__(self, logger: Optional[XLogger]=None) -> None
```

**Original docstring (source language)**

```text
Args:
    logger (XLogger): 全てのインスタンスが同じ XLogger()
```

**Calls (static AST extraction):** `XLogger`

**Instance attributes assigned directly:** `self._logger`

**Source location:** L24–L32（添付版）。

### `_exists_either`

```python
@staticmethod
```

**Original docstring (source language)**

```text
通常 or .gz のどちらかが存在するか
```

**Calls (static AST extraction):** `path.exists`, `path.with_suffix`, `path.with_suffix(path.suffix + '.gz').exists`

**Return expressions (static extraction):** `path.exists() or path.with_suffix(path.suffix + '.gz').exists()`

**Source location:** L39–L43（添付版）。

### `_copy_either`

```python
def _copy_either(self, src: Path, dst: Path) -> None
```

**Original docstring (source language)**

```text
通常 or .gz を copy。必要に応じて .gz 拡張子を付与
```

**Calls (static AST extraction):** `Path`, `gzsrc.exists`, `self._logger.info`, `shutil.copyfile`, `src.exists`, `src.with_suffix`, `str`

**Principal conditions (static extraction):** `src.exists()`; `gzsrc.exists()`

**Source location:** L45–L59（添付版）。

### `_move_either`

```python
def _move_either(self, src: Path, dst: Path) -> None
```

**Original docstring (source language)**

```text
通常 or .gz を move。必要に応じて .gz 拡張子を付与
```

**Calls (static AST extraction):** `Path`, `gzsrc.exists`, `self._logger.info`, `shutil.move`, `src.exists`, `src.with_suffix`, `str`

**Principal conditions (static extraction):** `src.exists()`; `gzsrc.exists()`

**Source location:** L61–L75（添付版）。

### `vcopy`

```python
def vcopy(self, suffix: str) -> None
```

**Original docstring (source language)**

```text
Vcopy と同等の整理処理を実行（Vcopy2 は未実装）。

Args:
    suffix (str): 付与する接尾辞（例: "A1" など）
```

**Calls (static AST extraction):** `FileNotFoundError`, `Path`, `Path('OUTCAR').exists`, `Path('OUTCAR.gz').exists`, `contcar.exists`, `contcar.with_suffix`, `contcar_gz.exists`, `gzip.open`, `name.lower`, `open`, `os.chmod`, `os.getpid`, `poscar_backup.exists`, `self._copy_either`, `self._exists_either`, `self._logger.info`, `self._move_either`, `shutil.copyfile`, `shutil.copyfileobj`

**Explicitly raised exceptions:** `FileNotFoundError('STOP: OUTCAR and OUTCAR.gz file not found.')`

**Principal conditions (static extraction):** `not (Path('OUTCAR').exists() or Path('OUTCAR.gz').exists())`; `self._exists_either(dst)`; `contcar.exists() or contcar_gz.exists()`; `src_path.suffix == '.gz'`; `poscar_backup.exists()`

**Source location:** L77–L157（添付版）。

### `get_E0`

```python
@staticmethod
```

**Original docstring (source language)**

```text
OSZICAR から E0 を取り出して、ファイル保存する
(廃止予定)

Args:
    input_filename:
    output_filename:
    key:

Returns:
```

**Calls (static AST extraction):** `f.readlines`, `open`, `outfile.writelines`, `print`

**Principal conditions (static extraction):** `key in line`

**Source location:** L161–L187（添付版）。

### `collect_result`

```python
def collect_result(self)
```

**Original docstring (source language)**

```text
VASPのログからひつようなじょうほうをとりだして、保存する
This function is used to grep energy from OUTCAR file.
```

**Calls (static AST extraction):** `self._logger.info`, `self.get_E0`

**Source location:** L189–L195（添付版）。

### `backup_result`

```python
def backup_result(self, log_dir: str='log') -> bool
```

**Original docstring (source language)**

```text
Copy VASP log files to the specified directory.

Args:
    log_dir (str): Directory to copy the log files to.
```

**Calls (static AST extraction):** `os.makedirs`, `os.path.exists`, `self._logger.info`, `shutil.copy`

**Return expressions (static extraction):** `True`

**Principal conditions (static extraction):** `not os.path.exists(log_dir)`; `os.path.exists(file_name)`

**Source location:** L197–L233（添付版）。

### `remove_file`

```python
def remove_file(self, filename: str) -> None
```

**Original docstring (source language)**

```text
存在するファイルを削除
```

**Calls (static AST extraction):** `os.path.exists`, `os.remove`, `self._logger.info`

**Principal conditions (static extraction):** `os.path.exists(filename)`

**Source location:** L235–L239（添付版）。

### `remove_pattern`

```python
def remove_pattern(self, pattern: str) -> None
```

**Original docstring (source language)**

```text
ワイルドカードパターンで一致するファイルを削除
```

**Calls (static AST extraction):** `glob.glob`, `os.remove`, `self._logger.info`

**Source location:** L241–L248（添付版）。

### `clean`

```python
def clean(self, suffixes: List[str]=None) -> None
```

**Original docstring (source language)**

```text
Args:
    suffixes (str):

Returns:
```

**Calls (static AST extraction):** `f.lower`, `f.upper`, `self.remove_file`, `self.remove_pattern`

**Principal conditions (static extraction):** `not suffixes`

**Source location:** L250–L330（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_log
:members:
:undoc-members:
:show-inheritance:
```
