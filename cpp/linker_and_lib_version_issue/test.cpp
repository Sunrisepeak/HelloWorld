#include "mylib-v1/mylib.h" // use mylib v1
#include "mylib-v1/mylib.hpp" // use mylib v1 - header only

void test() {
    send(1000);
    MyLib().write(1000);
    MyLib().write();
}