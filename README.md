# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

[![GitHub](https://img.shields.io/badge/GitHub-ohara--lab--su%2Fvasp_util-181717?logo=github)](https://github.com/ohara-lab-su/vasp_util/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Documentation-222222?logo=githubpages&logoColor=white)](https://ohara-lab-su.github.io/vasp_util/en/)
[![Ohara Lab](https://img.shields.io/badge/Ohara%20Lab-Home-4B5563?logo=homeassistant&logoColor=white)](https://ohara-lab-su.github.io/index.en.html)

`vasp_util` is a Python library for working with VASP input and output files, atomic structures, calculations, and
results in research workflows. It was extracted from the VASP-related routines
in [RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/) starting with version 0.7.10.

[ASE](https://ase-lib.org/) and [pymatgen](https://pymatgen.org/) already provide extensive support for structures and
VASP files. `vasp_util` is not intended to replace them. It uses existing libraries where appropriate and brings
together operations repeatedly needed in practice: managing calculation files, addressing atoms by element-specific site
numbers, inspecting neighbors and atomic displacements, organizing results, and exchanging structures with RMCProfile.
Even when the underlying operation exists elsewhere, a higher-level API that preserves a particular workflow and its
input/output conventions can still be useful.

## Background

Between approximately 2010 and 2015, I developed [sae](https://github.com/ohara-lab-su/sae), a collection of VASP and
crystal-structure tools. As features accumulated, the project became unwieldy and suffered from design problems.
Meanwhile, ASE and pymatgen grew considerably, reducing the need to rebuild sae.

Nevertheless, work on VASP-based research programs kept calling for specific structure analyses and file operations, and
similar routines accumulated across projects. I gathered the parts actually used in RMC-DFT into smaller classes and
functions and extracted them as `vasp_util`.

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

## Execution-script architecture in v0.0.7

The principal architectural change is the **separation of reusable execution logic from user-editable calculation parameters**. Previously, complete calculation scripts were copied from `examples/` or similar directories into each working directory. This also duplicated execution logic, leaving old copies behind after fixes or package upgrades.

The intended division of responsibilities is:

- **Library (`src/vasp_util/`)**: reusable VASP file I/O, structural analysis, and related APIs. The existing library module `vasp.py` belongs here.
- **Runners (`src/vasp_util/runners/`)**: calculation preparation, execution, and result handling that users normally do not edit. A runner `vasp.py` has its own namespace to avoid collision with the existing library `vasp.py`.
- **Editable templates (repository-root `scripts/`)**: `*_init.py` and similar parameter/configuration files, intended for local modification. They invoke runner functionality instead of carrying independent copies of the execution implementation.
- **Installer (`src/vasp_util/install.py`)**: copies packaged editable templates into the current working directory. It does not execute VASP.

This allows calculation parameters to remain local while execution logic is maintained through package upgrades. The same separation is intended for `rmc_util`; `rmc_dft` can then act as a thin integration layer invoking the two packages, reducing duplicated scripts and version mismatches in standalone and coupled workflows.

**Implementation status:** the install command and template packaging configuration are included in v0.0.7. The supplied files do not establish whether migration to `runners/` or packaging of specific `*_init.py` templates has been completed. The structure above describes the agreed architecture, not unverified completed work.

### Installing editable templates

After installing the package, run the following in the calculation working directory:

```bash
vasp_util install
```

The `.py` and `.sh` files packaged from the repository-root `scripts/` directory are copied into the **current working directory**. Existing files are skipped. To overwrite them explicitly:

```bash
vasp_util install --force
```

Edit the copied `*_init.py` or other parameter templates locally. Package upgrades do not update existing local copies. `--force` can overwrite local modifications. Moving execution logic into runners does not make locally edited templates auto-updating.

## Notes on use

Some POSCAR/CFG conversion paths assume particular line layouts and Direct coordinates. Displacements between MD
snapshots assume consistent atom indexing and do not reconstruct unwrapped trajectories over multiple steps. Check that
the selected routines match the input format and cell geometry before using their results in analysis.

See the [documentation](https://ohara-lab-su.github.io/vasp_util/) for API details and examples.
