cmake_minimum_required(VERSION 3.17)
project(c___part)

set(CMAKE_CXX_STANDARD 14)
#add_subdirectory(pybind11)
#pybind11_add_module(c___part main.cpp sort/generate.cpp sort/normal_sort.cpp binding/py_c_interface.cpp binding/py_bind.cpp)

add_executable(c___part main.cpp sort/generate.cpp sort/normal_sort.cpp binding/py_c_interface.cpp)