#include "Eigen/Eigen"

Eigen::Vector2i cycle3_origins(Eigen::Vector3i b_face, int n);

Eigen::MatrixX3i fill_hole_liepa(const Eigen::MatrixX3d& vertices, const Eigen::MatrixX3i& faces, const Eigen::VectorXi& boundary_loop, const std::string& method);
