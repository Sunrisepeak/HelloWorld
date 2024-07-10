#include <iostream>

// g++ d2ds/array/1.Array.cpp && ./a.out

template <typename T, unsigned int N>
struct Array {
    T & operator[](int index) {
        if (index < 0) {
            index += N;
        }
        return arr[index];
    }
    T arr[N];
};

int main() {
    int arr[10];
    Array <int, 10> myArr;
    arr[8] = myArr[8] = 8;
    std::cout << arr[8] << " - " << arr[-2] << std::endl;
    std::cout << myArr[8] << " - " << myArr[-2] << std::endl;
    return 0;
}