// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#ifndef BEMAN_EXEMPLAR_IDENTITY_HPP
#define BEMAN_EXEMPLAR_IDENTITY_HPP

// C++ Standard Library: std::identity equivalent.
// See https://eel.is/c++draft/func.identity:
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

namespace beman::exemplar {

struct __is_transparent; // not defined

// A function object that returns its argument unchanged.
struct identity {
    // Returns `t`.
    template <class T>
    constexpr T&& operator()(T&& t) const noexcept {
        return std::forward<T>(t);
    }

    using is_transparent = __is_transparent;
};

} // namespace beman::exemplar

#endif // BEMAN_EXEMPLAR_IDENTITY_HPP
