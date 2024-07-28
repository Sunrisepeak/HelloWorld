#include <iostream>

// g++ d2ds/array/2.Array.cpp && ./a.out

template <typename T, unsigned int N>
struct Array {
public:
    Array(std::initializer_list<T> list) {
        int i = 0;
        for (auto it = list.begin(); i < N && it != list.end(); it++) {
            arr[i] = *it;
            i++;
        }
        while (i < N) {
            arr[i] = T();
            i++;
        }
    }
public:
    T & operator[](int index) {
        if (index < 0) {
            index += N;
        }
        return arr[index];
    }
private:
    T arr[N];
};

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    Array<int, 5> myArr = {1, 2, 3};
    std::cout << arr[0] << " - " << myArr[0] << std::endl;
    std::cout << arr[3] << " - " << myArr[-2] << std::endl;
    return 0;
}