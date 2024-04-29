#include "mylib.h"

static int cnt = 1;

void mylib1_func() {
    HONLY_LOGD("cnt %d, addr %p", cnt, &cnt);
}