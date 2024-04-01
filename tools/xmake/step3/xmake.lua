add_requires("gtest v1.11.0")

package("dstruct")
    set_urls("git@github.com:Sunrisepeak/dstruct.git")

    add_includedirs(".")

    on_install(function (package)
        os.mv("*", package:installdir("."))
    end)
package_end()

add_requires("dstruct")

target("test")
    set_kind("binary")
    add_packages("gtest", "dstruct")
    add_files("dstruct_test.cpp")