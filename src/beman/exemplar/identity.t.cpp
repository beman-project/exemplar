// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/exemplar/identity.hpp>

#include <gtest/gtest.h>

#include <algorithm>
#include <functional>

namespace exe = beman::exemplar;

TEST(IdentityTest, call_identity_with_int) {
    for (int i = -100; i < 100; ++i) {
        EXPECT_EQ(i, exe::identity()(i));
    }
}

TEST(IdentityTest, call_identity_with_custom_type) {
    struct S {
        int i;
    };

    for (int i = -100; i < 100; ++i) {
        const S s{i};
        const S s_id = exe::identity()(s);
        EXPECT_EQ(s.i, s_id.i);
    }
}

TEST(IdentityTest, compare_std_vs_beman) {
// Requires: std::identity support.
#if defined(__cpp_lib_identity)
    std::identity std_id;
    exe::identity beman_id;
    for (int i = -100; i < 100; ++i) {
        EXPECT_EQ(std_id(i), beman_id(i));
    }
#endif
}

TEST(IdentityTest, check_is_transparent) {
// Requires: transparent operators support.
#if defined(__cpp_lib_transparent_operators)

    exe::identity id;

    const auto container = {1, 2, 3, 4, 5};
    auto       it        = std::find(std::begin(container), std::end(container), 3);
    EXPECT_EQ(3, *it);
    auto it_with_id = std::find(std::begin(container), std::end(container), id(3));
    EXPECT_EQ(3, *it_with_id);

    EXPECT_EQ(it, it_with_id);
#endif
}
