# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(ALL_EXAMPLES # identity_as_default_projection
    identity_direct_usage
)

foreach(example ${ALL_EXAMPLES})
    add_executable(beman.exemplar.examples.${example})
    target_sources(beman.exemplar.examples.${example} PRIVATE ${example}.cpp)
    target_link_libraries(beman.exemplar.examples.${example} beman::exemplar)
endforeach()
