//
// Created by 史坤明 on 2020/10/11.
//

#ifndef C___PART_GENERATE_H
#define C___PART_GENERATE_H

#include <vector>
#include "../course/target_course.h"
using courseVecType =  std::vector<std::string>;
using coursePointVecType = std::vector<float>;
using preVecType = std::vector<std::vector<std::string>> ;
using targetCoursePtr = std::shared_ptr<target_course> ;
using coursePtr = std::shared_ptr<course> ;


std::vector<targetCoursePtr> generateDAG(courseVecType& target,
                                         coursePointVecType& target_point,
                                         courseVecType& base,
                                         coursePointVecType& base_point,
                                         preVecType& pre,
                                         std::vector<coursePtr>& all_base_course);
targetCoursePtr generate_target(courseVecType& target,
                                coursePointVecType& target_point,
                                preVecType& pre,
                                std::string target_this,
                                float target_point_this,
                                std::vector<std::string> pre_this,
                                std::vector<coursePtr>& all_base_course,
                                std::vector<targetCoursePtr>& all_target_course,
                                const int& index);




#endif //C___PART_GENERATE_H
