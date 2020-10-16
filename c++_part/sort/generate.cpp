//
// Created by 史坤明 on 2020/10/11.
//
#include "generate.h"
#include "../course/target_course.h"
#include "../course/course.h"

struct find_type{
    std::string type;
    int index;
};

targetCoursePtr generate_target(courseVecType& target,
                                coursePointVecType& target_point,
                                preVecType& pre,
                                std::string target_this,
                                float target_point_this,
                                std::vector<std::string> pre_this,
                                std::vector<coursePtr>& all_base_course,
                                std::vector<targetCoursePtr>& all_target_course,
                                const int& index)
{
    std::vector<targetCoursePtr> target_vector; std::vector<coursePtr> base_vector;
    auto targetCourse = std::make_shared<target_course>(target_this, target_point_this);
    target.erase(target.begin() + index); target_point.erase(target_point.begin() + index); pre.erase(pre.begin() + index);

    for (auto prior = 0; prior != pre_this.size(); prior++){
        // find the pre course is target or base
        auto find =
                [&] () -> find_type {
                    for (auto i = 0; i < all_base_course.size(); i++){
                        if (all_base_course[i]->get_name() == pre_this[prior])
                            return find_type{"base", i};
                    }
                    for (auto i = 0; i < target.size(); i++){
                        if(target[i] == pre_this[prior])
                            return find_type{"target", i};
                    }
                    return find_type{"NOTFOUND"};
                };

        auto res = find();
        // has a base in pre
        if (res.type == "base"){
            base_vector.push_back(all_base_course[res.index]);
        }

        // has a target in pre or the last one, res returns NOTFOUND
        else {
            // find pre target if already generated
            auto find_in_targetVec =
                    [&](const std::string& pre) -> find_type{
                        for (auto i = 0; i < all_target_course.size(); i++){
                            if (all_target_course[i]->name == pre)
                                return find_type{"FIND", i};
                        }
                        return find_type{"FALSE", -1};
                    };
            auto res2 = find_in_targetVec(pre_this[prior]);

            //has generated
            if (res2.type == "FIND"){
                target_vector.push_back(all_target_course[res2.index]);
                all_target_course.erase(all_target_course.begin() + res2.index);
            }
            else{
                target_vector.push_back(generate_target(target, target_point, pre, target[res.index], target_point[res.index],
                                                        pre[res.index], all_base_course, all_target_course, res.index));
            }
        }
    }
    targetCourse->pre_base = base_vector; targetCourse->pre = target_vector;
    return targetCourse;
}


std::vector<targetCoursePtr> generateDAG(courseVecType& target,
                                         coursePointVecType& target_point,
                                         courseVecType& base,
                                         coursePointVecType& base_point,
                                         preVecType& pre,
                                         std::vector<coursePtr>& all_base_course)
{
    assert(target.size() == target_point.size());
    assert(target.size() == pre.size());
    assert(base.size() == base_point.size());

    for (auto i = 0; i != base.size(); i++){
        all_base_course.push_back(std::make_shared<course>(base[i], base_point[i]));
    }

    std::vector<targetCoursePtr> all_target_course;
    auto i = 0;
    auto target_size = target.size();
    while (target.size()){
        auto target_this = target[0];
        auto target_point_this = target_point[0];
        auto pre_this = pre[0];
        std::vector<targetCoursePtr> pre_course_this;

        all_target_course.push_back(generate_target(target, target_point, pre, target_this, target_point_this,
                        pre_this, all_base_course, all_target_course, 0));
        i++;
    }
    return all_target_course;
}


