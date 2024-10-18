// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

// This example demonstrates the usage of beman::exemplar::identity as a default projection in a range-printer.
// Requires: range support (C++20) and std::identity support (C++20).
// TODO Darius: Do we need to selectively compile this example?
// Or should we assume that this project is compiled with C++20 support only?

#include <beman/exemplar/identity.hpp>

#include <algorithm>
#include <functional> // std::identity
#include <iostream>
#include <ranges>
#include <string>

namespace exe = beman::exemplar;

// Class with a pair of values.
struct Pair {
    int         n;
    std::string s;

    // Output the pair in the form {n, s}.
    // Used by the range-printer if no custom projection is provided (default: identity projection).
    friend std::ostream& operator<<(std::ostream& os, const Pair& p) {
        return os << "Pair" << '{' << p.n << ", " << p.s << '}';
    }
};

// A range-printer that can print projected (modified) elements of a range.
// All the elements of the range are printed in the form {element1, element2, ...}.
// e.g., pairs with identity: Pair{1, one}, Pair{2, two}, Pair{3, three}
// e.g., pairs with custom projection: {1:one, 2:two, 3:three}
template <std::ranges::input_range R, typename Projection>
void print_helper(const std::string_view rem, R&& range, Projection projection) {
    std::cout << rem << '{';
    std::ranges::for_each(range, [O = 0](const auto& o) mutable { std::cout << (O++ ? ", " : "") << o; }, projection);
    std::cout << "}\n";
};

// Print wrapper with exe::identity.
template <std::ranges::input_range R,
          typename Projection = exe::identity> // <- Notice the default projection.
void print_beman(const std::string_view rem, R&& range, Projection projection = {}) {
    print_helper(rem, range, projection);
}

// Print wrapper with std::identity.
template <std::ranges::input_range R,
          typename Projection = std::identity> // <- Notice the default projection.
void print_std(const std::string_view rem, R&& range, Projection projection = {}) {
    print_helper(rem, range, projection);
}

int main() {
    // A vector of pairs to print.
    const std::vector<Pair> pairs = {
        {1, "one"},
        {2, "two"},
        {3, "three"},
    };

    // Print the pairs using the default projection.
    std::cout << "Default projection:\n";
    print_beman("\tpairs with beman: ", pairs);
    print_std("\tpairs with   std: ", pairs);

    // Print the pairs using a custom projection.
    std::cout << "Custom projection:\n";
    print_beman("\tpairs with beman: ", pairs, [](const auto& p) { return std::to_string(p.n) + ':' + p.s; });
    print_std("\tpairs with   std: ", pairs, [](const auto& p) { return std::to_string(p.n) + ':' + p.s; });

    return 0;
}
