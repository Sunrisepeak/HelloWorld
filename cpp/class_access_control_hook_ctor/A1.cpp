#include <iostream>

class A {

public:

    A() {
        config();
    }

    /**
     * 
     *   other op
     * 
     */

    int getSum() const {
        return __mA + __mB + __mC;
    }

private:
    int __mA, __mB;
    int __mC;

    void config() {
        __mA = __mB = __mC = 1;
    }
};

int main() {
    A a;
    std::cout << a.getSum() << std::endl;
    return 0;
}