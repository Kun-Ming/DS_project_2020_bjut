//
// Created by 史坤明 on 2020/10/15.
//

#ifndef C___PART_PY_C_INTERFACE_H
#define C___PART_PY_C_INTERFACE_H
#include "../sort/normal_sort.h"
#include <map>

std::map<std::string, size_t> normal_sort_cxx(courseNameVecType target, preNameVecType pre, coursePointVecType target_point,
                                         courseNameVecType base, coursePointVecType base_point);
#endif //C___PART_PY_C_INTERFACE_H
