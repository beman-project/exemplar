# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25...3.31)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
)

if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_BINARY_DIR})
    message(FATAL_ERROR "In-source builds are not allowed!")
endif()

include(CPack)
include(FetchContent)
include(GNUInstallDirs)

add_subdirectory(src/beman/exemplar)

option(BUILD_TESTING "build tests too" ${PROJECT_IS_TOP_LEVEL})
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
        set(BUILD_GMOCK OFF)
        set(CMAKE_CXX_FLAGS) # FIXME: Do not propagate our project settings! CK
        FetchContent_MakeAvailable(googletest)
    endblock()

    add_subdirectory(tests/beman/exemplar)
endif()

if(PROJECT_IS_TOP_LEVEL)
    add_subdirectory(examples)
endif()
