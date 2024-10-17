add_rules("mode.debug", "mode.release")

-- 1.don't use system's opencv
--- add_requires("opencv 4.6", {system = false})


-- 2.if you want to use system's opencv, need install opencv-dev
--     sudo apt-get install libopencv-dev
add_requires("opencv")

target("opencv_demo")
    set_kind("binary")
    add_files("main.cpp")
    add_packages("opencv")