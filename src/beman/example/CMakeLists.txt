# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.example STATIC)
add_library(beman::example ALIAS beman.example)

target_sources(beman.example PRIVATE identity.cpp)

target_include_directories(
  beman.example
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../../../include>)

install(
  TARGETS beman.example
  EXPORT beman.example
  DESTINATION ${CMAKE_INSTALL_LIBDIR})

install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../../../include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  FILES_MATCHING
  PATTERN "*.hpp")

if(BUILD_TESTING)
  include(GoogleTest)

  add_executable(beman.example.tests)
  target_sources(beman.example.tests PRIVATE identity.t.cpp)
  target_link_libraries(beman.example.tests
                        PRIVATE beman::example GTest::gtest GTest::gtest_main)

  gtest_add_tests(beman.example.tests "" AUTO)
endif()
