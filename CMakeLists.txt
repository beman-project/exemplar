# /CMakeLists.txt -*-makefile-*-
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.23)

project(beman_example
  VERSION 1.0.0
  DESCRIPTION "An example Beman library"
  LANGUAGES CXX
)

# Include the CTest module.
include(CTest)

# Build the tests only if enabled via the CLI flag: BUILD_TESTING.
if (BUILD_TESTING)
  enable_testing()

  # Fetch GoogleTest
  include(FetchContent)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
  )
  FetchContent_MakeAvailable(googletest)
endif ()

# Build the library.
add_subdirectory(src/Beman/Example)

# Build the examples.
add_subdirectory(examples)
