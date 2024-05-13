add_executable(example.test)
target_sources(example.test PRIVATE example.test.cpp)
target_link_libraries(example.test PRIVATE example::example)

add_test(
  NAME example.test
  COMMAND example.test
)
