import os
from hole_filling_liepa.core import fill_hole_liepa

from hole_filling_liepa.native import fill_hole_liepa as native_fill_hole_liepa
from hole_filling_liepa.native import find_boundary_loops, read_obj
from test import TEST_DATA_FOLDER


def test_bindings():
    file_path = os.path.join(TEST_DATA_FOLDER, 'ico.obj')
    vertices, faces = read_obj(file_path)
    boundary_loops = find_boundary_loops(faces)
    for method in ('area', 'angle'):
        triangles_native = native_fill_hole_liepa(vertices, faces, boundary_loops[0], method)
        triangles = fill_hole_liepa(vertices, faces, boundary_loops[0], method)
        assert (triangles_native == triangles).all()
