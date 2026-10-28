#!/usr/bin/env python3
"""VASP計算の起動スクリプト。計算条件は vasp_init.py で編集する。"""

import subprocess

from x_logger import XLogger
from vasp_util import Config, VaspIncar, VaspLog
from vasp_util.runners.run_vasp import run_vasp
from vasp_init import run_vasp_init


if __name__ == "__main__":
    config = Config("config.yml")
    logger = XLogger(log_level="debug", logger_name="rmc_vasp_run")
    vasp_log = VaspLog(logger=logger)
    vasp_incar = VaspIncar(config=config, logger=logger)
    msg = None

    # POSCARは事前に用意しておく。
    # 作業ディレクトリの編集可能な条件設定を適用する。
    run_vasp_init(
        config=config,
        vasp_incar=vasp_incar,
        vasp_kpoints=None,
        logger=logger,
    )

    # 旧単独実行スクリプトの富岳向けキャッシュ対策を維持する。
    subprocess.run(["sleep", "5"], check=True)
    subprocess.run(["ls", "-la", "./"], check=True)

    # デフォルト引数も省略せず明示する。
    run_vasp(
        config=config,
        vasp_log=vasp_log,
        vasp_incar=vasp_incar,
        log_dir_vasp=None,
        run_mode=None,
        postprocess_mode=True,
        msg=msg,
        logger=logger,
    )
