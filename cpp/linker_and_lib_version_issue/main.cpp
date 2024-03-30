
#include "test.h"
#include "mylib-v2/mylib.h" // use mylib v2
#include "mylib-v2/mylib.hpp" // use mylib v2 - Header Only

int main() {
    test();

    MyLib().write(20000); // mylib v2 Header Only

    // expect to use v2 version, but it will call v1 version
    // g++ -o main main.cpp $LIBS_DIR -ltest -lmylib.v2
    // libtest: test.o mylib.o(mylib.v1)
    send(20000);
}