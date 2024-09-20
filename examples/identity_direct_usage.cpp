// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/exemplar/identity.hpp>

#include <iostream>

int main() {
    std::cout << beman::exemplar::identity()(2024) << '\n';
    return 0;
}
