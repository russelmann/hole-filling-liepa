#include <limits>
#include <array>
#include <vector>
#include <list>
#include <set>
#include <unordered_map>

#include "hole_fillig_liepa.hpp"

namespace hole_filling_liepa {

	using std::vector;
	using std::list;
	using std::set;
	using std::unordered_map;

	using Eigen::Vector2i;
	using Eigen::Vector3i;
	using Eigen::Vector3d;
	using Eigen::VectorXi;
	using Eigen::VectorXd;
	using Eigen::MatrixX2i;
	using Eigen::MatrixX3i;
	using Eigen::MatrixX3d;

	typedef std::array<int, 2> array2i;
	typedef std::array<int, 3> array3i;

	vector<VectorXi> find_boundary_loops(const MatrixX3i faces) {
		vector<VectorXi> boundary_loops;
		set<std::pair<int, int>> edges;
		for (int i = 0; i < faces.rows(); ++i) {
			for (int j = 0; j < 3; ++j) {
				int a = faces(i, j);
				int b = faces(i, (j + 1) % 3);
				auto adj_edge = edges.find(std::make_pair(b, a));
				if (adj_edge == edges.end()) {
					edges.insert(std::make_pair(a, b));
				}
				else {
					edges.erase(adj_edge);
				}
			}
		}
		unordered_map<int, int> boundary_map;
		for (auto& edge : edges)
			boundary_map[edge.first] = edge.second;

		vector<int> boundary_loop;
		boundary_loop.reserve(boundary_map.size());
		int vertex = -1;
		while (true) {
			if (vertex == -1) {
				if (boundary_map.empty())
					break;
				vertex = boundary_map.begin()->first;
				boundary_loop.clear();
				boundary_loop.push_back(vertex);
			}
			else {
				int next_vertex = boundary_map[vertex];
				boundary_map.erase(vertex);
				if (next_vertex == boundary_loop[0]) {
					std::reverse(boundary_loop.begin(), boundary_loop.end());
					boundary_loops.emplace_back(Eigen::Map<VectorXi>(boundary_loop.data(), boundary_loop.size()));
					vertex = -1;
				}
				else {
					boundary_loop.push_back(next_vertex);
					vertex = next_vertex;
				}
			}
		}

		return boundary_loops;
	}

	// Compute area of a triangle based on vertex indices.
	double compute_triangle_area(const MatrixX3d& vertices, int i, int j, int k) {
		return fabs((vertices.row(j) - vertices.row(i)).cross(vertices.row(k) - vertices.row(i)).norm()) * 0.5;
	}

	// Compute normal of a triangle based on vertex indices.
	Vector3d compute_triangle_normal(const MatrixX3d& vertices, int i, int j, int k) {
		return (vertices.row(j) - vertices.row(i)).cross(vertices.row(k) - vertices.row(i)).normalized();
	}

	// Find vertex index origins of face indexed by boundary loop.
	Vector2i cycle3_origins(Vector3i b_face, int n) {
		std::sort(b_face.data(), b_face.data() + 3);
		int i = b_face[0];
		int j = b_face[1];
		int k = b_face[2];
		if (i == -1) {
			if (j == 0 && k == n - 1)
				return Vector2i{ n - 1, -1 };
			if (j + 1 == k)
				return Vector2i{ j, -1 };
			return Vector2i{ -1, -1 };
		}
		if (i == 0 && k == n - 1) {
			if (j == 1)
				return Vector2i{ n - 1, 0 };
			if (j == n - 2)
				return Vector2i{ n - 2, n - 1 };
			throw std::runtime_error("Error in boundary loop.");
		}
		return Vector2i{ i, j };
	}

	Eigen::MatrixX3i fill_hole_liepa(const MatrixX3d& vertices, const MatrixX3i& faces, const VectorXi& boundary_loop, const std::string& method) {
		Eigen::MatrixX3i hole_triangles;

		int n = boundary_loop.size();

		vector<VectorXd> areas;
		areas.reserve(n - 1);
		vector<VectorXi> lambdas;
		lambdas.reserve(n - 1);
		for (int i = n - 1; i > 0; --i) {
			areas.emplace_back(VectorXd::Zero(i));
			if (i < n - 2) {
				lambdas.emplace_back(VectorXi::Zero(i));
			}
			else {
				lambdas.emplace_back();
			}
		}

		VectorXd& areas1 = areas[1];
		for (int i = 0; i < n - 2; ++i) {
			areas1[i] = compute_triangle_area(vertices, boundary_loop[i], boundary_loop[i + 1], boundary_loop[i + 2]);
		}

		if (method == "area") {
			// Area-based approach à la Barequet and Sharir. Areas are used as weights.
			for (int j = 3; j < n; ++j) {
				for (int i = 0; i < n - j; ++i) {
					double min_area = std::numeric_limits<double>::max();
					int optimal_m = -1;
					for (int m = 0; m < j - 1; ++m) {
						int m1 = j - m - 2;
						int i1 = i + 1 + m;
						double area = areas[m][i] + areas[m1][i1];
						area += compute_triangle_area(vertices, boundary_loop[i], boundary_loop[i1], boundary_loop[i + j]);
						if (area < min_area) {
							min_area = area;
							optimal_m = m;
						}
					}
					areas[j - 1][i] = min_area;
					lambdas[j - 1][i] = i + 1 + optimal_m;
				}
			}
		}
		else if (method == "angle") {
			// Dihedral-angle-based approach by Liepa. Angle-area pairs are used as weights.
			//throw std::runtime_error("Method 'angle' is not yet implemented.");

			VectorXi b = VectorXi::Constant(vertices.rows(), -1);
			for (int i = 0; i < boundary_loop.size(); ++i) {
				b[boundary_loop[i]] = i;
			}

			MatrixX3i b_faces(faces.rows(), faces.cols());
			b_faces = faces.unaryExpr([b](int x) { return b[x]; });
			vector<MatrixX3d> edge_face_normals;
			edge_face_normals.reserve(n - 2);
			for (int i = n - 1; i > 0; --i) {
				edge_face_normals.emplace_back(MatrixX3d::Zero(i < n - 1 ? i : n, 3));
			}
			// Note: edge_face_normals[n - 1][0] is not needed, it is defined for logical simplicity.
			for (int f = 0; f < faces.rows(); ++f) {
				Vector3i b_face = b_faces.row(f);
				if ((b_face.array() == -1).count() < 2) {
					Vector3i face = faces.row(f);
					Vector3d normal = compute_triangle_normal(vertices, face[0], face[1], face[2]);
					auto ij = cycle3_origins(b_face, n);
					if (ij[0] != -1)
						edge_face_normals[0].row(ij[0]) = normal;
					if (ij[1] != -1)
						edge_face_normals[0].row(ij[1]) = normal;
				}
			}
			vector<VectorXd> dot_products;
			dot_products.reserve(n - 1);
			for (int i = n - 1; i > 0; --i) {
				dot_products.emplace_back(VectorXd::Ones(i));
			}
			for (int i = 0; i < n - 2; ++i) {
				edge_face_normals[1].row(i) = compute_triangle_normal(vertices, boundary_loop[i], boundary_loop[i + 1], boundary_loop[i + 2]);
			}
			auto& dot_products1 = dot_products[1];
			for (int i = 0; i < n - 2; ++i) {
				double dot_0 = edge_face_normals[1].row(i).dot(edge_face_normals[0].row(i));
				double dot_1 = edge_face_normals[1].row(i).dot(edge_face_normals[0].row(i + 1));
				dot_products1[i] = std::min(dot_0, dot_1);
			}
			for (int j = 3; j < n; ++j) {
				for (int i = 0; i < n - j; ++i) {
					double max_d = std::numeric_limits<double>::lowest();
					double min_area = std::numeric_limits<double>::max();
					int optimal_m = -1;
					Vector3d optimal_normal;
					for (int m = 0; m < j - 1; ++m) {
						int m1 = j - m - 2;
						int i1 = i + 1 + m;
						array3i triangle{ boundary_loop[i], boundary_loop[i1], boundary_loop[i + j] };
						Vector3d normal = compute_triangle_normal(vertices, triangle[0], triangle[1], triangle[2]);
						double d = std::min(normal.dot(edge_face_normals[m].row(i)), normal.dot(edge_face_normals[m1].row(i1)));
						if (i == 0 && j == n - 1)
							d = std::min(d, normal.dot(edge_face_normals[0].row(n - 1)));
						d = std::min(d, dot_products[m][i]);
						d = std::min(d, dot_products[m1][i1]);
						double area = areas[m][i] + areas[m1][i1] + compute_triangle_area(vertices, triangle[0], triangle[1], triangle[2]);
						if (max_d < d || (max_d == d && area < min_area)) {
							max_d = d;
							min_area = area;
							optimal_m = m;
							optimal_normal = normal;
						}
					}
					dot_products[j - 1][i] = max_d;
					areas[j - 1][i] = min_area;
					lambdas[j - 1][i] = i + 1 + optimal_m;
					edge_face_normals[j - 1].row(i) = optimal_normal;
				}
			}
		}
		else {
			throw std::invalid_argument("Unsupported method.");
		}

		// Reconstruct triangulation.
		list<array2i> sections;
		sections.emplace_back(array2i{ 0, n - 1 });
		list<array3i> triangles;
		while (!sections.empty()) {
			auto& section = sections.back();
			int d = section[0];
			int b = section[1];
			sections.pop_back();
			int m;
			if (b - d == 2) {
				m = d + 1;
			}
			else {
				m = lambdas[b - d - 1][d];
			}
			triangles.emplace_back(array3i{ d, m, b });
			if (1 < m - d)
				sections.emplace_back(array2i{ d, m });
			if (1 < b - m)
				sections.emplace_back(array2i{ m, b });
		}
		hole_triangles.resize(triangles.size(), 3);
		int i = 0;
		for (auto& triangle : triangles) {
			for (int j = 0; j < 3; ++j) {
				hole_triangles(i, j) = boundary_loop[triangle[j]];
			}
			++i;
		}

		return hole_triangles;
	}

}
