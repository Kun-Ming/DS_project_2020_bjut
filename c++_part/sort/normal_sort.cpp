//
// Created by 史坤明 on 2020/10/11.
//

#include <array>
#include "normal_sort.h"
size_t semester = 8;

schedulePtrVecType normal_sort_re(coursePtr& target_this,
                                  schedulePtr& targetPostPtr,
                                  schedulePtrVecType& all_courseSchedule,
                                  schedulePtrVecType& baseCourseSchedule){
    schedulePtrVecType courseSchedule;
    auto thisTarget_SchedulePtr = std::make_shared<schedule>(target_this,
                                                             0,
                                                             targetPostPtr);
    // if target has target in pre
    // v2: Check if has pre
//    if (!target_this->pre.empty()){
    for (auto& i : target_this->pre){
        // Dealing with target in pre
        if (!i->study_type && !i->pre.empty()){

            // find target in pre
            auto var = normal_sort_re(i, thisTarget_SchedulePtr, all_courseSchedule, baseCourseSchedule);

            // insert target in pre
            courseSchedule.insert(courseSchedule.end(), var.begin(), var.end());

            // When this target has more than 1 target pre, find the biggest semester
            thisTarget_SchedulePtr->semester =var.back()->semester + 1 > thisTarget_SchedulePtr->semester?
                                              var.back()->semester + 1: thisTarget_SchedulePtr->semester;

//            courseSchedule.push_back(thisTarget_SchedulePtr);
            i->study_type = true;
        }
        // Dealing with base in pre
        else {
            if (!target_this->study_type) {
                thisTarget_SchedulePtr->semester = 2;
//                courseSchedule.push_back(thisTarget_SchedulePtr);

                for(auto& base : baseCourseSchedule){
                    if (i->name == base->course->name)
                        base->postCourse.push_back(thisTarget_SchedulePtr);
                }
            }
        }

    }
    courseSchedule.push_back(thisTarget_SchedulePtr);
//    }
    // target only has base in pre
//    else{
//        if (!target_this->study_type){
//            thisTarget_SchedulePtr->semester = 2;
//            courseSchedule.push_back(thisTarget_SchedulePtr);
//            target_this->study_type = true;
//        }
//    }
    target_this->study_type = true;
    return courseSchedule;
}

schedulePtrVecType normal_sort(std::vector<coursePtr>& targetCoursePtrVec, std::vector<coursePtr>& baseCoursePtrVec){
    schedulePtrVecType courseSchedule;
    schedulePtrVecType baseCourseSchedule;

    // lambda function, re assign semester number to each course
    auto re_number =
            [&](schedulePtrVecType& course){
                size_t min = 8;
                for (auto& j : course)
                    if(j->semester < min)
                        min = j->semester;

                for (auto& j : course)
                    j->semester -= (min-1);
    };

    // for those pure base course
    for (auto& i : baseCoursePtrVec){
        if(!i->study_type){
//            courseSchedule.push_back(std::make_shared<schedule>(i, 1));
            baseCourseSchedule.push_back(std::make_shared<schedule>(i, 1));
            i->study_type = true;
        }
    }
    courseSchedule.insert(courseSchedule.begin(), baseCourseSchedule.begin(), baseCourseSchedule.end());

    // for target course
    for (auto& thisTargetPtr : targetCoursePtrVec){
        // semester will re assigned in normal_sort_re
        auto thisTarget_schedulePtr = std::make_shared<schedule>(thisTargetPtr, 0);

        // target has target in pre
        // v2: Check if target has pre
//        if (!thisTargetPtr->pre.empty()){
        assert(thisTargetPtr->pre.size() != 0);
            // this target didn't studied
        if(!thisTargetPtr->study_type){
            auto a = std::shared_ptr<schedule>(nullptr);
            auto var = normal_sort_re(thisTargetPtr, a, courseSchedule, baseCourseSchedule);
            courseSchedule.insert(courseSchedule.end(), var.begin(), var.end());
            thisTargetPtr->study_type = true;
        }
//        }
        // when target has base and target, base will dealing in normal_sort_re

        // target has pure base in pre
        // In v2, target has pure base assigned in normal_sort_re
//        else{
//            // append this course if not studied
//            if (!thisTargetPtr->study_type){
//                thisTarget_schedulePtr->semester = 2;
//                courseSchedule.push_back(thisTarget_schedulePtr);
//                thisTargetPtr->study_type = true;
//            }
//        }
    }

    re_number(courseSchedule);
    return courseSchedule;
}

void defer_course(schedulePtr & i, std::array<float, 9>& total_point){
    i->semester ++;
    for (auto& j : i->postCourse)
        if (j && j->semester == i->semester)
            defer_course(j, total_point);
}

schedulePtrVecType& check_point(schedulePtrVecType & course_schedule, float max){
    /*
     * :param max: default as 17.5
     * */
    auto get_point =
            [&](const schedulePtr & i) -> float {
        return i->course->point;

    };

     std::array<float, 9> total_point{};
     total_point.fill(0);
    for (auto & iter : course_schedule){
        total_point[iter->semester] += get_point(iter);
        if (total_point[iter->semester] > max){

            total_point[iter->semester] -= get_point(iter);
            defer_course(iter, total_point);
            total_point[iter->semester] += get_point(iter);

        }
    }
    return course_schedule;
}

std::vector<plain_schedule> plain_schedule::changeTo(const schedulePtrVecType& course_schedule){
    /*
     * Change cxx class to string vector and number vector
     * for python part
     * */
    std::vector<plain_schedule> plain_course_schedule;

    auto get_info =
            [](const schedulePtr & i) -> plain_schedule{
                return plain_schedule{i->course->name, i->course->point, i->semester};
            };
    for (const auto& i : course_schedule)
        plain_course_schedule.push_back(get_info(i));
    return plain_course_schedule;
}
