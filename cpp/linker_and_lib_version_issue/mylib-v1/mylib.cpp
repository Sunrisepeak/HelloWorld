#include <iostream>
#include <cassert>

#include "mylib.h"

void send(int val) {
    std::cout << "version 1: " << val << std::endl;
    assert(val < 10000);
}