# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fvasp_util-181717?logo=github)](https://github.com/ohara-lab-su/vasp_util/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/vasp_util/en/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)

`vasp_util` is a Python library for working with VASP input and output files, atomic structures, calculations, and
results in research workflows. Its VASP-related tools and classes were first organized as an internal foundation for
[RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/). Following a decision to develop the RMC and VASP components independently, this foundation was separated into `vasp_util` starting with RMC-DFT version 0.7.10.

[ASE](https://ase-lib.org/) and [pymatgen](https://pymatgen.org/) already provide extensive support for structures and
VASP files. `vasp_util` is not intended to replace them. It uses existing libraries where appropriate and brings
together operations repeatedly needed in practice: managing calculation files, addressing atoms by element-specific site
numbers, inspecting neighbors and atomic displacements, organizing results, and exchanging structures with RMCProfile.
Even when the underlying operation exists elsewhere, a higher-level API that preserves a particular workflow and its
input/output conventions can still be useful.

## Background

Between approximately 2010 and 2015, I developed [sae](https://github.com/ohara-lab-su/sae), a collection of VASP and crystal-structure tools. As features accumulated, the project became unwieldy and developed design problems, and I eventually stopped using it. Meanwhile, ASE and pymatgen advanced substantially, reducing the need to rebuild sae as it was.

The more direct basis for the present library was `x_poscar`, a set of tools used in other analysis work. It included POSCAR-related operations developed for workflows involving LAMMPS, Bader charge and charge-density analysis, and vibrational analysis. Rather than consolidating every VASP utility developed over the years, I reorganized and adapted primarily these `x_poscar` tools into classes and functions for VASP file handling and structural analysis.

I subsequently reorganized these tools, primarily based on `x_poscar`, **within RMC-DFT** as the shared foundation of tools and classes for its VASP-related operations. This RMC-DFT component is the direct predecessor of the present `vasp_util`.

Later, the development approach changed: the RMC and VASP components would be separated and developed independently. The VASP tool foundation was therefore extracted as `vasp_util`. Functionality specific to coupling RMC and VASP, including their coordinated calculation workflows, belongs in the separate `rmc_dft` package rather than either independent utility library.

This is not a completed consolidation or cleanup of all the earlier tools. Returning to this development work after some time, I found that ASE and pymatgen had become considerably more capable than I had expected. Some functionality therefore still overlaps with these libraries. Further consolidation should preserve the input/output conventions and research workflows that matter while replacing redundant implementations where existing libraries provide suitable alternatives.

## Main functionality

- **POSCAR and site indexing:** `VaspPoscar` reads lattice vectors and Direct/Cartesian coordinates and exposes both
  element-specific site numbers and global atom indices. Public site indices are generally one-based. The reader
  accounts for single scaling factors, negative volume specifications, three-component scaling, and Selective dynamics
  headers.
- **Structure and MD analysis:** `VaspPoscarAnalyzer` provides interatomic distances, element-filtered and
  distance-sorted neighbors, displacements of identically indexed sites between structures, threshold-based jump
  detection, and site-motion analysis across MD snapshots. Corresponding site indices are assumed to identify the same
  atoms.
- **Periodic-cell geometry:** `cell_geometry` supplies cell volumes, coordinate conversion, wrapping, periodic-image
  searches, and pair-specific minimum-distance checks. `minimum_image_vector` searches a finite range of lattice images
  using Cartesian distances.
- **INCAR and KPOINTS:** `VaspIncar` combines pymatgen's `Incar` data model with the original file lines to edit tags
  while retaining comments and much of the existing layout. `VaspKpoints` uses pymatgen's `Kpoints` to manage
  Gamma/Monkhorst-Pack meshes, shifts, and comments. Both support configurable automatic writing.
- **POTCAR:** `VaspPotcarBuilder` assembles POTCAR files from locally available PAW datasets, using a defined
  per-element preference order and checking which files exist. It does not determine the scientifically optimal
  potential automatically.
- **OUTCAR:** `VaspOutcar` extracts electronic-iteration and ionic-step energies (TOTEN, energy without entropy, and
  sigma→0), positions, forces, and atomic and total magnetic moments. It raises an exception when its completion check
  fails.
- **Execution and result handling:** `Vasp` coordinates input preparation, INCAR/KPOINTS settings, local/MPI/job-command
  execution, result collection and backup, continuation from CONTCAR, and CFG conversion. `VaspLog` manages logs,
  including copying and organizing ordinary and `.gz` files.
- **RMCProfile interchange:** `poscar2cfg` and related functions convert POSCAR/CONTCAR-like files into RMCProfile CFG.
  The format-specific mapping uses half-sized CFG cell vectors and transforms fractional coordinates as `2f−1`.
  Utilities also handle XDATCAR extraction and assist with VASP4-to-VASP5 POSCAR conversion.

## Relationship to ASE and pymatgen

Not every function in `vasp_util` represents a new algorithm. ASE and pymatgen already cover VASP file I/O, coordinate
conversion, periodic distances and neighbors, input files, output parsing, and calculation execution. Parts of `Vasp`
use `ase.io`; `VaspIncar` and `VaspKpoints` directly use pymatgen.

The principal distinction is **the combination of operations and their interface conventions**. For example,
`VaspPoscarAnalyzer` connects element-local site numbering to global indices and returns neighbors with their species,
site numbers, distances, and displacement vectors. It also compares identically indexed atoms across MD snapshots. These
operations can be composed from existing libraries, but here they are provided as research-oriented workflows.
`VaspIncar` adds line-aware editing to dictionary-like tag management, while `Vasp` covers preparation, execution,
collection, and RMC conversion rather than acting solely as a calculator.

Existing ASE/pymatgen implementations can replace internal routines where they preserve the required behavior.
Equivalence must be checked at the level of coordinate conventions, atom indexing, periodic boundaries, file
preservation, exceptions, and return values—not merely function names. In particular,
`VaspPoscar.apply_pbc_shortest_direct_vector` compares candidate lengths in fractional coordinates, whereas
`cell_geometry.minimum_image_vector` compares Cartesian lengths. These implementations need not agree for skewed cells;
this is a limitation of the current code, not a claim of a distinct physical definition.

## Execution-script architecture in v0.0.8

The principal architectural change is the **separation of reusable execution logic from user-editable calculation parameters**. Previously, complete calculation scripts were copied from `examples/` or similar directories into each working directory. This also duplicated execution logic, leaving old copies behind after fixes or package upgrades.

The implemented division of responsibilities is:

- **Library (`src/vasp_util/`)**: reusable VASP file and structure APIs, including the existing `vasp.py` library module.
- **Runner (`src/vasp_util/runners/run_vasp.py`)**: installed execution function `run_vasp(...)`. Its original standalone `__main__` workflow is retained for development and testing.
- **Editable launcher (`scripts/vasp.py`)**: creates `Config`, `XLogger`, `VaspLog`, and `VaspIncar`, invokes the editable initialization function, then calls `run_vasp(...)` with all parameters explicitly specified.
- **Editable initialization (`scripts/vasp_init.py`)**: contains `run_vasp_init(...)` for preparing KPOINTS, POTCAR, and INCAR. It is derived from the supplied `rmc_vasp_init.py`; the original standalone entry point is retained.
- **Installer (`src/vasp_util/install.py`)**: copies packaged scripts into the current working directory, without running VASP.

The launcher preserves the prior standalone script's `sleep 5` and `ls -la ./` commands used as a Fugaku cache workaround. Edit or remove these commands locally as needed. The launcher passes `log_dir_vasp=None`, `run_mode=None`, and `postprocess_mode=True` explicitly; the runner determines the log directory and resolves the run mode from `config.run_mode`.

### Installing editable templates

After installing the package, run the following in the calculation working directory:

```bash
vasp_util install
```

The `.py` and `.sh` files packaged from the repository-root `scripts/` directory are copied into the **current working directory**. Existing files are skipped. To overwrite them explicitly:

```bash
vasp_util install --force
```

Edit `vasp_init.py` and, when needed, `vasp.py` locally. Run the calculation with `python vasp.py`. Package upgrades do not update existing local copies. `--force` can overwrite local modifications. Moving execution logic into runners does not make locally edited templates auto-updating.

## Notes on use

Some POSCAR/CFG conversion paths assume particular line layouts and Direct coordinates. Displacements between MD
snapshots assume consistent atom indexing and do not reconstruct unwrapped trajectories over multiple steps. Check that
the selected routines match the input format and cell geometry before using their results in analysis.

See the [documentation](https://ohara-lab-su.github.io/vasp_util/) for API details and examples.
