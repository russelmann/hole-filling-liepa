import os

from hole_filling_liepa.core import fill_hole_liepa
from hole_filling_liepa.native import fill_hole_liepa as fill_hole_liepa_native, find_boundary_loops, read_obj
from hole_filling_liepa.utils import timer


def main():
    file_names = ['ico.obj', 'sphere-1.obj', 'sphere-2.obj', 'bunny-1.obj']
    methods = ['area', 'angle']
    for file_name in file_names:
        vertices, faces = read_obj(os.path.join('../data/', file_name))
        boundary_loops = find_boundary_loops(faces)
        holes_text = '1 hole' if len(boundary_loops) == 1 else f'{len(boundary_loops)} holes'
        print(f'Comparing file "{file_name}" with {holes_text}.')
        for method in methods:
            print(f'Method "{method}":')
            with timer('Native'):
                for boundary_loop in boundary_loops:
                    fill_hole_liepa_native(vertices, faces, boundary_loop, method)
            with timer('Binding'):
                for boundary_loop in boundary_loops:
                    fill_hole_liepa(vertices, faces, boundary_loop, method)


if __name__ == '__main__':
    main()
