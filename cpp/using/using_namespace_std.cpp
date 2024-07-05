#include <iostream>
#include <vector>

void process(std::vector<int> data) {
    using namespace std;
    for (auto &val : data) {
        val *= 2;
    }
    cout << "[ ";
    for (auto &val : data) {
        cout << val << " ";
    }
    cout << "]" << endl;
}

namespace n1 {
namespace n2 {
namespace n3 {
    struct vector {

    };
}
}
}

template <typename T>
struct vector {

};

int main() {
    vector<int> myVec;
    {
        using namespace std;
        std::vector<int> vec {1, 2, 2, 3};
        cout << "Hello World - " << vec[0] << endl;
        process(vec);
    }
    vector<int> myVec2;
    using namespace n1::n2;
    n3::vector nVector;
    return 0;
}