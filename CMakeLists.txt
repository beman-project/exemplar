# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# TODO Darius: Find CMake minimum required version.
cmake_minimum_required(VERSION 3.23)

project(
  beman.exemplar
  DESCRIPTION "A Beman library exemplar"
  VERSION 0.0.0
  LANGUAGES CXX)

include(CMakePackageConfigHelpers)
include(CTest)
include(FetchContent)
include(GNUInstallDirs)

set(TARGETS_EXPORT_NAME ${CMAKE_PROJECT_NAME}Targets)
set(INSTALL_CONFIGDIR ${CMAKE_INSTALL_LIBDIR}/cmake)

if(BUILD_TESTING)
  enable_testing()

  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
    EXCLUDE_FROM_ALL CMAKE_ARGS -DBUILD_TESTING=OFF)
  FetchContent_MakeAvailable(googletest)
endif()

add_subdirectory(src/beman/exemplar)
add_subdirectory(examples)

write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}ConfigVersion.cmake
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY AnyNewerVersion)

configure_package_config_file(
  "cmake/Config.cmake.in"
  ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}Config.cmake
  INSTALL_DESTINATION ${INSTALL_CONFIGDIR})

install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}Config.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}ConfigVersion.cmake
  DESTINATION ${INSTALL_CONFIGDIR})
