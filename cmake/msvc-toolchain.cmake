# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include_guard(GLOBAL)

set(CMAKE_C_COMPILER cl)
set(CMAKE_CXX_COMPILER cl)

if(BEMAN_BUILDSYS_SANITIZER STREQUAL "ASan")
    set(SANITIZER_FLAGS "/fsanitize=address /Zi")
endif()

set(CMAKE_CXX_FLAGS_DEBUG_INIT "/EHsc /permissive- ${SANITIZER_FLAGS}")
set(CMAKE_C_FLAGS_DEBUG_INIT "/EHsc /permissive- ${SANITIZER_FLAGS}")

set(CMAKE_C_FLAGS_RELWITHDEBINFO_INIT
    "/EHsc /permissive- /O2 ${SANITIZER_FLAGS}"
)
set(CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT
    "/EHsc /permissive- /O2 ${SANITIZER_FLAGS}"
)
