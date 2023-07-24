#include <iostream>

#include "helloaosp_api.h" // lib api

int main() {

    int a = 1, b = 2;
    
    std::cout << "Hello AOSP: " << a << " " << b << std::endl;
    std::cout << "max: " << max(a, b) << std::endl;
    
    return 0;
}
