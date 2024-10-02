# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

add_library(beman.exemplar STATIC)
add_library(beman::exemplar ALIAS beman.exemplar)

target_sources(beman.exemplar PRIVATE identity.cpp)

set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../../include/)

target_sources(
    beman.exemplar
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${INCLUDE_DIR}
        FILES ${INCLUDE_DIR}/beman/exemplar/identity.hpp
)

set_target_properties(beman.exemplar PROPERTIES VERIFY_INTERFACE_HEADER_SETS ON)

install(
    TARGETS beman.exemplar
    EXPORT beman.exemplar
    DESTINATION
    $<$<CONFIG:Debug>:debug/>${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION $<$<CONFIG:Debug>:debug/>${CMAKE_INSTALL_BINDIR}
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

if(BUILD_TESTING)
    include(GoogleTest)

    add_executable(beman.exemplar.tests)
    target_sources(beman.exemplar.tests PRIVATE identity.t.cpp)
    target_link_libraries(
        beman.exemplar.tests
        PRIVATE beman::exemplar GTest::gtest GTest::gtest_main
    )

    gtest_add_tests(beman.exemplar.tests "" AUTO)
endif()
