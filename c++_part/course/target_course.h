//
// Created by 史坤明 on 2020/10/11.
//

#ifndef C___PART_TARGET_COURSE_H
#define C___PART_TARGET_COURSE_H

#include <utility>
#include <vector>
#include "course.h"

class target_course : course {
public:
    std::string name;
    float point;
    std::vector<std::shared_ptr<target_course>> pre;
    std::vector<std::shared_ptr<course>> pre_base;
    bool study_type;

    target_course(std::string s, float point, std::vector<std::shared_ptr<target_course>>& pre,
                  std::vector<std::shared_ptr<course>>& pre_base):
            name(std::move(s)), point(point), pre(pre), pre_base(pre_base), study_type(false) {}

    explicit target_course(std::string s, float point) : name(std::move(s)), point(point), study_type(false) {}

    bool operator ==(const target_course& a){
        if (a.name == this->name)
            return true;
        else
            return false;
    }
};


#endif //C___PART_TARGET_COURSE_H
