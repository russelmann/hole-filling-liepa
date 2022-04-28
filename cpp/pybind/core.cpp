#include "pybind11/pybind11.h"
#include "pybind11/eigen.h"
#include "pybind11/stl.h"
#include "pybind11/stl_bind.h"

#include "hole_fillig_liepa.hpp"

PYBIND11_MAKE_OPAQUE(std::vector<Eigen::VectorXi>);

namespace py = pybind11;

PYBIND11_MODULE(core, m) {
	m.doc() = "Hole filling algorithm by P. Liepa.";

	py::bind_vector<std::vector<Eigen::VectorXi>>(m, "VectorVectorXi");

	m.def("find_boundary_loops", &find_boundary_loops, "Find boundary loops of a triangle mesh.", py::arg("faces"));
	m.def("fill_hole_liepa", &fill_hole_liepa, "Coarsely fill a hole in a triangle mesh. Method is 'area' or 'angle'.", py::arg("vertices"), py::arg("faces"), py::arg("boundary_loop"), py::arg("method"));

#ifdef VERSION_INFO
	m.attr("__version__") = VERSION_INFO;
#else
	m.attr("__version__") = "dev";
#endif
}
