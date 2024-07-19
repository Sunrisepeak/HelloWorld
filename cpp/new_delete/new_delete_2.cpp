#include <iostream>
#include <new>

/*

g++ cpp/new_delete/new_delete_2.cpp && ./a.out

*/

struct T { int t[10000000]; };

struct Object {
    Object(int i) : data { i } {
        std::cout << "Object(int i)" << std::endl;
    }
    ~Object() {
        std::cout << "~Object()" << std::endl;
    }
    int data;
    T t[1000000];
};

void * operator new(std::size_t size) {
    auto handler = std::get_new_handler();
    void *ptr;
    while (true) {
        // 1. malloc
        ptr = malloc(size);

        // 2. ptr ? nullptr
        if (ptr) {
            break;
        }
    
        // 3. ptr is nullptr - std::handler...
        if (handler) {
            handler();
        } else {
            // 4. bad_alloc
            throw std::bad_alloc();
        }
    }
    printf("allocate bytes %ld, addr %p\n", size, ptr);
    return ptr;
}

void operator delete(void *ptr) noexcept {
    printf("free addr %p\n", ptr);
    if (ptr) {
        free(ptr);
    }
}

int main() {

    std::set_new_handler([] {
        static int i = 1;
        if (i == 0) {
            throw std::bad_alloc();
        }
        i--;
        std::cout << "new_handler" << std::endl; 
    });

    try {
        Object *objPtr = new Object(2);
        // 1.ptr = malloc(xx)
        // 2.ptr->T()
        std::cout << objPtr << " - " << objPtr->data << std::endl;
        delete objPtr;
        // 3.ptr->~T()
        // 4.free(ptr)
    } catch(const std::bad_alloc &e) {
        std::cerr << e.what() << std::endl;
    }
    
    printf(".....end\n");
    return 0;
}