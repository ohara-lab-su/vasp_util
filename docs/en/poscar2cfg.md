# poscar2cfg — Source-based detailed API notes

This page preserves the full implementation analysis supplied in the Japanese manual for `poscar2cfg`. Function signatures, source locations, call graphs, explicit exceptions, return expressions, and branch conditions are retained. Japanese source docstrings and comments are quoted verbatim rather than represented as English translations. These observations are static and are not runtime guarantees.


Source file: `poscar2cfg(3).py`。公開・非公開の定義を含みます。以下の条件分岐、戻り値式、例外は AST から機械的に抽出したもので、実行時の挙動を検証したものではありません。

## function `contcar2cfg`

```python
def contcar2cfg(cfg_name: str, logger: Optional[Any]=None)
```

**Original docstring (source language)**

```text
2025.10.29 update CONTCAR タイプ対応
コア部分を分離

Args:
    cfg_name (str):  CFG 保存用の名前
    logger (str):

Returns:
```

**Calls (static AST extraction):** `convert_to_cfg`, `logger.info`, `logging.getLogger`

**Return expressions (static extraction):** `convert_to_cfg('CONTCAR', cfg_name)`

**Principal conditions (static extraction):** `logger is None`

**Source location:** L42–L64（添付版）。

## function `poscar2cfg`

```python
def poscar2cfg(cfg_name: str, poscar_name: Optional[str]=None, logger: Optional[Any]=None) -> bool
```

**Original docstring (source language)**

```text
2025.10.29 update CONTCAR タイプ対応
コア部分を分離

Args:
    cfg_name (str): CFG 保存用の名前
    poscar_name (str):
    logger (Any):

Returns:
```

**Calls (static AST extraction):** `convert_to_cfg`, `logger.info`, `logging.getLogger`

**Return expressions (static extraction):** `convert_to_cfg(f'{poscar_name}', cfg_name)`

**Principal conditions (static extraction):** `logger is None`; `poscar_name is None`

**Source location:** L67–L95（添付版）。

## function `vasp2cfg`

```python
def vasp2cfg(vasp_name: str, cfg_name: str=None, logger: Optional[Any]=None)
```

**Original docstring (source language)**

```text
2025.10.29 update CONTCAR タイプ対応

*) poscar2cfg ではなく vasp2cfg にしているのは
   poscar --> xxx.cfg ではなく
   xxx.vasp --> xxx.cfg を意図しているから

Args:
    cfg_name (str): cfg_name.vasp ファイルを読み込む(POSCAR相当)
                    もし、cfg_name.vasp ファイルが存在しなければ
                    CONTCAR を読み込む
    vasp_name (str):
    logger:

Returns:
```

**Calls (static AST extraction):** `convert_to_cfg`, `logger.info`, `logging.getLogger`

**Return expressions (static extraction):** `convert_to_cfg(poscar_name=poscar_name, cfg_name=cfg_name)`

**Principal conditions (static extraction):** `logger is None`; `cfg_name is None`

**Source location:** L98–L134（添付版）。

## function `convert_to_cfg`

```python
def convert_to_cfg(poscar_name: str='POSCAR', cfg_name: str='aaa', logger: Optional[Any]=None) -> bool
```

**Original docstring (source language)**

```text
name ファイルを中身 POSCAR/CONTCAR とみなして、そのファイルを cfg 形式にする

Args:
    poscar_name (str): この名前のファイルをそのまま読み込む
    cfg_name (str): cfg_name.cfg として書き出す
    logger (XLogger):

Returns:
```

**Calls (static AST extraction):** `cfg.close`, `datfile.split`, `datlines[2].split`, `datlines[3].split`, `datlines[4].split`, `datlines[6].split`, `datlines[lines].split`, `float`, `int`, `len`, `list`, `logger.error`, `logging.getLogger`, `map`, `np.zeros`, `open`, `os.path.exists`, `print`, `range`, `sum`, `tmp.read`

**Return expressions (static extraction):** `True`; `False`

**Principal conditions (static extraction):** `logger is None`; `not os.path.exists(poscar_name)`

**Source location:** L137–L312（添付版）。


## Sphinx autodoc（ビルド時に最新ソースから生成）

```{automodule} vasp_util.util.poscar2cfg
:members:
:undoc-members:
:show-inheritance:
```
