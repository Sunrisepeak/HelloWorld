#include <iostream>
#include <new>

/*

g++ cpp/new_delete/new_delete_3.cpp && ./a.out

*/

// alignas(x)
struct Object {
    char data;
};

int main() {
    Object *ptr = new Object;
    //Object *ptr = new (std::nothrow) Object;

    if (ptr != nullptr) {
        ptr->data = 1;
        delete ptr;
    }

    return 0;
}