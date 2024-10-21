# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(ALL_EXAMPLES identity_direct_usage)
if(COMPILER_SUPPORTS_RANGES)
    list(APPEND ALL_EXAMPLES identity_as_default_projection)
else()
    message(WARNING "Missing range support! Skip: identity_as_default_projection")
endif()

foreach(example ${ALL_EXAMPLES})
    add_executable(beman.exemplar.examples.${example})
    target_sources(beman.exemplar.examples.${example} PRIVATE ${example}.cpp)
    target_link_libraries(beman.exemplar.examples.${example} beman::exemplar)
endforeach()
