#include <iostream>

#include "xlib.h"

int main() {
    print_lib_info();

    int sum = add(100, 200);
    std::cout << "sum: " << sum << std::endl;

    return 0;
}