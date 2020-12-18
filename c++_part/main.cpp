#include <iostream>
//#include "course/course.h"
#include "course/target_course.h"
#include "sort/normal_sort.h"
#include "sort/generate.h"
#include "binding/py_c_interface.h"
#include <algorithm>

int main() {

    courseNameVecType target = {"线性代数", "模电", "计组", "数电", "java", "汇编", "数据结构", "数据库原理", "编译原理", "操作系统"};
    preNameVecType pre = {std::vector<std::string>{"高等数学"},
                          std::vector<std::string>{"高等数学"},
                          std::vector<std::string>{"模电", "数电"},
                          std::vector<std::string>{"C"},
                          std::vector<std::string>{"C"},
                          std::vector<std::string>{"C"},
                          std::vector<std::string>{"java"},
                          std::vector<std::string>{"离散数学"},
                          std::vector<std::string>{"计组", "汇编"},
                          std::vector<std::string>{"计组"}
    };
    coursePointVecType target_point = {2, 3, 2, 2, 2.5, 3, 3.5, 4, 2, 2};
    courseNameVecType base = {"高等数学", "C", "离散数学"};
    coursePointVecType base_point = {5, 2.5, 2};

    auto res = normal_sort_cxx(target, pre, target_point, base, base_point);
    for (auto i : res){
        std::cout<<i.first<<"  "<<i.second<<std::endl;
    }
//    auto res2 = normal_sort_schedule_cxx(target, pre, target_point, base, base_point);
//    auto res3 = pre2post_cxx(target, pre, target_point, base, base_point);


    return 0;
}
