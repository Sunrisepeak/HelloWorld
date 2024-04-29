#include <cstdio>

int count() {
    static int cnt = 0;
    return ++cnt;
}

int main() {
    printf("count: %d\n", count());
    printf("count: %d\n", count());
    return 0;
}