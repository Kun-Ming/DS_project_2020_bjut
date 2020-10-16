//
// Created by 史坤明 on 2020/10/15.
//

#include "pybind11/pybind11.h"
#include "py_c_interface.h"
#include <pybind11/stl.h>
namespace py = pybind11;

PYBIND11_MODULE(c___part, m){
    m.doc() = "interface between window and sort";
    m.def("interface1", &interface1, "using c++ to sort");
}

