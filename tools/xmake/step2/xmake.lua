add_includedirs("include")

target("xlib-static")
    set_kind("static")
    add_files("src/*.cpp")

target("xlib-shared")
    set_kind("shared")
    add_files("src/*.cpp")

target("test")
    set_kind("binary")
    add_files("tests/test.cpp")
    add_deps("xlib-shared")