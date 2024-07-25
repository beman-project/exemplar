// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#ifndef BEMAN_EXAMPLE_EXAMPLE_HPP
#define BEMAN_EXAMPLE_EXAMPLE_HPP

// C++ Standard Library: std::identity equivalent.
// Check https://eel.is/c++draft/func.identity:
//
// 22.10.12 Class identity  [func.identity]
//
// struct identity {
//   template<class T>
//     constexpr T&& operator()(T&& t) const noexcept;
//
//   using is_transparent = unspecified;
// };
//
// template<class T>
//   constexpr T&& operator()(T&& t) const noexcept;
//
// Effects: Equivalent to: return std::forward<T>(t);
//

#include <utility> // std::forward

namespace beman
{
namespace example
{

struct __is_transparent; // not defined

// Class identity  [func.identity]
// The class identity is a function object that takes a single argument and returns that argument unchanged.
// C++ standard compatibility: C++11 and later.
struct identity
{
    // operator() returns its argument unchanged.
    template <class T>
#if defined(__cpp_constexpr)
    constexpr
#endif
        T &&
        operator()(T &&t) const noexcept
    {
        return std::forward<T>(t);
    }

    // is_transparent is a nested type alias that is used to specify that a type is transparent.
    using is_transparent = __is_transparent;
};

} // namespace example
} // namespace beman

#endif // BEMAN_EXAMPLE_EXAMPLE_HPP
