# Copyright © 2024 Bret Brown
# SPDX-License-Identifier: MIT

add_library(example)
add_library(example::example ALIAS example)

# Using the full project version because example does not provide a stable ABI
# between shared library versions
set_property(TARGET example PROPERTY SOVERSION "${PROJECT_VERSION}")

target_sources(example PRIVATE
  example.cpp
)
target_sources(example PUBLIC
  FILE_SET HEADERS
  BASE_DIRS .
  FILES example.hpp
)

# GNUInstallDirs provides default definitions for CMAKE_INSTALL_LIBDIR
# See: https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html
include(GNUInstallDirs)

install(TARGETS example
  EXPORT example
  ARCHIVE
    COMPONENT libexample-dev
  FILE_SET HEADERS
    COMPONENT libexample-dev
  LIBRARY
    COMPONENT libexample
    NAMELINK_COMPONENT libexample-dev
)
install(EXPORT example
  FILE example-config.cmake
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/example"
  COMPONENT libexample-dev
  NAMESPACE example::
)
