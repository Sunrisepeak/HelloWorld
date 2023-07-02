#include <iostream>

template <typename T>
struct Functor1 {
	void operator()(T t) {
    	std::cout << "functor1 template: " << t << std::endl;
	}
};

template <typename T1, typename T2>
struct Functor2 {
	void operator()(T1 t1, T2 t2) {
    	std::cout << "functor2 template: " << std::min(t1, t2) << std::endl;
	}
};

template<typename T, typename... Args>
struct Functor3 {
    auto /*need cpp14*/ operator()(T t, Args&&... args) /* c11 -> returnType*/ {
        auto s = t + sum(std::forward<Args>(args)...);
        std::cout << "functor3 template: " << s << std::endl;
        return s;
    }

private:
    template <typename _T, typename... _Args>
    auto sum(_T t, _Args&&... _args) {
        return t + sum(std::forward<_Args>(_args)...);
    }

    template <typename _T>
    auto sum(_T t) {
        return t;
    }
};

template <template <typename...> class FT, typename... Args>
void test(Args&&... args) {
    // do something...
    FT<Args...>()(std::forward<Args>(args)...);
    // do something...
}

int main() {
    test<Functor1>(11);
    test<Functor2>(10, 11);
    test<Functor3>(2, 1, 4, 2.3, -1, -0.1, '0');
    return 0;
}