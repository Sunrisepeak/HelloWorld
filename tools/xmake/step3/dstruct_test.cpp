#include <gtest/gtest.h>

#include <dstruct.hpp>

TEST(Vector, resize) {
    dstruct::Vector<int> vec;
    ASSERT_EQ(vec.size(), 0);
    vec.push_back(1);
    vec.resize(10, -1);
    ASSERT_EQ(vec.size(), 10);
    ASSERT_EQ(vec[0], 1);
    ASSERT_EQ(vec[1], -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}