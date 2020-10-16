#include <utility>
#include <string>

#ifndef C___PART_COURSE_H
#define C___PART_COURSE_H


class course {
public:
    std::string name;
    float point;
    bool study_type;

    course() = default;

    course(std::string s, const float t) :
            name(std::move(s)), point(t), study_type(false) {}

    explicit course(std::string s) :
            name(std::move(s)), study_type(false) {}

    explicit course(const float &t) :
            point(t), study_type(false) {}

    float get_point() const {return point;}

    bool operator ==(const course& a){
        if (a.name == this->name)
            return true;
        else
            return false;
    }

    std::string get_name() {return name;}


};


#endif //C___PART_COURSE_H
