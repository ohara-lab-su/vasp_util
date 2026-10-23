# vasp_log — 実装に基づく API Reference

対象ソース: `vasp_log(3).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## class `VaspLog`

VASP の出力ファイルを計算後に整理・解析するクラス

### `__init__`

```python
def __init__(self, logger: Optional[XLogger]=None) -> None
```

**既存 docstring（原文）**

```text
Args:
    logger (XLogger): 全てのインスタンスが同じ XLogger()
```

**呼び出す関数・メソッド（静的抽出）:** `XLogger`

**更新するインスタンス属性（直接代入）:** `self._logger`

**ソース位置:** L24–L32（添付版）。

### `_exists_either`

```python
@staticmethod
```

**既存 docstring（原文）**

```text
通常 or .gz のどちらかが存在するか
```

**呼び出す関数・メソッド（静的抽出）:** `path.exists`, `path.with_suffix`, `path.with_suffix(path.suffix + '.gz').exists`

**return 式（静的抽出）:** `path.exists() or path.with_suffix(path.suffix + '.gz').exists()`

**ソース位置:** L39–L43（添付版）。

### `_copy_either`

```python
def _copy_either(self, src: Path, dst: Path) -> None
```

**既存 docstring（原文）**

```text
通常 or .gz を copy。必要に応じて .gz 拡張子を付与
```

**呼び出す関数・メソッド（静的抽出）:** `Path`, `gzsrc.exists`, `self._logger.info`, `shutil.copyfile`, `src.exists`, `src.with_suffix`, `str`

**主な条件分岐（静的抽出）:** `src.exists()`; `gzsrc.exists()`

**ソース位置:** L45–L59（添付版）。

### `_move_either`

```python
def _move_either(self, src: Path, dst: Path) -> None
```

**既存 docstring（原文）**

```text
通常 or .gz を move。必要に応じて .gz 拡張子を付与
```

**呼び出す関数・メソッド（静的抽出）:** `Path`, `gzsrc.exists`, `self._logger.info`, `shutil.move`, `src.exists`, `src.with_suffix`, `str`

**主な条件分岐（静的抽出）:** `src.exists()`; `gzsrc.exists()`

**ソース位置:** L61–L75（添付版）。

### `vcopy`

```python
def vcopy(self, suffix: str) -> None
```

**既存 docstring（原文）**

```text
Vcopy と同等の整理処理を実行（Vcopy2 は未実装）。

Args:
    suffix (str): 付与する接尾辞（例: "A1" など）
```

**呼び出す関数・メソッド（静的抽出）:** `FileNotFoundError`, `Path`, `Path('OUTCAR').exists`, `Path('OUTCAR.gz').exists`, `contcar.exists`, `contcar.with_suffix`, `contcar_gz.exists`, `gzip.open`, `name.lower`, `open`, `os.chmod`, `os.getpid`, `poscar_backup.exists`, `self._copy_either`, `self._exists_either`, `self._logger.info`, `self._move_either`, `shutil.copyfile`, `shutil.copyfileobj`

**明示的に送出する例外:** `FileNotFoundError('STOP: OUTCAR and OUTCAR.gz file not found.')`

**主な条件分岐（静的抽出）:** `not (Path('OUTCAR').exists() or Path('OUTCAR.gz').exists())`; `self._exists_either(dst)`; `contcar.exists() or contcar_gz.exists()`; `src_path.suffix == '.gz'`; `poscar_backup.exists()`

**ソース位置:** L77–L157（添付版）。

### `get_E0`

```python
@staticmethod
```

**既存 docstring（原文）**

```text
OSZICAR から E0 を取り出して、ファイル保存する
(廃止予定)

Args:
    input_filename:
    output_filename:
    key:

Returns:
```

**呼び出す関数・メソッド（静的抽出）:** `f.readlines`, `open`, `outfile.writelines`, `print`

**主な条件分岐（静的抽出）:** `key in line`

**ソース位置:** L161–L187（添付版）。

### `collect_result`

```python
def collect_result(self)
```

**既存 docstring（原文）**

```text
VASPのログからひつようなじょうほうをとりだして、保存する
This function is used to grep energy from OUTCAR file.
```

**呼び出す関数・メソッド（静的抽出）:** `self._logger.info`, `self.get_E0`

**ソース位置:** L189–L195（添付版）。

### `backup_result`

```python
def backup_result(self, log_dir: str='log') -> bool
```

**既存 docstring（原文）**

```text
Copy VASP log files to the specified directory.

Args:
    log_dir (str): Directory to copy the log files to.
```

**呼び出す関数・メソッド（静的抽出）:** `os.makedirs`, `os.path.exists`, `self._logger.info`, `shutil.copy`

**return 式（静的抽出）:** `True`

**主な条件分岐（静的抽出）:** `not os.path.exists(log_dir)`; `os.path.exists(file_name)`

**ソース位置:** L197–L233（添付版）。

### `remove_file`

```python
def remove_file(self, filename: str) -> None
```

**既存 docstring（原文）**

```text
存在するファイルを削除
```

**呼び出す関数・メソッド（静的抽出）:** `os.path.exists`, `os.remove`, `self._logger.info`

**主な条件分岐（静的抽出）:** `os.path.exists(filename)`

**ソース位置:** L235–L239（添付版）。

### `remove_pattern`

```python
def remove_pattern(self, pattern: str) -> None
```

**既存 docstring（原文）**

```text
ワイルドカードパターンで一致するファイルを削除
```

**呼び出す関数・メソッド（静的抽出）:** `glob.glob`, `os.remove`, `self._logger.info`

**ソース位置:** L241–L248（添付版）。

### `clean`

```python
def clean(self, suffixes: List[str]=None) -> None
```

**既存 docstring（原文）**

```text
Args:
    suffixes (str):

Returns:
```

**呼び出す関数・メソッド（静的抽出）:** `f.lower`, `f.upper`, `self.remove_file`, `self.remove_pattern`

**主な条件分岐（静的抽出）:** `not suffixes`

**ソース位置:** L250–L330（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.vasp_log
:members:
:undoc-members:
:show-inheritance:
```
