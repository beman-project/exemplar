# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# BEMAN_BUILDSYS_SANITIZER is not a general use option
# It is used by preset and CI system.
# There's three possible values:
# TSan: Thread sanitizer
# ASan: All sanitizer (majorly Address sanitizer) that doesn't conflict with TSan
# OFF: No sanitizer

if(DEFINED BEMAN_BUILDSYS_SANITIZER)
    message("Applying sanitizers for ${CMAKE_CXX_COMPILER_ID}")

    if(BEMAN_BUILDSYS_SANITIZER STREQUAL "ASan")
        set(_ASAN_ADDR "-fsanitize=address")
        set(_ASAN_LEAK "-fsanitize=leak")
        set(_ASAN_MISC
            "-fsanitize=address -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=undefined"
        )

        # Exclude -fsanitize=leak on Apple Clang as it is not supported.
        if(CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
            message(STATUS "Using AppleClang; excluding -fsanitize=leak")
            set(SANITIZER_FLAGS "${_ASAN_ADDR} ${_ASAN_MISC}")
            # Only include Address sanitizer on MSVC, debug info must be included for MSVC to work
        elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
            message(STATUS "Using MSVC; only Address sanitizer is set")
            set(SANITIZER_FLAGS "/fsanitize=address /Zi")
            # We are able to enable all sanitizers on Clang and GNU
        elseif(
            CMAKE_CXX_COMPILER_ID STREQUAL "Clang"
            OR CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
        )
            set(SANITIZER_FLAGS "${_ASAN_ADDR} ${_ASAN_LEAK} ${_ASAN_MISC}")
        else()
            message(
                STATUS
                "Unknown compiler ${CMAKE_CXX_COMPILER_ID}, no sanitizer is set"
            )
        endif()
    elseif(BEMAN_BUILDSYS_SANITIZER STREQUAL "TSan")
        # Basic TSan flags
        if(
            CMAKE_CXX_COMPILER_ID STREQUAL "Clang"
            OR CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
        )
            set(SANITIZER_FLAGS "-fsanitize=thread")
        else()
            message(
                STATUS
                "TSan not supported/ Unknown compiler: ${CMAKE_CXX_COMPILER_ID}, no sanitizer is set"
            )
        endif()
    elseif(BEMAN_BUILDSYS_SANITIZER STREQUAL "OFF")
        set(SANITIZER_FLAGS "")
    else()
        message(
            FATAL_ERROR
            "Invalid BEMAN_BUILDSYS_SANITIZER option: ${BEMAN_BUILDSYS_SANITIZER}"
        )
    endif()

    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${SANITIZER_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${SANITIZER_FLAGS}")
endif()
