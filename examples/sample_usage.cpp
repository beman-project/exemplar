// examples/sample_usage.cpp -*-C++-*-
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

#include <Beman/Example/example.hpp>
#include <iostream>

int main() {
    std::cout << beman::example::identity()(2024) << std::endl;
    return 0;
}
