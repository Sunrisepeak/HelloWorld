#ifndef __MY_LIB__HPP__
#define __MY_LIB__HPP__

#include <iostream>

struct MyLib {
    void write(int val);
};

inline void MyLib::write(int val) {
    std::cout << "Header-Only: version 2: " << val << std::endl;
}

#endif