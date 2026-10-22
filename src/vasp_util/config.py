"""
K.NAKADA, kengo.nakada@gmail.com (1st, 3rd varsion)
K.KOBAYASHI (2nd version)
"""

from typing import Any, Dict, List, Optional, Union, Tuple, Callable, Sequence
import yaml
import os

from x_logger import XLogger


class Config:

    # VASP parameter mirror
    vasp_incar_tags: Dict[str, Any] = {}
    vasp_kpoints_mode: Optional[str] = None
    vasp_kpoints_grid: Optional[Tuple[int, int, int]] = None
    vasp_kpoints_shift: Optional[Tuple[int, int, int]] = None
    vasp_kpoints_comment: Optional[str] = None

    # ------- DFT (VASP) --------
    dft_code: str = "Vasp"
    dft_log_dir: str = "vasp_log"
    vasp_name: str = "aaa"  # aaa.vasp
    run_mode: str = "local"

    #
    # VASP  path
    #
    # dft_bin = f"/home/hpc/vasp/bin/vasp-gamma"
    # dft_bin = f"/home/k/Downloads/vasp.6.4.2/bin/vasp_gam"
    # dft_bin = "/home/hpc/vasp/bin/vasp"
    dft_bin: Optional[str] = f"vasp_gam"

    num_procs: Optional[int] = 1

    mpi_cmd: Optional[str] = "mpirun"
    # mpi = f"mpirun -np {num_procs} {os.path.expanduser('/home/hpc/vasp/bin/vasp')}"

    mpi_flag: Optional[str] = "-np"

    dft_omp_num_threads: Optional[int] = None

    # default job_name
    job_cmd: Optional[str] = "qsub job_hpcs2024_node2.sh"

    # 自動セーブ
    auto_write: bool = True

    def __init__(
        self,
        yaml_path: Optional[str] = None,
        *,
        logger: Optional[XLogger] = XLogger(),
    ):
        """

        Args:
            yaml_path (str):
            logger (XLogger):
        """
        self._logger = logger

        # インスタンスで使いたいときだけ、ここで個別設定
        if yaml_path:
            self._load_yaml(yaml_path)

    @classmethod
    def load_yaml(cls, yaml_path=None):
        if yaml_path is None:
            yaml_path = os.environ.get("RMC_DFT_CONFIG_YAML")
            if yaml_path is None:
                return
        # with open(yaml_path, "r") as f:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for k, v in data.items():
            if hasattr(cls, k):
                setattr(cls, k, v)
            else:
                print("NO SUCH VAR:", k)

    def _load_yaml(self, yaml_path=None):
        # インスタンス用：インスタンスdictにのみ上書き
        self._logger.info(f"load_yaml: {yaml_path}")
        if yaml_path is None:
            yaml_path = os.environ.get("RMC_DFT_CONFIG_YAML")
            if yaml_path is None:
                return
        yaml_path = os.path.abspath(yaml_path)
        self._logger.info(f"abspath: {yaml_path}")
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        for k, v in data.items():
            setattr(self, k, v)


if __name__ == "__main__":
    config = Config("config.yml")
    print(config.num_procs)
    print(type(config.num_procs))
