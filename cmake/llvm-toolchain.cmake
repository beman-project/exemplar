# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include_guard(GLOBAL)

set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

if(BEMAN_BUILDSYS_SANITIZER STREQUAL "ASan")
    set(CMAKE_CXX_FLAGS_DEBUG_INIT
        "-fsanitize=address -fsanitize=leak -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=undefined"
    )
    set(CMAKE_C_FLAGS_DEBUG_INIT
        "-fsanitize=address -fsanitize=leak -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=undefined"
    )
elseif(BEMAN_BUILDSYS_SANITIZER STREQUAL "TSan")
    set(CMAKE_CXX_FLAGS_DEBUG_INIT "-fsanitize=thread")
    set(CMAKE_C_FLAGS_DEBUG_INIT "-fsanitize=thread")
endif()

set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "-O3")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "-O3")
