void test(int *ptr) {

	*ptr = 6;

}

int main() {
	int *ptr = nullptr;
    // 不小心, 还是故意的?
	test(ptr);
    return 0;
}
