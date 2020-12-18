//
// Created by 史坤明 on 2020/10/15.
//

#include "py_c_interface.h"
#include <iostream>
#include <map>
schedulePtrVecType normal_sort_schedule_cxx(courseNameVecType target, preNameVecType pre, coursePointVecType target_point,
                                              courseNameVecType base, coursePointVecType base_point){
    std::vector<coursePtr> all_base_course;
    auto a = generateDAG( target, target_point, base, base_point, pre, all_base_course);
    auto b = normal_sort(a, all_base_course);
    return b;
}
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
std::vector<std::string> pre2post_re(schedulePtr thisTarget, schedulePtrVecType schedule){
    auto res = std::vector<std::string>();

    if (thisTarget->postCourse.empty()){
        res.push_back(thisTarget->course->name);
        return std::move(res);
    }

    for (const auto& post : thisTarget->postCourse){
        auto resFromRe = pre2post_re(post, schedule);
        res.insert(res.end(), resFromRe.begin(), resFromRe.end());
    }

    res.push_back(thisTarget->course->name);
    return res;
}
std::map<std::string, std::vector<std::string>> pre2post(schedulePtrVecType schedule){
    auto res = std::map<std::string, std::vector<std::string>>();
    for (auto i : schedule){
        auto preCourseName = i->course->name;
        auto postCourseNameVec = std::vector<std::string>();

        auto post = pre2post_re(i, schedule);
        // Remove this course
        post.erase(post.end()-1);
        // Remove same course name
        std::sort(post.begin(), post.end());
        auto unique_iter = std::unique(post.begin(), post.end());
        post.erase(unique_iter, post.end());
        // Add in map
        res[preCourseName] = std::move(post);
    }

    return res;
}

std::map<std::string, std::vector<std::string>> pre2post_cxx(courseNameVecType target, preNameVecType pre, coursePointVecType target_point,
                                                             courseNameVecType base, coursePointVecType base_point){
    auto res = normal_sort_schedule_cxx(target, pre, target_point, base, base_point);
    auto res2 = pre2post(res);
    return res2;
}