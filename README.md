# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

Yet another collection of tools for working with VASP.

This package grew out of the VASP-related routines used in [RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/) and was separated into a reusable library (branched from 0.7.10).

ASE and pymatgen already provide a remarkable range of tools for generating, converting, and analyzing structures. There is little point in rewriting what they already do well. The reason for developing `vasp_util` was more specific: after reading VASP structures and results, I repeatedly needed analyses that I could not find in a directly usable form in the existing libraries. I implemented those routines as the need arose.

Not everything in this package is a new analysis method. File handling and basic coordinate operations provide the common groundwork for the analysis routines. Where ASE or pymatgen already provides what is needed, using it makes more sense than duplicating it; parts of the implementation already use these libraries. The package may also serve as a higher-level interface to them, without making reimplementation an objective.

## Background

From around 2010 to 2015, I developed [sae](https://github.com/ohara-lab-su/sae), a collection of tools related to VASP and crystal structures. Much of the experience gained then still informs these tools.

As features accumulated, sae became too large, and my limited understanding of Python at the time left it with several design problems. Meanwhile, ASE and pymatgen had grown substantially more capable, so there was less reason to maintain sae. It remained shelved for years.

Nevertheless, while writing other VASP tools, I kept needing common routines for handling POSCAR structures and extracting information from calculation results. I wrote the necessary parts separately for each project, eventually leaving similar code scattered across multiple programs.

Rather than redesign sae from scratch, I collected the routines actually needed by RMC-DFT into a smaller set of classes. `vasp_util` is the result of extracting those classes into a standalone package.

## Current scope

The package handles POSCAR lattice and coordinate data, coordinate transformations, interatomic distances and neighbors under periodic boundary conditions, atomic displacements, INCAR and KPOINTS editing, POTCAR assembly, energies, forces and magnetic moments from OUTCAR, and VASP execution and log management. It also includes structure-data exchange between RMC and VASP, reflecting its origins in RMC-DFT.

Input/output and basic geometry operations are the foundation, not the main claim of originality. The emphasis is on the analysis of structures and calculation results. Whether an individual analysis is absent from ASE, pymatgen, or related packages must be established by comparing the actual computed quantities and algorithms, not merely the method names.

See the [documentation](https://ohara-lab-su.github.io/vasp_util/) for usage and API details. Some API descriptions are generated from static source-code inspection; these should not be confused with runtime validation against calculation data.
