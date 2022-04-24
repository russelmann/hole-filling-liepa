import numpy as np

from hole_filling_liepa.hole_filling_liepa import compute_triangle_area, compute_triangle_normal, find_boundary_loops, \
    read_obj


def test_explicit_triangles():
    triangles = [
        np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]]),
        np.array([[0, 1, 0], [0, 0, 0], [0, 0, 1]]),
        np.array([[0, 0, 0], [0, 0, 1], [1, 0, 0]]),
        np.identity(3),
    ]
    areas = [0.5, 0.5, 0.5, np.sqrt(3) / 2]
    normals = [[0, 0, 1], [-1, 0, 0], [0, 1, 0], np.ones(3) / np.sqrt(3)]
    for triangle, area, normal in zip(triangles, areas, normals):
        offset = [1, 0, 0]
        for _ in range(4):
            assert np.isclose(compute_triangle_area(triangle + offset), area)
            assert np.allclose(compute_triangle_normal(triangle + offset), normal)
            triangle *= 2
            area *= 4
            offset = [0] + offset[:2]


def test_degenerate_triangles():
    triangles = [
        np.zeros((3, 3)),
        np.array([[1, 0, 0], [1, 0, 0], [0, 0, 0]]),
        np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]]),
        np.array([[1, 1, 1], [0, 0, 0], [1, 1, 1]]),
    ]
    for triangle in triangles:
        offset = [1, 0, 0]
        for _ in range(4):
            assert np.isclose(compute_triangle_area(triangle + offset), 0.)
            assert np.isnan(compute_triangle_normal(triangle + offset)).all()
            triangle *= 2
            offset = [0] + offset[:2]


def test_boundary_loops():
    vertices, faces = read_obj('../data/ico.obj')
    boundary_loops = find_boundary_loops(faces)
    assert len(boundary_loops) == 2
    assert [2, 24, 23, 26, 17, 16, 0, 11] in boundary_loops
    assert [35, 29, 9] in boundary_loops
