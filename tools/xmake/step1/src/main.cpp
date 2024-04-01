#include <iostream>

bool test() {
    int *ptr = nullptr;
    *ptr = 0; // test
    return true;
}

int main() {
    std::cout << "Hello xmake!" << std::endl;
    test();
    return 0;
}