//
// Created by 史坤明 on 2020/10/11.
//

#ifndef C___PART_TARGET_COURSE_H
#define C___PART_TARGET_COURSE_H

#include <utility>
#include <vector>
#include <string>
//#include "course.h"

class course { //: public course {
public:
    std::string name;
    float point;
    std::vector<std::shared_ptr<course>> pre;
    bool study_type;

    explicit course(std::string s, float point, std::vector<std::shared_ptr<course>>& pre):
            name(std::move(s)), point(point), pre(pre), study_type(false) {}

    explicit course(std::string s, float point) : name(std::move(s)), point(point), pre(0), study_type(false) {}

    bool operator ==(const course& a){
        if (a.name == this->name)
            return true;
        else
            return false;
    }
};


#endif //C___PART_TARGET_COURSE_H
