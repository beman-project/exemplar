# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(ALL_EXAMPLES 
  #identity_as_default_projection 
identity_direct_usage)

foreach(example ${ALL_EXAMPLES})
  add_executable(beman.example.examples.${example})
  target_sources(beman.example.examples.${example} PRIVATE ${example}.cpp)
  target_link_libraries(beman.example.examples.${example} beman::example)
endforeach()
