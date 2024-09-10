# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# TODO Darius: Find CMake minimum required version.
cmake_minimum_required(VERSION 3.23)

project(
  beman.example # CMake Project Name, which is also the name of the top-level
                # targets (e.g., library, executable, etc.).
  DESCRIPTION "A Beman Library Example"
  LANGUAGES CXX)

include(CTest)
include(FetchContent)

if(BUILD_TESTING)
  enable_testing()

  # Fetch GoogleTest
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
    EXCLUDE_FROM_ALL CMAKE_ARGS -DBUILD_TESTING=OFF)
  FetchContent_MakeAvailable(googletest)
endif()

add_subdirectory(src/beman/example)

add_subdirectory(examples)
