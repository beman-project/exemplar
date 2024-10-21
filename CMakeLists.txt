# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")
include(CTest)
include(FetchContent)
include(CompilerFeatureTest)
beman_check_range_support(COMPILER_SUPPORTS_RANGES)

if(BUILD_TESTING)
    enable_testing()

    # Fetch GoogleTest
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG
            f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
        EXCLUDE_FROM_ALL
    )
    block()
        set(INSTALL_GTEST OFF) # Disable GoogleTest installation
        set(BUILD_TESTING OFF) # Disable GoogleTest tests
        FetchContent_MakeAvailable(googletest)
    endblock()
endif()

add_subdirectory(src/beman/exemplar)

add_subdirectory(examples)
