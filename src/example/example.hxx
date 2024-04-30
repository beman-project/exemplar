// Copyright © 2024 Bret Brown
// SPDX-License-Identifier: MIT

#ifndef EXAMPLE_HXX
#define EXAMPLE_HXX

#include <type_traits>

template <class T>
constexpr bool foo() {
    static_assert(std::is_trivially_copyable_v<T>);
    return true;
}

#endif
