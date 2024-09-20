// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <beman/exemplar/identity.hpp>

#include <iostream>

namespace exe = beman::exemplar;

int main() {
    std::cout << exe::identity()(2024) << '\n';
    return 0;
}
