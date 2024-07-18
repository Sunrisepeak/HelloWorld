#include <iostream>
#include <vector>

/*

g++ cpp/new_delete/new_delete_expression_1.cpp && ./a.out

replaceable - operator new - (std::size_t)
replaceable - operator new - (std::size_t, align)
replaceable - operator new - (std::size_t, nothrow)
replaceable - operator new - (std::size_t, align, nothrow)

placement - operator new (std::size_t, void *) - std

placement - operator new - (std::size_t, ...)
placement - operator new (std::size_t, align, ...)

replaceable? - exist c++ std define

*/

struct Object {
    Object(int i) : data { i } {
        std::cout << "Object(int i)" << std::endl;
    }
    ~Object() {
        std::cout << "~Object()" << std::endl;
    }

    static void * operator new(std::size_t sz) noexcept {
        void *ptr = malloc(sz);
        printf("Object: new: %ld byte, addr %p\n", sz, ptr);
        return ptr;
    }

    // C++ std-noexcept version - operator new - global is std, is it std in class ?
    static void * operator new(std::size_t sz, const std::nothrow_t&) noexcept {
        void *ptr = malloc(sz);
        printf("Object-std-noexcept: new: %ld byte, addr %p\n", sz, ptr);
        return ptr;
    }

    // C++ custom-noexcept version - operator new
    static void * operator new(std::size_t sz, const bool&) noexcept {
        void *ptr = malloc(sz);
        printf("Object-custom-noexcept: new: %ld byte, addr %p\n", sz, ptr);
        return ptr;
    }

    static void operator delete(void *ptr) noexcept {
        printf("Object: delete: addr %p\n", ptr);
        free(ptr);
    }

    // placement-new dont need operator delete

    int data;
};

void * operator new(std::size_t sz) noexcept {
    void *ptr = malloc(sz);
    printf("new: %ld byte, addr %p\n", sz, ptr);
    return ptr;
}

void operator delete(void *ptr) noexcept {
    printf("delete: addr %p\n", ptr);
    free(ptr);
}

int main() {

    auto p = new int;
    delete p;

    Object *objPtr = new Object(2);
    std::cout << objPtr << " - " << objPtr->data << std::endl;
    delete objPtr;

    Object *objPtr2 = new (std::nothrow) Object(2);
    delete objPtr2;

    Object *objPtr3 = new (true) Object(2);
    delete objPtr3;

    return 0;
}