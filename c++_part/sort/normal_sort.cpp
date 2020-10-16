//
// Created by 史坤明 on 2020/10/11.
//

#include <array>
#include "normal_sort.h"
size_t semester = 8;

schedulePtrVecType normal_sort_re(targetCoursePtr target_this,
                                  schedulePtr targetPostPtr,
                                  schedulePtrVecType all_courseSchedule){
    schedulePtrVecType courseSchedule;
    auto thisTarget_SchedulePtr = std::make_shared<schedule>(target_this,
                                                             nullptr,
                                                             0,
                                                             targetPostPtr);


    // if target has target in pre
    if (!target_this->pre.empty()){
        for (auto& i : target_this->pre){
            if (!i->study_type){

                // find target in pre
                auto var = normal_sort_re(i, thisTarget_SchedulePtr, all_courseSchedule);

                // insert target in pre
                courseSchedule.insert(courseSchedule.end(), var.begin(), var.end());

                thisTarget_SchedulePtr->semester = var.back()->semester + 1 > thisTarget_SchedulePtr->semester?
                                                   var.back()->semester + 1: thisTarget_SchedulePtr->semester;

                i->study_type = true;
            }
        }
//        schedule_base();
        courseSchedule.push_back(thisTarget_SchedulePtr);
    }
    // target only has base in pre
    else{
            thisTarget_SchedulePtr->semester = 2;
            courseSchedule.push_back(thisTarget_SchedulePtr);
        }
//    size_t max_semester_in_pre = findTargetInAll_func(target_this);
//    thisTarget_SchedulePtr->semester = max_semester_in_pre + 1;
    return courseSchedule;
}

schedulePtrVecType normal_sort(std::vector<targetCoursePtr>& targetCoursePtrVec, std::vector<coursePtr>& baseCoursePtrVec){
    schedulePtrVecType courseSchedule;

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
            courseSchedule.push_back(std::make_shared<schedule>(nullptr, i, 1, nullptr));
            i->study_type = true;
        }
    }

    // for target course
    for (auto& thisTargetPtr : targetCoursePtrVec){
        // semester will re assigned in normal_sort_re
        auto thisTarget_schedulePtr = std::make_shared<schedule>(thisTargetPtr, nullptr, 0, nullptr);

        // target has target in pre
        if (!thisTargetPtr->pre.empty()){

            // this target didn't studied
            if(!thisTargetPtr->study_type){
                auto var = normal_sort_re(thisTargetPtr, nullptr, courseSchedule); // 应在normal_sort_re中处理
                courseSchedule.insert(courseSchedule.end(), var.begin(), var.end());
                thisTargetPtr->study_type = true;
            }
        }
        // when target has base and target, base will dealing in normal_sort_re
        // target has pure base in pre
        else{
            // append this course if not studied
            if (!thisTargetPtr->study_type){
                thisTarget_schedulePtr->semester = 2;
                courseSchedule.push_back(thisTarget_schedulePtr);
                thisTargetPtr->study_type = true;
            }

        }
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
    auto get_point =
            [&](const schedulePtr & i) -> float {
        return i->baseCourse? i->baseCourse->point : i->targetCourse->point;

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
    std::vector<plain_schedule> plain_course_schedule;

    auto get_info =
            [](const schedulePtr & i) -> plain_schedule{
                return plain_schedule{i->baseCourse? i->baseCourse->name : i->targetCourse->name,
                                      i->baseCourse? i->baseCourse->point : i->targetCourse->point,
                                      i->semester};
            };
    for (const auto& i : course_schedule)
        plain_course_schedule.push_back(get_info(i));
    return plain_course_schedule;
}
