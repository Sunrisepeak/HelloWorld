#define LOG_TAG "add"

#include <log/log.h>

#include "helloaosp.h"

int add(int a, int b) {
	int c = a + b;
	ALOGD("return %d", c);
	return c;
}