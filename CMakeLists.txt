# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

cmake_minimum_required(VERSION 3.25)

project(
    beman.exemplar # CMake Project Name, which is also the name of the top-level
    # targets (e.g., library, executable, etc.).
    DESCRIPTION "A Beman library exemplar"
    LANGUAGES CXX
)

include(CTest)
include(FetchContent)

if(BUILD_TESTING)
    enable_testing()

    block()
        # Disable installing google test dependency on cmake --install
        set(INSTALL_GTEST OFF)

        # Fetch GoogleTest
        FetchContent_Declare(
            googletest
            GIT_REPOSITORY https://github.com/google/googletest.git
            GIT_TAG
                f8d7d77c06936315286eb55f8de22cd23c188571 # release-1.14.0
            EXCLUDE_FROM_ALL
            CMAKE_ARGS
            -DBUILD_TESTING=OFF
        )
        FetchContent_MakeAvailable(googletest)
    endblock()
endif()

add_subdirectory(src/beman/exemplar)

add_subdirectory(examples)
