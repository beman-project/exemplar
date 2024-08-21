# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(GoogleTest)

set(TARGET_LIBRARY_TESTS "${TARGET_LIBRARY}.Test")

add_executable(${TARGET_LIBRARY_TESTS})

target_sources(${TARGET_LIBRARY_TESTS} PRIVATE identity.t.cpp)

target_link_libraries(${TARGET_LIBRARY_TESTS}
                      PRIVATE Beman::Example GTest::gtest GTest::gtest_main)

gtest_add_tests(${TARGET_LIBRARY_TESTS} "" AUTO)
