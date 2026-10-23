# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

Yet another tool for making VASP easier to use, among the many such tools already available.

This package originated as a collection of VASP-related utilities used within [RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/). They were subsequently extracted into a standalone library (branched from version 0.7.10).

ASE and pymatgen provide extensive functionality, ranging from structure generation and conversion to various forms of analysis. However, simply reading a structure from a VASP input or output file and converting it into another representation is not particularly difficult to implement independently. The more important question, in my view, is what analytical capabilities are available for the structures and calculation results once they have been extracted.

For this reason, rather than depending on a large library solely for structure input and output, the approach here is to organize VASP file operations into small, independent components and make it possible to add and reuse analytical routines as needed. Of course, the goal is not to replace the advanced capabilities offered by ASE or pymatgen.

## Development Background

From around 2010 to 2015, I developed [sae](https://github.com/ohara-lab-su/sae), a general-purpose toolkit for crystal structures, including VASP-related functionality. The experience and knowledge accumulated through that work form the basis of the current tools.

However, as more features were added, sae grew excessively large. My limited understanding of Python at the time also contributed to a number of design problems.

Meanwhile, pymatgen and ASE had become extremely capable, further reducing the rationale for maintaining sae. As a result, the project was shelved for many years.

Nevertheless, while developing other tools that use VASP, I repeatedly encountered situations—particularly when manipulating structures described in POSCAR files—where something like sae would have been useful.

I worked around this by implementing similar routines separately in individual tools, but this eventually led to duplicated code scattered across multiple projects.

Redesigning sae in its entirety would have required substantial effort. Instead, I started by developing a small set of classes for VASP-related operations within RMC-DFT, keeping the functionality limited to what was actually needed.

These classes have now been extracted into `vasp_util`, a standalone package that can be reused by other tools.

In the end, this may have become another library similar to those already available. Even so, I hope to gradually consolidate the routines that have repeatedly been implemented in separate tools into this package.

## Current Components and Scope

The package currently covers reading lattice and coordinate data from POSCAR files, coordinate transformations, analysis of interatomic distances, neighboring atoms, and atomic displacements under periodic boundary conditions, editing INCAR and KPOINTS files, assembling POTCAR files, extracting energies, forces, and magnetic moments from OUTCAR files, and managing VASP execution and logs.

Given its origins in RMC-DFT, the package also covers transferring structural data between RMC and VASP. At this stage, the aim is not to build a comprehensive crystal-structure analysis environment, but to consolidate functions that have proved useful in actual calculations and analyses.

For examples and API details, see the [documentation](https://ohara-lab-su.github.io/vasp_util/).

## Implemented API and Manuals

The classes, methods, and top-level functions in the current implementation have been reviewed against the source code. A [user guide](https://ohara-lab-su.github.io/vasp_util/en/usage.html) and an [API Reference](https://ohara-lab-su.github.io/vasp_util/en/api_reference.html) are available. The API Reference combines module-specific descriptions with signatures and docstrings generated automatically by Sphinx autodoc.

Regarding dependencies, although the package provides its own structure-handling and analysis functionality, parts of the existing implementation do use ASE and pymatgen. The design should therefore not be interpreted as avoiding these libraries entirely.

### API Coverage and Updates

`docs/api_reference.md` provides access to the classes, methods, and functions from all ten source files supplied for the documentation update. Each entry includes the implementation signature and existing docstring, as well as extracted return expressions, conditional branches, exceptions, calls, and source line numbers. These pages can be regenerated with `docs/generate_api.py`. Information obtained through static source-code analysis should be distinguished from guarantees about runtime behavior.
