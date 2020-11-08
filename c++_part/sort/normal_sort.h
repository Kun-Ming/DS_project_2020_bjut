//
// Created by 史坤明 on 2020/10/11.
//

#ifndef C___PART_NORMAL_SORT_H
#define C___PART_NORMAL_SORT_H

#include <utility>

#include "generate.h"

struct schedule{
    coursePtr course;
    std::size_t semester;
    std::vector<std::shared_ptr<schedule>> postCourse;

    explicit schedule(coursePtr& a, size_t c, std::shared_ptr<schedule>& d) :
    // Parameter a can be target course or base course
    course(a), semester(c) {
        if(d)
            postCourse.push_back(d);
    }

    explicit schedule(coursePtr& a, size_t b) :
    course(a), semester(b) {}
};
using schedulePtr = std::shared_ptr<schedule>;
using scheduleVecType = std::vector<schedule>;
using schedulePtrVecType = std::vector<schedulePtr>;

struct plain_schedule{
    std::string courseName;
    float point;
    size_t semester;

    plain_schedule() = default;
    plain_schedule(std::string a,float b, size_t c) :
    courseName(std::move(a)), point(b), semester(c) {}

    std::vector<plain_schedule> changeTo(const schedulePtrVecType& course_schedule);
};
using plainScheduleVecType = std::vector<plain_schedule>;



schedulePtrVecType normal_sort(std::vector<coursePtr>& targetCoursePtrVec, std::vector<coursePtr>& baseCoursePtrVec);
schedulePtrVecType& check_point(schedulePtrVecType& course_schedule, float max = 17.5);
schedulePtrVecType normal_sort_re(coursePtr& target_this,
                                  schedulePtr& targetPostPtr,
                                  schedulePtrVecType& all_courseSchedule,
                                  schedulePtrVecType& baseCourseSchedule);

#endif //C___PART_NORMAL_SORT_H
