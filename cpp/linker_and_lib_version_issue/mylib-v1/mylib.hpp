#ifndef __MY_LIB__HPP__
#define __MY_LIB__HPP__

#include <iostream>
#include <cassert>

struct MyLib {
    void write(int val);

    void write() {
        std::cout << "Header-Only: version 1 ****" << std::endl;
    }
};

inline void MyLib::write(int val) {
    std::cout << "Header-Only: version 1: " << val << std::endl;
    assert(val < 10000);
}

#endif