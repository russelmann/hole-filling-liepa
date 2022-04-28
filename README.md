# Hole Filling Liepa

![Buidld status](https://github.com/russelmann/hole-filling-liepa/actions/workflows/python-package-conda.yml/badge.svg?event=push)

Implementation of coarse hole filling algorithm for triangle meshes. Main purpose is a Python package. Can be used as a C++ library as well.

Based on paper *Filling Holes in Meshes*, P. Liepa, Eurographics Symposium on Geometry Processing (2003).
https://diglib.eg.org/handle/10.2312/SGP.SGP03.200-206

### Installation

```
pip install hole-filling-liepa
```

### Example usage

```python
from hole_filling_liepa.core import fill_hole_liepa, find_boundary_loops
from hole_filling_liepa.utils import read_obj, write_obj

vertices, faces = read_obj('mesh.obj')
boundary_loops = find_boundary_loops(faces)
patch_faces = fill_hole_liepa(vertices, faces, boundary_loops[0], method='angle')
write_obj('patch.obj', vertices, patch_faces)
```
