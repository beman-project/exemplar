# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(CMAKE_C_FLAGS_RELEASE_INIT "-O3")
set(CMAKE_CXX_FLAGS_RELEASE_INIT "-O3")

set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "-O3")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "-O3")

# BEMAN_BUILDSYS_SANITIZER is not a general use option
# It is used by preset and CI system.
# There's three possible values:
# TSan: Thread sanitizer
# ASan: All sanitizer (majorly Address sanitizer) that doesn't conflict with TSan
# OFF: No sanitizer

if(DEFINED BEMAN_BUILDSYS_SANITIZER)
    if(BEMAN_BUILDSYS_SANITIZER STREQUAL "ASan")
        # Basic ASan flags
        set(SANITIZER_FLAGS
            "-fsanitize=address -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=undefined"
        )

        # Exclude -fsanitize=leak if using GCC on macOS
        # TODO: Is there a way to detect Apple Clang???
        if(
            CMAKE_CXX_COMPILER_ID STREQUAL "GNU"
            AND CMAKE_SYSTEM_NAME STREQUAL "Darwin"
        )
            message(STATUS "Using GCC on macOS; excluding -fsanitize=leak")
        else()
            set(SANITIZER_FLAGS "${SANITIZER_FLAGS} -fsanitize=leak")
        endif()
    elseif(BEMAN_BUILDSYS_SANITIZER STREQUAL "TSan")
        # Basic ASan flags
        set(SANITIZER_FLAGS "-fsanitize=thread")
    elseif(BEMAN_BUILDSYS_SANITIZER STREQUAL "OFF")
        set(SANITIZER_FLAGS "")
    else()
        message(
            FATAL_ERROR
            "Invalid BEMAN_BUILDSYS_SANITIZER option: ${BEMAN_BUILDSYS_SANITIZER}"
        )
    endif()

    set(CMAKE_C_FLAGS_DEBUG_INIT
        "${CMAKE_C_FLAGS_DEBUG_INIT} ${SANITIZER_FLAGS}"
    )
    set(CMAKE_CXX_FLAGS_DEBUG_INIT
        "${CMAKE_C_FLAGS_DEBUG_INIT} ${SANITIZER_FLAGS}"
    )
endif()
