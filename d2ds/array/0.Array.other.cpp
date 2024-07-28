#include <iostream>

// g++ d2ds/array/1.Array.cpp && ./a.out

struct IndexSafe {
    IndexSafe(int i) : index{i} { handler = nullptr; }
    using ErrHandler = int (*)(const char *);
    IndexSafe & err(ErrHandler handler) {
        this->handler = handler;
        return *this;
    }
    void throw_err(const char *errMsg) {
        if (handler) {
            index = handler(errMsg);
        } else {
            std::cout << "IndexSafe: " << errMsg << std::endl;
            index = 0;
        }
    }
    int index;
    ErrHandler handler;
};

template <typename T, unsigned int N>
struct Array {
    T & operator[](IndexSafe index) {
        if (index.index < 0) {
            index.index += N;
        }
        if (index.index < 0 || index.index >= N) {
            index.throw_err("out of range...");
        } 
        return arr[index.index];
    }
    T arr[N];
};

int main() {
    int arr[10];
    Array <int, 10> myArr;
    myArr[10] = 0;
    myArr[IndexSafe(10).err(
        [](auto e){
            printf("xxx: %s, return 9\n", e);
            return 9;
        }
    )] = 2233;
    std::cout << myArr[9] << std::endl;
    return 0;
}