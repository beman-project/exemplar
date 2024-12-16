# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include_guard(GLOBAL)

set(CMAKE_C_COMPILER cl)
set(CMAKE_CXX_COMPILER cl)

if(BEMAN_BUILDSYS_SANITIZER STREQUAL "ASan")
    set(CMAKE_CXX_FLAGS_DEBUG_INIT "/fsanitize=address /Zi")
    set(CMAKE_C_FLAGS_DEBUG_INIT "/fsanitize=address /Zi")
endif()

set(CMAKE_CXX_FLAGS_DEBUG_INIT
    "${CMAKE_CXX_FLAGS_DEBUG_INIT} /EHsc /permissive-"
)
set(CMAKE_C_FLAGS_DEBUG_INIT "${CMAKE_C_FLAGS_DEBUG_INIT} /EHsc /permissive-")

set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "/EHsc /permissive- /O2")
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "/EHsc /permissive- /O2")
