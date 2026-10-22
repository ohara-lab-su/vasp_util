# vasp_util

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.md)
[![ja](https://img.shields.io/badge/lang-ja-yellow.svg)](https://github.com/ohara-lab-su/vasp_util/blob/main/README.ja.md)

Yet another tool for making VASP easier to use, among the countless tools already out there.

This library was originally part of the [RMC-DFT](https://github.com/ohara-lab-su/rmc_dft/) package. It brings together VASP-related utilities that were used internally there and makes them available as a standalone library.

In many cases, pymatgen or ASE may be more convenient. Still, there are plenty of situations where having my own tools works better for me, so here I am, building another one.

## Background

Around 2010–2015, I developed [sae](https://github.com/ohara-lab-su/sae), a fairly comprehensive collection of tools for crystal structures, including VASP-related functionality. Much of the VASP know-how I accumulated back then forms the basis of my current tools.

However, as I kept adding features, sae grew rather large. Combined with my limited understanding of Python at the time, this led to various design problems.

Meanwhile, pymatgen and ASE had become remarkably useful. As a result, sae gradually lost much of its reason for existing and ended up sitting on the shelf for years.

Even so, whenever I developed new tools involving VASP, I often found myself wishing I had something like sae—especially when I simply wanted to manipulate structures described in POSCAR files.

I worked around this by implementing similar functionality separately in each tool, but that eventually left me with nearly identical code scattered across multiple projects.

Redesigning sae from scratch would have been a substantial undertaking. Instead, I started small, creating a minimal set of classes for handling VASP-related operations within RMC-DFT.

Those classes have now been extracted into a standalone package, `vasp_util`, so they can be reused more easily in other projects.

In the end, this may look much like other libraries already available. Nevertheless, I hope to gradually consolidate the functionality I have repeatedly implemented across my various tools into this package.
