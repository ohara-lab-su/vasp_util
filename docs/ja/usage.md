# 使用マニュアル：実装に基づく Python API 利用例

本書は `vasp_util` の主要クラスを、単なるメソッド一覧ではなく、入力作成→計算→構造・電子状態解析→RMC 連携の流れで使用するための実例集です。コード例は提示された Python 実装の公開シグネチャに合わせています。VASP 本体、擬ポテンシャル、実データを使った実行試験は行っていません。

**実行上の前提**：各例は原則として VASP 入出力ファイルの存在する作業ディレクトリで実行します。`POSCAR`・`INCAR`・`KPOINTS`・`OUTCAR` 等は実際のファイル名です。例示する元素、原子番号、カットオフは対象系に合わせて変更してください。以下の Python スクリプト例は CLI 引数を必要としません。

## 1. POSCAR の構造を読む

```python
from vasp_util.vasp_poscar import VaspPoscar

POSCAR_FILE: str = "POSCAR"


def main() -> None:
    poscar = VaspPoscar(POSCAR_FILE)
    print("atoms:", poscar.get_num_atoms())
    print("elements:", poscar.get_elements())
    print("atom species:", poscar.get_atom_indices())
    print("lattice (Å):\n", poscar.get_lattice_vectors())
    print("scale specification:", poscar.get_scale())
    print("fractional coordinates:\n", poscar.get_coords_direct())
    print("first atom (Å):", poscar.get_cartesian_position(1))


if __name__ == "__main__":
    main()
```

`get_coords_direct()` は全原子の分率座標配列を返し、`get_coords_direct(1)` は第1原子の分率座標を返します。**原子番号を受け取る個別取得 API は原則 1 始まり**です。一方、返された NumPy 配列を Python で添字アクセスするときは 0 始まりです。POSCAR が Cartesian 表記でも内部座標は Direct に変換されます。`get_lattice_vectors()` はスケール適用済みの格子を返します。POSCAR 第2行の正の単一倍率、負の体積指定、3成分倍率に対応する実装です。

### 元素別サイト番号と全体番号の変換

```python
from vasp_util.vasp_poscar import VaspPoscar

POSCAR_FILE: str = "POSCAR"
ELEMENT: str = "Li"
LOCAL_SITE: int = 1


def main() -> None:
    poscar = VaspPoscar(POSCAR_FILE)
    global_index: int = poscar.get_global_index(ELEMENT, LOCAL_SITE)
    print("global index:", global_index)
    print("element:", poscar.get_element_by_global_index(global_index))
    print("local index:", poscar.get_local_index_by_global_index(global_index))
    print("all global indices:", poscar.get_element_site_indices(ELEMENT))


if __name__ == "__main__":
    main()
```

`get_global_index("Li", 1)` は Li の第1サイトに対応する**全原子通し番号**を返します。Li が存在しない構造ではこの例は使用できません。`get_element_site_indices("Li")` が返す番号も全原子通し番号です。

### 座標変換と周期境界条件（PBC）

```python
import numpy as np
from vasp_util.vasp_poscar import VaspPoscar

POSCAR_FILE: str = "POSCAR"
INDEX_A: int = 1
INDEX_B: int = 2


def main() -> None:
    poscar = VaspPoscar(POSCAR_FILE)
    a = poscar.get_direct_position(INDEX_A)
    b = poscar.get_direct_position(INDEX_B)
    displacement_direct = poscar.get_shortest_pbc_direct_vector(a, b)
    displacement_cartesian = poscar.conv_direct_to_cartesian(displacement_direct)
    print("minimum-image displacement (Å):", displacement_cartesian)
    print("distance (Å):", float(np.linalg.norm(displacement_cartesian)))
    print("back to Direct:", poscar.conv_cartesian_to_direct(displacement_cartesian))


if __name__ == "__main__":
    main()
```

`get_shortest_pbc_direct_vector()` は Direct 座標で最短像変位を求めます。距離を Å で得るには、格子行列を使って Cartesian に変換した後にノルムを計算します。単純な Direct 座標差のノルムは一般には Å 単位の距離ではありません。

## 2. 近接原子・配位環境を調べる

```python
from vasp_util.vasp_poscar import VaspPoscar
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

POSCAR_FILE: str = "POSCAR"
CENTER: int = 1
NEIGHBOR_COUNT: int = 4


def main() -> None:
    analyzer = VaspPoscarAnalyzer(VaspPoscar(POSCAR_FILE))
    distance = analyzer.get_interatomic_distance(1, 2, pbc=True)
    vector, vector_length = analyzer.get_distance_vector(1, 2, pbc=True)
    print("interatomic distance (Å):", float(distance))
    print("vector (Å):", vector, "norm (Å):", vector_length)
    neighbors = analyzer.get_neighbors(CENTER, NEIGHBOR_COUNT, target_elements=["O", "S"])
    for neighbor in neighbors:
        print(neighbor)


if __name__ == "__main__":
    main()
```

`get_neighbors(center_global_idx, nn, target_elements)` の返り値は `(距離, 元素, 元素内サイト番号, 全体番号, Cartesian座標)` のタプルのリストです。対象元素は実際の POSCAR に合わせてください。

**実装上の注意**：提示された `get_neighbors()` の距離計算は `get_shortest_pbc_direct_vector()` の返り値に直接 `np.linalg.norm()` を適用しています。従って、**このメソッドの第1要素を Å 単位の距離とみなすのは危険**です。Å 単位の配位距離が必要なら `get_interatomic_distance()` で再評価してください。`get_nearest_neighbors()` では Direct 変位を Cartesian に変換してから距離を求める別実装になっています。

### 元素を指定して最近接原子を調べる

```python
from vasp_util.vasp_poscar import VaspPoscar
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

POSCAR_FILE: str = "POSCAR"
CENTER_ELEMENT: str = "P"
CENTER_LOCAL_SITE: int = 1
NEIGHBOR_ELEMENT: str = "O"
MAX_NEIGHBORS: int = 4


def main() -> None:
    analyzer = VaspPoscarAnalyzer(VaspPoscar(POSCAR_FILE))
    neighbors = analyzer.get_nearest_neighbors(
        center_element=CENTER_ELEMENT,
        center_local_site_index=CENTER_LOCAL_SITE,
        max_neighbors=MAX_NEIGHBORS,
        neighbor_element=NEIGHBOR_ELEMENT,
        pbc=True,
    )
    for element, site, global_index, distance, displacement in neighbors:
        print(element, site, global_index, distance, displacement)


if __name__ == "__main__":
    main()
```

返り値は `(元素, 元素内サイト番号, 全体番号, 距離, Cartesian変位)` です。`cutoff_distance` を指定すると、`max_neighbors` での個数制限よりも距離による抽出が優先されます。**注意**：提示された実装では `get_nearest_neighbors(..., pbc=False)` を指定しても内部で最短像変位を計算しており、`pbc` 引数は距離計算の切替に使われていません。

## 3. 2つの構造間の原子移動を解析する

RMC と DFT 緩和前後の構造比較や、MD の隣接ステップ間の移動量解析に利用できます。**両構造で原子の並びが同一であることが必要**です。

```python
from vasp_util.vasp_poscar import VaspPoscar
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

BEFORE_FILE: str = "POSCAR_before"
AFTER_FILE: str = "POSCAR_after"
ELEMENT: str = "Li"
THRESHOLD_ANGSTROM: float = 2.0


def main() -> None:
    before = VaspPoscarAnalyzer(VaspPoscar(BEFORE_FILE))
    after = VaspPoscarAnalyzer(VaspPoscar(AFTER_FILE))
    indices = before.poscar.get_element_site_indices(ELEMENT)
    for global_index in indices:
        distance = before.get_jump_distance(after, global_index, pbc=True)
        jumped = before.is_jump(after, global_index, THRESHOLD_ANGSTROM, pbc=True)
        print(global_index, distance, jumped)


if __name__ == "__main__":
    main()
```

`get_jump_distance()` は**全体原子番号**を受け取り、PBC 補正後の移動距離を Å で返します。`is_jump()` はその距離としきい値を比較します。格子が大きく変形する場合は、両構造の座標と基準格子の扱いを別途検討してください。

### MD ファイル群を走査する

```python
from vasp_util.vasp_poscar_analyzer import VaspPoscarAnalyzer

MD_DIRECTORY: str = "md_poscars"
FILE_TEMPLATE: str = "POSCAR_{}"
START_STEP: int = 0
END_STEP: int = 100
ELEMENT: str = "Li"
START_SITE: int = 1
END_SITE: int = 10
JUMP_THRESHOLD: float = 2.0


def main() -> None:
    VaspPoscarAnalyzer.scan_md_series_for_jumps(
        folder_path=MD_DIRECTORY,
        file_template=FILE_TEMPLATE,
        step_min=START_STEP,
        step_max=END_STEP,
        element=ELEMENT,
        start_site=START_SITE,
        end_site=END_SITE,
        threshold=JUMP_THRESHOLD,
        show_non_jumps=False,
    )


if __name__ == "__main__":
    main()
```

同クラスには `check_jump_between_two_steps()` と `trace_site_motion_over_md_steps()` もあります。いずれも表示を伴うユーティリティであり、数値配列を必要とする解析には `get_jump_distance()` を直接使う方が明確です。

## 4. INCAR を編集する

`VaspIncar` はコメントや空行を維持しつつタグを編集する設計です。**コンストラクタだけではファイルを初期化しません**。`init()` または最初のタグ操作によって初期化されます。

```python
from vasp_util.vasp_incar import VaspIncar

INCAR_FILE: str = "INCAR"


def main() -> None:
    incar = VaspIncar(incar_name=INCAR_FILE, auto_write=False)
    incar.init()
    print("old ENCUT:", incar.get("ENCUT", default=None))
    incar.set("ENCUT", 520, auto_write=False)
    incar.set("EDIFF", 1e-6, auto_write=False)
    incar.set_tag("ISMEAR", 0, auto_write=False)
    incar.set_tag("SIGMA", 0.05, auto_write=False)
    incar.write()
    print("updated INCAR:", incar.export_dict())


if __name__ == "__main__":
    main()
```

`auto_write=False` をコンストラクタと各 `set()` に指定し、最後に `write()` する例です。`set()` / `set_tag()` はそれぞれ `auto_write` の引数既定値が `True` なので、**コンストラクタの設定だけを見て一括書込みになると決めつけない**でください。削除は `remove("TAG", auto_write=False)`、外部変更の再読み込みは `reload()` です。

### 2つの INCAR を比較する

```python
from vasp_util.vasp_incar import VaspIncar

FIRST_INCAR: str = "INCAR.initial"
SECOND_INCAR: str = "INCAR.relaxed"


def main() -> None:
    first = VaspIncar(incar_name=FIRST_INCAR, auto_write=False)
    second = VaspIncar(incar_name=SECOND_INCAR, auto_write=False)
    first.init()
    second.init()
    differences = first.diff_with(second)
    for tag, values in differences.items():
        print(tag, values)


if __name__ == "__main__":
    main()
```

`diff_with()` は異なるタグだけを辞書で返します。指定したファイルが存在しない場合、`init()` は空ファイルを生成するため、比較対象ファイルの存在を事前に確認してください。

## 5. KPOINTS を作成・更新する

```python
from vasp_util.vasp_kpoints import VaspKpoints

KPOINTS_FILE: str = "KPOINTS"


def main() -> None:
    kpoints = VaspKpoints(kpoints_name=KPOINTS_FILE, auto_write=False)
    kpoints.set_mode("Gamma", auto_write=False)
    kpoints.set_grid(2, 2, 2, auto_write=False)
    kpoints.set_shift(0, 0, 0, auto_write=False)
    kpoints.set_comment("Gamma-centered mesh", auto_write=False)
    kpoints.write()
    print(kpoints.export_dict())


if __name__ == "__main__":
    main()
```

既存の KPOINTS があればコンストラクタが読み込みます。**存在しなければ** `Monkhorst-Pack`, `(1,1,1)`, `(0,0,0)` で初期化し、コンストラクタ内でファイルを書き出します。`auto_write=False` でも新規ファイルの作成は抑止されません。`update(mode=..., grid=..., shift=..., comment=...)` によるまとめての設定にも対応しています。

## 6. POTCAR を生成する

```python
from vasp_util.vasp_potcar import VaspPotcarBuilder

POTENTIAL_DIRECTORY: str = "~/potpaw_PBE.64"
ELEMENTS: list[str] = ["Li", "P", "S"]
OUTPUT_FILE: str = "POTCAR"


def main() -> None:
    builder = VaspPotcarBuilder(base_dir=POTENTIAL_DIRECTORY)
    for element in ELEMENTS:
        print(element, builder.choose_potential(element))
    success = builder.build(elements=ELEMENTS, poscar_name=OUTPUT_FILE)
    print("POTCAR written:", success)


if __name__ == "__main__":
    main()
```

`choose_potential()` は元素別優先候補を検索します。一方、**提示された `build()` の実装は `base_dir/<元素名>/POTCAR` を直接参照し、`choose_potential()` の優先候補を使っていません**。例えば `Li_sv` のみ存在する環境では `choose_potential("Li")` が見つけても `build(["Li"])` が同じファイルを使うとは限りません。利用前に擬ポテンシャル配置と元素順序を確認してください。PAW データセット自体は本パッケージに含まれません。

## 7. OUTCAR の SCF・イオン緩和履歴を解析する

`VaspOutcar` は**終了判定に失敗した OUTCAR をコンストラクタで拒否**します。計算途中のログを逐次読む用途ではありません。

```python
import numpy as np
from vasp_util.vasp_outcar import VaspOutcar

OUTCAR_FILE: str = "OUTCAR"


def main() -> None:
    outcar = VaspOutcar(OUTCAR_FILE)
    print("finalized:", outcar.is_finalized())
    print("ionic steps:", outcar.get_ionstep_count())
    for mode in ("toten", "e0", "sigma0"):
        energies = outcar.get_energy_ionstep(mode=mode)
        print(mode, energies)
    matrix = outcar.get_energy_matrix(mode="e0")
    flat = outcar.get_energy_flat(mode="e0")
    print("SCF matrix shape:", matrix.shape)
    print("valid SCF energies:", flat.size)
    print("finite energy values:", int(np.isfinite(matrix).sum()))


if __name__ == "__main__":
    main()
```

エネルギーの `mode` は `toten`（free energy TOTEN）、`e0`（energy without entropy）、`sigma0`（energy(sigma→0)）です。`get_energy_matrix()` の行がイオンステップ、列が電子反復で、未使用セルには `NaN` が入ります。`get_energy_flat()` は `NaN` を除いた一次元配列です。`get_energy(ionstep, iterstep, mode=...)` の添字は **0 始まり**で、範囲外や値がない場合は `None` です。

### 原子位置・力・磁気モーメント

```python
import numpy as np
from vasp_util.vasp_outcar import VaspOutcar

OUTCAR_FILE: str = "OUTCAR"


def main() -> None:
    outcar = VaspOutcar(OUTCAR_FILE)
    last_step: int = outcar.get_ionstep_count() - 1
    positions = outcar.get_positions(last_step)
    forces = outcar.get_forces(last_step)
    magnetic_moments = outcar.get_magmom_atom(last_step)
    print("positions shape:", positions.shape)
    print("forces shape:", forces.shape)
    print("max force (eV/Å):", float(np.nanmax(np.linalg.norm(forces, axis=1))))
    print("magmom (s,p,d,total) shape:", magnetic_moments.shape)
    print("total magnetization:", outcar.get_magmom_total(last_step))


if __name__ == "__main__":
    main()
```

`get_positions()` / `get_forces()` は `(nions, 3)`、`get_magmom_atom()` は `(nions, 4)` を返します。磁気モーメントが出力されていない計算では `NaN` を含む場合があります。力の評価では、実データに有効な値が存在することを確認してください。

## 8. Vasp クラスで入力設定と実行をまとめる

`Vasp` は `Config`、`VaspIncar`、`VaspKpoints`、`VaspLog` を統合します。既存入力ファイルの扱いを明示するため、まず `make_default_input=False` で構築します。

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

VASP_BINARY: str = "vasp_gam"


def main() -> None:
    config = Config()
    config.dft_bin = VASP_BINARY
    config.run_mode = "local"
    vasp = Vasp(config=config, make_default_input=False)
    vasp.set_tag("EDIFF", 1e-6)
    vasp.set_tag("NELM", 100)
    print(vasp.get_tag("EDIFF"))
    print(vasp.export_incar_dict())
    print(vasp.export_kpoints_dict())
    vasp.preprocess()
    succeeded = vasp.run(mode="local")
    print("VASP succeeded:", succeeded)


if __name__ == "__main__":
    main()
```

`preprocess()` は `INCAR`、`KPOINTS`、`POTCAR`、`POSCAR` の存在を確認し、**構造変換は自動では行いません**。不足時には `sys.exit(-1)` が実行されます。`run(mode="local")` も単にバイナリを直接実行するのではなく、**`mpirun -np 1 <dft_bin>`** を構成します。`mpirun` と VASP 実行ファイルが利用可能である必要があります。

### MPI 実行

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

VASP_BINARY: str = "vasp_std"
PROCESS_COUNT: int = 8


def main() -> None:
    config = Config()
    vasp = Vasp(config=config, dft_bin=VASP_BINARY, make_default_input=False)
    vasp.set_mpi(mpi_cmd="mpirun", mpi_flag="-np", num_procs=PROCESS_COUNT)
    vasp.preprocess()
    result = vasp.run(mode="mpi")
    print(result)


if __name__ == "__main__":
    main()
```

`run(mode="mpi")` は `mpi_cmd`、`mpi_flag`、`num_procs`、`dft_bin` を組み立てます。`mode="job"` は `job_cmd` のみをコマンドとして実行する実装です。`job_cmd` にシェル文字列全体を渡す設計には注意が必要で、提示されたコードは `subprocess.run([...], shell=False)` で実行します。空白を含む `"qsub script.sh"` がシェル同様に分解されるとは限りません。`blocking` 引数はありますが、提示された `run()` 本体では実行制御に使用されず `subprocess.run()` は同期実行です。

## 9. RMC との構造受け渡し

`Vasp` には `contcar2cfg()`、`poscar2cfg()`、`convert_to_cfg()`、`xdatcar2poscar()`、`ensure_vasp5_format()` などの変換インターフェースがあります。これらは `vasp_util.util` 以下の実装を呼び出します。**今回提示されたソースには該当ユーティリティ本体の一部が含まれていないため、変換後の詳細仕様・全引数・出力形式は未検証です**。

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

CFG_NAME: str = "relaxed"


def main() -> None:
    config = Config()
    vasp = Vasp(config=config, make_default_input=False)
    vasp.contcar2cfg(cfg_name=CFG_NAME)


if __name__ == "__main__":
    main()
```

`postprocess(log_dir=..., cfg_name=...)` はログ収集・バックアップ後に、`CONTCAR` が存在し空でない場合に `CONTCAR → POSCAR`、`POSCAR → <cfg_name>.vasp`、`CONTCAR → CFG` を実行します。**`POSCAR` を上書きするため、元の入力構造を保持したい場合は先にバックアップしてください**。また `cfg_name` 省略時は `config.cfg_name` を参照しますが、今回提示された `Config` クラスの宣言部分には `cfg_name` が見当たりません。したがって、以下のように明示するのが安全です。

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

LOG_DIRECTORY: str = "vasp_log"
CFG_NAME: str = "relaxed"


def main() -> None:
    vasp = Vasp(config=Config(), make_default_input=False)
    success = vasp.postprocess(log_dir=LOG_DIRECTORY, cfg_name=CFG_NAME)
    print("postprocess:", success)


if __name__ == "__main__":
    main()
```

## 10. 設定の扱いと副作用

`Config(yaml_path="config.yml")` は YAML 内容を**インスタンス属性**へ反映します。`Config.load_yaml("config.yml")` は**クラス属性**を変更するクラスメソッドで、作用範囲が異なります。YAML キーは `Config` が持つ属性名と一致させてください。`Vasp(config=...)` に明示設定を渡すと、`dft_bin` や MPI 関連設定などは個別引数の `None` でない値が優先されます。

```python
from vasp_util.config import Config
from vasp_util.vasp import Vasp

CONFIG_FILE: str = "config.yml"


def main() -> None:
    config = Config(yaml_path=CONFIG_FILE)
    vasp = Vasp(config=config, make_default_input=False)
    print("run mode:", config.run_mode)
    print("binary:", vasp.dft_bin)


if __name__ == "__main__":
    main()
```

**再現性のための注意**：入力ファイルを書き換える API（`set_tag`、`write`、`postprocess`、POTCAR 生成など）と読み取り専用 API（POSCAR/OUTCAR 解析）を区別してください。解析前には対象ファイルのコピーを保存することを推奨します。

## 11. API リファレンスとの対応

詳細なシグネチャと docstring は [API リファレンス](api_reference.md) に掲載します。主な実装モジュールは `vasp_util.vasp`、`vasp_util.vasp_incar`、`vasp_util.vasp_kpoints`、`vasp_util.vasp_poscar`、`vasp_util.vasp_poscar_analyzer`、`vasp_util.vasp_outcar`、`vasp_util.vasp_potcar`、`vasp_util.vasp_log`、`vasp_util.config` です。利用例と実装が食い違う場合は、実際にインストールしたバージョンのソースを優先してください。


## 全メソッド・関数の参照先

使用例で紹介していないメソッドも含め、添付された実装の全クラス・関数の一覧と自動生成リファレンスを [API Reference](api_reference) に収録しています。


## 全 API の確認と保守

本ページは利用例です。全メソッドのシグネチャ、既存の説明、実装から抽出した return 式・例外・条件分岐は [API Reference](api_reference.md) を参照してください。API ページは `docs/generate_api.py` により再生成します。
