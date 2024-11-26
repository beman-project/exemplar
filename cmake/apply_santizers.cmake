# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# BEMAN_BUILDSYS_SANITIZER is not a general use option
# It is used by preset and CI system.
# There's three possible values:
# TSan: Thread sanitizer
# ASan: All sanitizer (majorly Address sanitizer) that doesn't conflict with TSan
# OFF: No sanitizer

function(GENERATE_SANITIZER_PARAM KIND COMPILER_ID SANITIZER_FLAGS)
    if(${KIND} STREQUAL "ASan")
        set(_ASAN_ADDR "-fsanitize=address")
        set(_ASAN_LEAK "-fsanitize=leak")
        set(_ASAN_MISC
            "-fsanitize=address -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=undefined"
        )

        if(${COMPILER_ID} STREQUAL "AppleClang")
            # Exclude -fsanitize=leak on Apple Clang as it is not supported.
            message(STATUS "Using AppleClang; excluding -fsanitize=leak")
            set(RES "${_ASAN_ADDR} ${_ASAN_MISC}")
        elseif(${COMPILER_ID} STREQUAL "MSVC")
            # Only include Address sanitizer on MSVC, debug info must be included for MSVC to work
            message(STATUS "Using MSVC; only Address sanitizer is set")
            set(RES "/fsanitize=address /Zi")
        elseif(${COMPILER_ID} STREQUAL "Clang" OR ${COMPILER_ID} STREQUAL "GNU")
            # We are able to enable all sanitizers on Clang and GNU
            set(RES "${_ASAN_ADDR} ${_ASAN_LEAK} ${_ASAN_MISC}")
        else()
            message(
                STATUS
                "Unknown compiler ${${COMPILER_ID}}, no sanitizer is set"
            )
        endif()
    elseif(KIND STREQUAL "TSan")
        # Basic TSan flags
        if(${COMPILER_ID} STREQUAL "Clang" OR ${COMPILER_ID} STREQUAL "GNU")
            set(RES "-fsanitize=thread")
        else()
            message(
                STATUS
                "TSan not supported/ Unknown compiler: ${${COMPILER_ID}}, no sanitizer is set"
            )
        endif()
    elseif(KIND STREQUAL "OFF")
        set(RES "")
    else()
        message(FATAL_ERROR "Invalid Sanitizer class kind option: ${KIND}")
    endif()

    set(${SANITIZER_FLAGS} ${RES} PARENT_SCOPE)
endfunction()
