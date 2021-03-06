//
// Created by 史坤明 on 2020/10/15.
//

#include "pybind11/pybind11.h"
#include "py_c_interface.h"
#include <pybind11/stl.h>
namespace py = pybind11;

PYBIND11_MODULE(c___part, m){
    m.doc() = "interface between UI and sort";
    m.def("normal_sort_cxx", &normal_sort_cxx, "using c++ to sort");
    m.def("pre2post_cxx", &pre2post_cxx);
}

