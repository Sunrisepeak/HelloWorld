#include <iostream>
#include <new>

/*

g++ cpp/new_delete/new_delete_4.cpp && ./a.out

*/

struct Object {
    Object(int i) : data { i } {
        std::cout << "Object(int i)" << std::endl;
    }
    ~Object() {
        std::cout << "~Object()" << std::endl;
    }
    int data;
};

struct CustomNewFlag { };

inline void * operator new(std::size_t sz, void *ptr, CustomNewFlag) {
    return ptr; // only call contructor
}

int main() {
    // Object *objPtr = new Object(2);
    void *ptr = malloc(sizeof(Object));
    new (ptr, CustomNewFlag()) Object(2);
    auto objPtr = reinterpret_cast<Object *>(ptr);

    std::cout << objPtr->data << std::endl;

    // delete objPtr;
    objPtr->~Object();
    free(objPtr);
    objPtr = nullptr;

    return 0;
}