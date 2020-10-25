## 辅助排课系统

### File tree
```bash
.
├── c++_part
│   ├── course
│   │   ├── course.h
│   │   └── target_course.h
│   ├── CMakeLists.txt
│   ├── main.cpp
│   ├── binding
│   │   ├── py_bind.cpp
│   │   ├── py_c_interface.cpp
│   │   └── py_c_interface.h
│   └── sort
│       ├── normal_sort.cpp
│       ├── normal_sort.h
│       ├── generate.cpp
│       └── generate.h
└── project
    ├── add.cpp
    ├── add.h
    ├── CMakeLists.txt
    ├── main.cpp
    ├── py_qt
    │   ├── subwindow.py
    │   ├── c___part.cpython-37m-darwin.so
    │   ├── file.py
    │   ├── window.py
    │   └── widget.py
    ├── data
    │   └── course_private.txt
    └── course.txt
```


### 说明

用pybind11进行C++与python混合编程，python实现前端，C++实现后端。