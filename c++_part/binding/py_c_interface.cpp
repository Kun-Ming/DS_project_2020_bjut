//
// Created by 史坤明 on 2020/10/15.
//

#include "py_c_interface.h"
#include <iostream>
#include <map>
std::map<std::string, size_t> normal_sort_cxx(courseNameVecType target, preNameVecType pre, coursePointVecType target_point,
                                         courseNameVecType base, coursePointVecType base_point){
    std::vector<coursePtr> all_base_course;
    auto a = generateDAG( target, target_point, base, base_point, pre, all_base_course);
    auto b = normal_sort(a, all_base_course);

    auto compare =
            [&](schedulePtr a, schedulePtr b) -> bool{
                return a->semester < b->semester;
            };
    std::sort(b.begin(), b.end(), compare);
    b=check_point(b);
    auto scheduleTranser = plain_schedule();
    auto plain_c = scheduleTranser.changeTo(b);

    std::map<std::string, size_t> ret;
    for (auto plain : plain_c){
        ret[plain.courseName] = plain.semester;
    }
    return ret;
}