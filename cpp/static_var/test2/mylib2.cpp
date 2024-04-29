#include "mylib.h"

static int cnt = 2;

void mylib2_func() {
    HONLY_LOGD("cnt %d, addr %p", cnt, &cnt);
}