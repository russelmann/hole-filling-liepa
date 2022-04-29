from hole_filling_liepa.core import fill_hole_liepa, find_boundary_loops
from hole_filling_liepa.utils import read_obj, write_obj


def main():
    vertices, faces = read_obj('../data/flat.obj')
    boundary_loops = find_boundary_loops(faces)
    area_patch = fill_hole_liepa(vertices, faces, boundary_loops[0], method='area')
    write_obj('../data/crenellations-patch-area.obj', vertices, area_patch)
    angle_patch = fill_hole_liepa(vertices, faces, boundary_loops[0], method='angle')
    write_obj('../data/crenellations-patch-angle.obj', vertices, angle_patch)


if __name__ == '__main__':
    main()
