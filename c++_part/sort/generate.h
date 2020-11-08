//
// Created by 史坤明 on 2020/10/11.
//

#ifndef C___PART_GENERATE_H
#define C___PART_GENERATE_H

#include <vector>
#include "../course/target_course.h"
using courseNameVecType =  std::vector<std::string>;
using coursePointVecType = std::vector<float>;
using preNameVecType = std::vector<std::vector<std::string>> ;
using coursePtr = std::shared_ptr<course> ;


std::vector<coursePtr> generateDAG(courseNameVecType& target,
                                         coursePointVecType& target_point,
                                         courseNameVecType& base,
                                         coursePointVecType& base_point,
                                         preNameVecType& pre,
                                         std::vector<coursePtr>& all_base_course);
coursePtr generate_target(courseNameVecType& target,
                                coursePointVecType& target_point,
                                preNameVecType& pre,
                                std::string target_this,
                                float target_point_this,
                                std::vector<std::string> pre_this,
                                std::vector<coursePtr>& all_base_course,
                                std::vector<coursePtr>& all_target_course,
                                const int& index);




#endif //C___PART_GENERATE_H
