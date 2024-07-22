#include <iostream>
#include <new>

/*

g++ cpp/new_delete/new_delete_2.cpp && ./a.out

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

void * operator new(std::size_t size) {
    std::cout << "Custom operator new called, size: " << size << std::endl;
    // 1. get handler
    std::new_handler currentHandler = std::get_new_handler();
    void* ptr = nullptr;
    int retry = 3;
    while (retry) {
        // 2. malloc
        ptr = std::malloc(size);

        // 3. check ptr
        if (ptr) {
            return ptr;
        }

        // 4. call handler
        if (!currentHandler) {
            break;
        }
        currentHandler();
        printf("new: retry(%d) to alloc...\n", retry);
        retry--;
    }
    throw std::bad_alloc();
    // return nullptr; x
}

void operator delete(void *ptr) noexcept {
    printf("delete: addr %p\n", ptr);
    free(ptr);
}

void * operator new[](std::size_t size) {
    void *ptr = malloc(size);
    printf("new[]: size %ld, addr %p\n", size, ptr);
    return ptr;
}

void operator delete[](void *ptr) noexcept {
    printf("delete[]: addr %p\n", ptr);
    free(ptr);
}

int main() {

    std::set_new_handler([] { std::cout << "do something..." << std::endl; });

    try {
        Object *objPtr = new Object(2);
        // 1.ptr = malloc(xx)
        // 2.ptr->T()
        std::cout << objPtr << " - " << objPtr->data << std::endl;
        delete objPtr;
        // 3.ptr->~T()
        // 4.free(ptr)

        auto arrPtr = new int[3];
        delete[] arrPtr;
    } catch (std::bad_alloc &e) {
        std::cout << e.what() << std::endl;
    }

    std::cout << "end..." << std::endl;

    return 0;
}