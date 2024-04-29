#ifndef MYLIB_H
#define MYLIB_H

#include <cstdio>

#define HONLY_LOGD(...) { fprintf (stdout, "[LOGD]: \t%s: %s:%d - ", __func__, __FILE__, __LINE__); fprintf(stdout, __VA_ARGS__); printf("\n"); }

static void * mylib() {
    static int cnt = 0;
    return &cnt;
}

void mylib1_func();
void mylib2_func();

#endif