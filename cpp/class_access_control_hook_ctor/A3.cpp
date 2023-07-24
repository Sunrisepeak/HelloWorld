#include <iostream>

class A {

public:

    struct AHook {
        // member data: private -> public
        int a;
        int b;
        
        A * const objPtr;

        AHook(A *aptr) : a { 0 }, b { 0 }, objPtr { aptr } { }

        // member function : private -> public 
        void init(AHook &data) { // A::init --> AHook::init
            objPtr->init(data);
        }

        /*
        void setC(int c) {
            objPtr->__mC = c;
        }
        */
    };

    using HFunc = void (*)(AHook &);

public:

    A(HFunc hf = init) : __mHData { this } {
        config();
        hf(__mHData);
    }

    /**
     * 
     *   other op
     * 
     */

    int getSum() const {
        return __mHData.a + __mHData.b + __mC;
    }

private:
    AHook __mHData;
    int __mC;

    void config() {
        __mHData.a = __mHData.b = __mC = 1;
    }

    static void init(AHook &hdata) {
        hdata.a = 2;
        hdata.b = 2;
    }

};

int main() {
    
    A::HFunc myInit = [](A::AHook &ah) {
        // access A's private function
        ah.init(ah);
        // acces A's public function
        std::cout << "my init: " << ah.objPtr->getSum() << std::endl;
        
        // access private hook data
        ah.a = 2;
        ah.b = 3;

        // access private data
        // ah.setC(5);
    };

    A a1, a2(myInit);
    
    std::cout << a1.getSum() << std::endl; // 1 + 2 + 2
    std::cout << a2.getSum() << std::endl; // 1 + 2 + 3

    return 0;
}