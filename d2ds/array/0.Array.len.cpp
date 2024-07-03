#include <iostream>

/*
    g++ d2ds/array/0.Array.len.cpp && ./a.out
*/

template <typename T>
void process(T arr) {
    printf("process: len %ld, arr[0] = %d\n", sizeof(arr), arr[0]);
}

template <typename T, unsigned int N>
struct Array {

    T & operator[](int index) {
        return data[index];
    }

    T data[N];
};

int main() {
    int arr[3];
    Array<int, 3> myArr;
    arr[0] = myArr[0] = 2233;
    printf("len %ld - arr[0] = %d\n", sizeof(arr), arr[0]);
    process(arr);
    printf("len %ld - arr[0] = %d\n", sizeof(myArr), myArr[0]);
    process(myArr);
    return 0;
}