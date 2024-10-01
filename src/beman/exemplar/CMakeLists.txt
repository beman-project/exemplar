# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.exemplar STATIC)
add_library(beman::exemplar ALIAS beman.exemplar)

target_sources(beman.exemplar PRIVATE identity.cpp)

set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../../include/)

target_sources(
  beman.exemplar PUBLIC
  FILE_SET HEADERS
  BASE_DIRS ${INCLUDE_DIR}
  FILES ${INCLUDE_DIR}/beman/exemplar/identity.hpp)

target_compile_features(beman.exemplar PUBLIC cxx_std_17)

set_target_properties(beman.exemplar PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

install(
  TARGETS beman.exemplar
  EXPORT beman.exemplar
  FILE_SET HEADERS
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

if(BUILD_TESTING)
  include(GoogleTest)

  add_executable(beman.exemplar.tests)
  target_sources(beman.exemplar.tests PRIVATE identity.t.cpp)
  target_link_libraries(beman.exemplar.tests
                        PRIVATE beman::exemplar GTest::gtest GTest::gtest_main)

  gtest_add_tests(beman.exemplar.tests "" AUTO)
endif()
