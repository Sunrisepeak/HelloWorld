#include <iostream>

/*

g++ cpp/new_delete/delete_this.cpp && ./a.out

*/

struct Object {
    Object(int i) : data { i } { }
    ~Object() {
        std::cout << "~Object()" << std::endl;
        //delete this;
        this->~Object();
        // free(this)
    }
    int data;
};

int main() {
    Object obj(2);
    std::cout << obj.data << std::endl;
    return 0;
}