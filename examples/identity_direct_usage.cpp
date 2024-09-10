// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/example/identity.hpp>

#include <iostream>

int main() {
    std::cout << beman::example::identity()(2024) << '\n';
    return 0;
}
