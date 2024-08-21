// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#ifndef BEMAN_EXAMPLE_IDENTITY_HPP
#define BEMAN_EXAMPLE_IDENTITY_HPP

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

#include <utility> // std::forward

namespace Beman::Example {

struct __is_transparent; // not defined

// A function object that returns its argument unchanged.
struct identity
{
    // Returns `t`.
    template <class T>
#if defined(__cpp_constexpr)
    constexpr
#endif
        T &&
        operator()(T &&t) const noexcept
    {
        return std::forward<T>(t);
    }

    using is_transparent = __is_transparent;
};

} // namespace Beman::Example

#endif // BEMAN_EXAMPLE_IDENTITY_HPP
