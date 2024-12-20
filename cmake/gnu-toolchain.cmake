# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include_guard(GLOBAL)

set(CMAKE_C_COMPILER gcc)
set(CMAKE_CXX_COMPILER g++)

if(BEMAN_BUILDSYS_SANITIZER STREQUAL "ASan")
    set(SANITIZER_FLAGS
        "-fsanitize=address -fsanitize=leak -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=undefined"
    )
elseif(BEMAN_BUILDSYS_SANITIZER STREQUAL "TSan")
    set(SANITIZER_FLAGS "-fsanitize=thread")
endif()

set(CMAKE_C_FLAGS_DEBUG_INIT "${SANITIZER_FLAGS}")
set(CMAKE_CXX_FLAGS_DEBUG_INIT "${SANITIZER_FLAGS}")

set(RELEASE_FLAG "-O3 ${SANITIZER_FLAGS}")

set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "${RELEASE_FLAG}")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "${RELEASE_FLAG}")

set(CMAKE_C_FLAGS_RELEASE_INIT "${RELEASE_FLAG}")
set(CMAKE_CXX_FLAGS_RELEASE_INIT "${RELEASE_FLAG}")
