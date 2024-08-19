# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Include the GoogleTest CMake module.
include(GoogleTest)

# Add the test executable.
add_executable(beman_example_test)

# Set the C++ sources.
target_sources(beman_example_test PRIVATE
  example.t.cpp
)

# Link the library.
target_link_libraries(beman_example_test PRIVATE beman::example GTest::gtest GTest::gtest_main)

# Add the tests.
gtest_add_tests(beman_example_test "" AUTO)
