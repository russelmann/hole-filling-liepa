import unittest

import numpy as np

from hole_filling_liepa.hole_filling_liepa import compute_triangle_area, compute_triangle_normal, find_boundary_loops, \
    read_obj


class Test_basic_compute(unittest.TestCase):

    def test_explicit_triangles(self):
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
                self.assertAlmostEqual(compute_triangle_area(triangle + offset), area)
                self.assertTrue(np.allclose(compute_triangle_normal(triangle + offset), normal))
                triangle *= 2
                area *= 4
                offset = [0] + offset[:2]

    def test_degenerate_triangles(self):
        triangles = [
            np.zeros((3, 3)),
            np.array([[1, 0, 0], [1, 0, 0], [0, 0, 0]]),
            np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]]),
            np.array([[1, 1, 1], [0, 0, 0], [1, 1, 1]]),
        ]
        for triangle in triangles:
            offset = [1, 0, 0]
            for _ in range(4):
                self.assertAlmostEqual(compute_triangle_area(triangle + offset), 0.)
                self.assertTrue(np.isnan(compute_triangle_normal(triangle + offset)).all())
                triangle *= 2
                offset = [0] + offset[:2]


class Test_basic_algorithms(unittest.TestCase):

    def test_boundary_loops(self):
        vertices, faces = read_obj('../data/ico.obj')
        boundary_loops = find_boundary_loops(faces)
        self.assertEqual(len(boundary_loops), 2)
        self.assertIn([2, 24, 23, 26, 17, 16, 0, 11], boundary_loops)
        self.assertIn([35, 29, 9], boundary_loops)


if __name__ == '__main__':
    unittest.main()
