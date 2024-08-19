# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Add the library.
add_library(beman_example STATIC "")
add_library(beman::example ALIAS beman_example)

# Using the full project version because example does not provide a stable ABI
# between shared library versions
set_property(TARGET beman_example PROPERTY SOVERSION "${PROJECT_VERSION}")

# Set the C++ sources.
target_sources(beman_example PRIVATE
  example.cpp
)
target_include_directories(
  beman_example
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../../../include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/${CMAKE_LOWER_PROJECT_NAME}> # <prefix>/include/scratch
)
# target_sources(example PUBLIC
#   FILE_SET HEADERS
#   BASE_DIRS ../../../
#   FILES ../../../include/
# )

# GNUInstallDirs provides default definitions for CMAKE_INSTALL_LIBDIR
# See: https://cmake.org/cmake/help/latest/module/GNUInstallDirs.html
include(GNUInstallDirs)

# Install the library.
install(TARGETS beman_example
  EXPORT beman_example
  ARCHIVE
    COMPONENT libbeman_example-dev
  FILE_SET HEADERS
    COMPONENT libbeman_example-dev
  LIBRARY
    COMPONENT libbeman_example
    NAMELINK_COMPONENT libbeman_example-dev
)
install(EXPORT beman_example
  FILE beman_example-config.cmake
  DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/${TARGET_LIBRARY}"
  COMPONENT libbeman_example-dev
  NAMESPACE beman::
)

# Build the tests only if enabled via the CLI flag: BUILD_TESTING.
if (BUILD_TESTING)
  add_subdirectory(tests)
endif ()
