target("test1")
    add_files("test1/main.cpp")

target("test2")
    add_includedirs("test2")
    add_files("test2/*.cpp")

target("test3")
    add_includedirs("test3")
    add_files("test3/*.cpp")

target("test4")
    add_includedirs("test4")
    add_files("test4/*.cpp")

target("test5")
    add_includedirs("test5")
    add_files("test5/*.cpp")