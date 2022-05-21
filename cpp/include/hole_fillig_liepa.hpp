#include "Eigen/Eigen"


namespace hole_filling_liepa {

	//Find boundary loops in a triangle mesh represented by faces.
	//
	// Note: Singular vertices are not supported.
	std::vector<Eigen::VectorXi> find_boundary_loops(const Eigen::Ref<Eigen::MatrixX3i> faces);

	// Fill a hole enclosed by vertex indices `boundary_loop` in a triangle mesh defined by its `vertices` and `faces`.
	// `method` can be either "area" or "angle".
	Eigen::MatrixX3i fill_hole_liepa(
		const Eigen::Ref<Eigen::MatrixX3d> vertices,
		const Eigen::Ref<Eigen::MatrixX3i> faces,
		const Eigen::Ref<Eigen::VectorXi> boundary_loop, 
		const std::string& method);

}
