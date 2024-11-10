# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(GoogleTest)

add_executable(beman.exemplar.tests.identity)
target_sources(beman.exemplar.tests.identity PRIVATE identity.test.cpp)
target_link_libraries(
    beman.exemplar.tests.identity
    PRIVATE beman::exemplar GTest::gtest GTest::gtest_main
)

gtest_add_tests(beman.exemplar.tests.identity "" AUTO)
