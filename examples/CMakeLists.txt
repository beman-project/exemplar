# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

set(ALL_EXAMPLES sample_usage)

foreach(example ${ALL_EXAMPLES})
  add_executable(${example} "")

  target_sources(${example} PRIVATE ${example}.cpp)

  target_link_libraries(${example} Beman::Example)
endforeach()
