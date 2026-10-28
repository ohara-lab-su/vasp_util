# Changelog

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/CHANGELOG.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/CHANGELOG.ja.md)

## v0.0.8 - 2026-10-28

- Added `scripts/vasp.py`, an editable launcher that explicitly initializes `Config`, logging, and VASP inputs, and passes all arguments to `run_vasp(...)`.
- Moved execution into `src/vasp_util/runners/run_vasp.py` and preserved its original standalone `__main__` block for development and testing.
- Added `scripts/vasp_init.py` from the supplied `rmc_vasp_init.py`, retaining calculation settings and preserving its standalone entry point.
- Preserved the former standalone launcher’s Fugaku cache-workaround commands in the editable launcher.
- Updated the English/Japanese documentation and kept `vasp_util install` and `--force` behavior. The package version is 0.0.8.

## v0.0.7 - 2026-10-28

### Execution architecture (major change)

- Documented the separation of **user-editable calculation parameters (`*_init.py`) from normally unchanged execution logic**, replacing the former practice of copying complete scripts from `examples/`.
- Established `src/vasp_util/runners/` as the intended namespace for execution logic, distinct from the existing library module `vasp.py`.
- Reserved repository-root `scripts/` for editable templates distributed through `install.py`. The same separation is intended for `rmc_util`, allowing `rmc_dft` to remain a simpler integration layer.
- Migration of runners and inclusion of specific templates have not been verified from the supplied files and are not claimed as complete.

### Installation of editable scripts

- Added `src/vasp_util/install.py` to copy editable calculation scripts into the current working directory.
- Registered `vasp_util = "vasp_util.install:main"` under `[project.scripts]` in `pyproject.toml`.
- Packaged `.py` and `.sh` files from the repository-root `scripts/` directory under `share/vasp_util/scripts`.
- Added `vasp_util install` to copy scripts without overwriting existing files and `vasp_util install --force` for explicit overwriting.
- Documented this workflow in the English and Japanese READMEs. Copied scripts are not automatically updated when the package is upgraded.

Earlier release history was not provided with the source files for this update.
