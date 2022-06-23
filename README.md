***Warning: This repo is work in progress.***

# Hole Filling Liepa

![Build status](https://github.com/russelmann/hole-filling-liepa/actions/workflows/python-package-conda.yml/badge.svg?event=push)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![MIT License](https://img.shields.io/github/license/russelmann/hole-filling-liepa?color=informational)
![Platforms](https://img.shields.io/conda/pn/conda-forge/hole-filling-liepa)

Implementation of a coarse hole filling algorithm for triangle meshes. Main purpose is a Python package. Can be used as a C++ library as well.

Based on paper [Filling Holes in Meshes](https://diglib.eg.org/handle/10.2312/SGP.SGP03.200-206), P. Liepa, *Eurographics Symposium on Geometry Processing* (2003).


<p align="center">
  <img width="350" src="https://github.com/russelmann/hole-filling-liepa/blob/main/media/bunny-hole.png" alt="Bunny with hole">
  <img width="350" src="https://github.com/russelmann/hole-filling-liepa/blob/main/media/bunny-patched.png" alt="Patched Bunny">
</p>

## Installation

### Conda (recommended)

```
conda install -c conda-forge hole-filling-liepa
```

### PyPI (not recommended)

Only Python 3.9, x64 Windows and MacOS 11 are supported at this point.

```
pip install hole-filling-liepa
```

### From source using Conda

1. Clone this repository.
2. Create build environment running script `create-env.sh` in Linux/MacOS or `create-env.bat` in Windows.
3. Activate build environment. `conda activate ../hfl-env`
4. Build development version from source. `pip install -e .`

## Usage example

```python
from hole_filling_liepa.core import fill_hole_liepa, find_boundary_loops
from hole_filling_liepa.utils import read_obj, write_obj

vertices, faces = read_obj('mesh.obj')
boundary_loops = find_boundary_loops(faces)
patch_faces = fill_hole_liepa(vertices, faces, boundary_loops[0], method='angle')
write_obj('patch.obj', vertices, patch_faces)
```
