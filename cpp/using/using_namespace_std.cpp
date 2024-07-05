#include <iostream>
#include <vector>

/*
    g++ cpp/using/using_namespace_std.cpp && ./a.out
*/

void print_vector(std::vector<int> &vec) {
    using namespace std;
    cout << "[ ";
    for (int val : vec) {
        cout << val << " ";
    }
    cout << "]" << endl;
}

using namespace std;

int main() {
    cout << "hello namespace" << endl;
    std::cout << "hello namespace" << std::endl;

    vector<int> vec = {2, 2, 3, 3};
    print_vector(vec);

    return 0;
}