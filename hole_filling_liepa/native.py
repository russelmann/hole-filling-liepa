from collections import deque
from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from module.hole_filling_liepa.utils import read_obj, write_obj


def find_boundary_loops(faces: npt.ArrayLike) -> List[List[int]]:
    """Find boundary loops in a triangle mesh represented by faces.

    Note: Singular vertices are not supported.

    :param faces: Mesh faces.
    :return: List of consecutive boundary loop vertex indices.
    """
    faces = np.asarray(faces)
    edges = np.r_[faces[:, :2], faces[:, 1:], faces[:, (2, 0)]]
    _, edge_index, edge_counts = np.unique(np.sort(edges), axis=0, return_index=True, return_counts=True)
    edge_index = edge_index[edge_counts == 1]
    boundary_map = {edge[0]: edge[1] for edge in edges[edge_index, :]}
    boundary_loops, boundary_loop, vertex = [], None, None
    while True:
        if vertex is None:
            if not boundary_map:
                break
            vertex = next(iter(boundary_map))
            boundary_loop = deque([vertex])
        else:
            next_vertex = boundary_map.pop(vertex)
            if next_vertex == boundary_loop[0]:
                boundary_loop.reverse()
                boundary_loops.append(list(boundary_loop))
                vertex = None
            else:
                boundary_loop.append(next_vertex)
                vertex = next_vertex
    return boundary_loops


def compute_triangle_area(t: npt.ArrayLike) -> float:
    """Compute area of a triangle with vertices located at rows of `t`.

    :param t: 3 x 3 matrix with vertex coordinates per-row.
    :return: The area of the triangle.
    """
    t = np.asarray(t)
    return 0.5 * abs(np.linalg.norm(np.cross(t[1] - t[0], t[2] - t[0])))


def compute_triangle_normal(t: npt.ArrayLike) -> npt.NDArray:
    """Compute normal of a triangle with vertices located at rows of `t`.

    :param t: 3 x 3 matrix with vertex coordinates per-row.
    :return: The normal of the triangle.
    """
    t = np.asarray(t)
    normal = np.cross(t[1] - t[0], t[2] - t[0])
    return normal / np.linalg.norm(normal)


def cycle3_origins(b_face: npt.ArrayLike, n: int) -> Tuple[int, int]:
    """Find vertex index origins of face indexed by boundary loop.

    :param b_face: Face indexed by boundary loop (-1 if vertex is not in boundary loop).
    :param n: Count of vertices in the boundary loop.
    :return: Vertex origin indices.
    """
    if len(b_face) != 3:
        raise ValueError('Input face in not triangular.')
    i, j, k = sorted(b_face)
    if i == -1:
        if j == 0 and k == n - 1:
            return n - 1, -1
        if j + 1 == k:
            return j, -1
        return -1, -1  # Internal face.
    if i == 0 and k == n - 1:
        if j == 1:
            return n - 1, 0
        if j == n - 2:
            return n - 2, n - 1
        raise RuntimeError('Error in boundary loop.')
    return i, j


def fill_hole_liepa(vertices: npt.ArrayLike,
                    faces: npt.ArrayLike,
                    boundary_loop: npt.ArrayLike,
                    method: str = 'areas') -> npt.NDArray:
    """Fill a hole enclosed by vertex indices `boundary_loop` in a triangle mesh defined by its `vertices` and `faces`.

    :param vertices: Mesh vertices.
    :param faces: Mesh faces.
    :param boundary_loop: Boundary loop around a hole to be filled.
    :param method: Hole filling method, 'areas' (à la Barequet and Sharir) or 'angle' (Liepa).
    :return: New triangles filling the hole.
    """
    vertices, faces, boundary_loop = np.asarray(vertices), np.asarray(faces), np.asarray(boundary_loop)
    n = len(boundary_loop)

    # Weights: first index is (vertex_index_offset - 1); second index is start vertex index.
    # For example, areas[3][5] is weight of minimum weight triangulation from vertex 5 till vertex 9 (= 5 + 1 + 3).
    # Indexing of lambdas matches indexing of areas.
    areas = [np.zeros(i) for i in range(n - 1, 0, -1)]
    areas[1] = np.array([compute_triangle_area(vertices[boundary_loop[i:i + 3]]) for i in range(n - 2)])
    lambdas = [np.zeros(i if i < n - 2 else 0, dtype=int) for i in range(n - 1, 0, -1)]  # Indexing offset.
    if method == 'area':
        # Area-based approach à la Barequet and Sharir. Areas are used as weights.
        for j in range(3, n):
            for i in range(n - j):
                min_area, optimal_m = float('inf'), None
                for m in range(j - 1):
                    m1, i1 = j - m - 2, i + 1 + m
                    area = areas[m][i] + areas[m1][i1]
                    area += compute_triangle_area(vertices[boundary_loop[[i, i1, i + j]]])
                    if area < min_area:
                        min_area, optimal_m = area, m
                areas[j - 1][i], lambdas[j - 1][i] = min_area, i + 1 + optimal_m
    elif method == 'angle':
        # Dihedral-angle-based approach by Liepa. Angle-area pairs are used as weights.
        b = -np.ones(vertices.shape[0], dtype=int)
        for i, index in enumerate(boundary_loop):
            b[index] = i
        b_faces = b[faces]  # Faces expressed via boundary loop indices (-1 if vertex is not boundary in loop).
        # Indexing of edge face normals matches indexing of weights.
        edge_face_normals = [np.zeros((i if i < n - 1 else n, 3)) for i in range(n - 1, 0, -1)]
        # Note: edge_face_normals[n - 1][0] is not needed, it is defined for logical simplicity.
        for face, b_face in zip(faces, b_faces):
            if sum(b_face == -1) < 2:
                normal = compute_triangle_normal(vertices[face])
                i, j = cycle3_origins(b_face, n)  # A triangular face can have 0, 1, or 2 edges on the boundary loop.
                if i != -1:
                    edge_face_normals[0][i] = normal
                if j != -1:
                    edge_face_normals[0][j] = normal
        for i in range(n - 2):
            edge_face_normals[1][i] = compute_triangle_normal(vertices[boundary_loop[i:i + 3]])
        dot_products = [np.ones(i) for i in range(n - 1, 0, -1)]
        dot_products[1] = np.minimum((edge_face_normals[1] * edge_face_normals[0][1:-1]).sum(axis=1),
                                     (edge_face_normals[1] * edge_face_normals[0][:-2]).sum(axis=1))
        for j in range(3, n):
            for i in range(n - j):
                max_d, min_area = -float('inf'), float('inf')
                optimal_m, optimal_normal = None, None
                for m in range(j - 1):
                    m1, i1 = j - m - 2, i + 1 + m
                    triangle = vertices[boundary_loop[[i, i1, i + j]]]
                    normal = compute_triangle_normal(triangle)
                    d = min(np.dot(normal, edge_face_normals[m][i]), np.dot(normal, edge_face_normals[m1][i1]))
                    if i == 0 and j == n - 1:
                        d = min(d, np.dot(normal, edge_face_normals[0][n - 1]))
                    d = min(d, dot_products[m][i], dot_products[m1][i1])
                    area = areas[m][i] + areas[m1][i1] + compute_triangle_area(triangle)
                    if max_d < d or (max_d == d and area < min_area):
                        max_d, min_area, optimal_m, optimal_normal = d, area, m, normal
                dot_products[j - 1][i], areas[j - 1][i] = max_d, min_area
                lambdas[j - 1][i], edge_face_normals[j - 1][i] = i + 1 + optimal_m, optimal_normal
    else:
        raise ValueError(f'Method "{method}" is not supported.')

    # Reconstruct triangulation.
    sections, triangles = deque([(0, n - 1)]), deque()
    while sections:
        d, b = sections.pop()
        if b - d == 2:
            m = d + 1
        else:
            m = lambdas[b - d - 1][d]
        triangles.append((d, m, b))
        if 1 < m - d:
            sections.append((d, m))
        if 1 < b - m:
            sections.append((m, b))
    return boundary_loop[np.array(triangles)]


def main():
    from sys import argv
    import os
    file_path = argv[1]
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    vertices, faces = read_obj(file_path)
    for i, boundary_loop in enumerate(find_boundary_loops(faces)):
        hole_faces = fill_hole_liepa(vertices, faces, boundary_loop, 'angle')
        write_obj(f'{file_name}-hole-{i:02d}.obj', vertices, hole_faces)


if __name__ == '__main__':
    main()
