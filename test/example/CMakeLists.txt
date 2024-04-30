# Setup the `lit` tool
add_custom_command(
    OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/venv/bin/lit"
    COMMAND python3 -m venv "${CMAKE_CURRENT_BINARY_DIR}/venv"
    COMMAND "${CMAKE_CURRENT_BINARY_DIR}/venv/bin/pip" install --upgrade pip
    COMMAND "${CMAKE_CURRENT_BINARY_DIR}/venv/bin/pip" install --upgrade lit
)

# Setup the test suite configuration
configure_file("${CMAKE_SOURCE_DIR}/test/support/lit.cfg.in"
               "${CMAKE_CURRENT_BINARY_DIR}/lit.cfg")

add_custom_target(test-depends
    COMMAND true
    DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/venv/bin/lit"
            "${CMAKE_CURRENT_BINARY_DIR}/lit.cfg"
            example
    COMMENT "Setup the test dependencies"
)

add_test(
    NAME setup-tests
    COMMAND "${CMAKE_COMMAND}" --build "${CMAKE_BINARY_DIR}" --target test-depends
)

add_test(
  NAME example.test
  COMMAND "${CMAKE_CURRENT_BINARY_DIR}/venv/bin/lit" -sv "${CMAKE_CURRENT_BINARY_DIR}"
)
set_tests_properties(example.test PROPERTIES DEPENDS setup-tests)
