import os
import unittest

import numpy as np

from hole_filling_liepa.hole_filling_liepa import read_obj, write_obj


class Test_obj(unittest.TestCase):

    def test_read_obj(self):
        vertices, faces = read_obj('../data/ico.obj')

        self.assertEqual(len(vertices), 39)
        self.assertEqual(len(faces), 67)

    def test_write_obj(self):
        file_path = '../data/tmp_test.obj'
        vertices, faces = np.identity(3), [[0, 1, 2]]
        write_obj(file_path, vertices, faces)
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
