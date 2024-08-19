// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <Beman/Example/example.hpp>

#include <gtest/gtest.h>

TEST(ExampleTest, call_identity) {
    for (int i = -100; i < 100; ++i) {
        EXPECT_EQ(i, beman::example::identity()(i));
    }
}

// Test comparing beman::example::identity with std::identity.
// Requires std::identity support.
#if defined(__cpp_lib_identity)
#include <functional>

TEST(ExampleTest, compare_identity_std_vs_beman) {
    std::identity std_id;
    bemane::example::identity beman_id;
    for (int i = -100; i < 100; ++i) {
        EXPECT_EQ(std_id(i), beman_id(i));
    }
}
#endif

// Test checking if beman::example::identity is transparent.
// Requires transparent operators support.
#if defined(__cpp_lib_transparent_operators)
#include <algorithm>

TEST(ExampleTest, is_transparent) {
    beman::example::identity id;

    const auto container = {1, 2, 3, 4, 5};
    auto it = std::find(std::begin(container), std::end(container), 3);
    EXPECT_EQ(3, *it);
    auto it_with_id = std::find(std::begin(container), std::end(container), id(3));
    EXPECT_EQ(3, *it_with_id);

    EXPECT_EQ(it, it_with_id);
}
#endif
