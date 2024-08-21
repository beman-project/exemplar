// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <Beman/Example/identity.hpp>

#include <iostream>

int main() {
    std::cout << Beman::Example::identity()(2024) << '\n';
    return 0;
}
