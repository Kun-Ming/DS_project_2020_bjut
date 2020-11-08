#include <iostream>
//#include "course/course.h"
#include "course/target_course.h"
#include "sort/normal_sort.h"
#include "sort/generate.h"
#include "binding/py_c_interface.h"
#include <algorithm>

int main() {

    courseNameVecType target = {"线性代数", "编译原理", "模电", "数电", "汇编", "java", "计组", "数据结构"};
    preNameVecType pre = {std::vector<std::string>{"高等数学"},
                          std::vector<std::string>{"计组", "汇编"},
                          std::vector<std::string>{"高等数学"},
                          std::vector<std::string>{"C"},
                          std::vector<std::string>{"C"},
                          std::vector<std::string>{"C"},
                          std::vector<std::string>{"数电", "模电"},
                          std::vector<std::string>{"java"}
    };
    std::swap(target[0], target[6]);
    std::swap(pre[0], pre[6]);
    coursePointVecType target_point = {2, 3, 2, 2, 2.5, 3, 3.5, 4};
    courseNameVecType base = {"高等数学", "C", "金工实习"};
    coursePointVecType base_point = {5, 2.5, 2};

    auto res = normal_sort_cxx(target, pre, target_point, base, base_point);
//    for (auto i : res){
//        std::cout<<i.courseName<<"  "<<i.semester<<"  "<<i.point<<std::endl;
//    }


    return 0;
}
