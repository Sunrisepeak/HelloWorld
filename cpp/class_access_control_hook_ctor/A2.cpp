#include <iostream>

class A {

public:
    using HFunc = void (*)(int &, int &);

public:

    A(HFunc hf = init) {
        config();
        hf(__mA, __mB);
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

    static void init(int &a, int &b) {
        a = 2;
        b = 2;
    }

};

int main() {
    A a1,  a2(
        [ ](int &a, int &b) {
            a = 2; // __mA
            b = 3; // __mB
        }
    );
    
    std::cout << a1.getSum() << std::endl; // 1 + 2 + 2
    std::cout << a2.getSum() << std::endl; // 1 + 2 + 3

    return 0;
}