#include "pybind11/pybind11.h"
#include "add.h"
#include <pybind11/stl.h>
namespace py = pybind11;



PYBIND11_MODULE(example, m) {
m.doc() = "pybind11 example plugin"; // optional module docstring

m.def("add", &add, py::arg("i"), py::arg("j"));
}