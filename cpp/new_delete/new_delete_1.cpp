#include <iostream>

/*

g++ cpp/new_delete/new_delete_1.cpp && ./a.out

*/

struct Object {
    Object(int i) : data { i } {
        std::cout << "Object(int i)" << std::endl;
    }
    ~Object() {
        std::cout << "~Object()" << std::endl;
    }
    int data;

    static void * operator new(std::size_t size) {
        void *ptr = malloc(size);
        printf("allocate bytes %ld, addr %p\n", size, ptr);
        return ptr;
    }

    static void operator delete(void *ptr) {
        printf("free addr %p\n", ptr);
        free(ptr);
    }

};


int main() {

    Object *objPtr = new Object(2);
    // 1.ptr = malloc(xx)
    // 2.ptr->T()
    std::cout << objPtr << " - " << objPtr->data << std::endl;
    delete objPtr;
    // 3.ptr->~T()
    // 4.free(ptr)

    auto p = new int;
    delete p;

    return 0;
}