#include <cstdio>

int count() {
    static int cnt = 0;
    return ++cnt;
}

struct A {
    A(const char *str) {
        printf("A: %s\n", str);
    }
};

A & create_a1() {
    static A a1("a1");
    return a1;
}

A & create_a2() {
    static A a2("a2");
    return a2;
}

void init_flow_control() {
    create_a2();
    create_a1();
}

int main() {

    printf("count: %d\n", count());
    printf("count: %d\n", count());

    return 0;
}