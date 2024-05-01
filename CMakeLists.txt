# Copyright © 2024 Bret Brown
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.23)
project(example
  VERSION 1.0.0
  DESCRIPTION "An example Beman library"
  LANGUAGES CXX
)
include(CTest)

add_subdirectory(src/example)

if (BUILD_TESTING)
  add_subdirectory(test/example)
endif ()
