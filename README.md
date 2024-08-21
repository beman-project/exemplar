<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

# Beman.Example: A Beman Library Example

![CI Tests](https://github.com/beman-project/Example/actions/workflows/ci_tests.yml/badge.svg)

`Beman.Example` is an example Beman library. `Beman.Example` is useful for nothing, though it might contain value as an experiment in modern and minimal C++ project structure. Please check [The Beman Standard](https://github.com/beman-project/beman/blob/main/docs/beman-standard.md).

Implements: N/A for `Beman.Example`.

## License

Source and docs are licenced with Apache License v2.0 with LLVM Exceptions. Copy the contents and incorporate in your own work as you see fit.

// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

## Building

### Dependencies

This project is mainly tested on Ubuntu `22.04` and `24.04`, but it should be as portable as CMake is.

This project has no C or C++ dependencies.

Build-time dependencies:

- `cmake`
- `ninja`, `make`, or another CMake-supported build system
  - CMake defaults to "Unix Makefiles" on POSIX systems

Example of installation on `Ubuntu 24.04`:

```shell
# Install tools:
apt-get install -y cmake make ninja-build

# Example of toolchains:
apt-get install                           \
  g++-14 gcc-14 gcc-13 g++-14             \
  clang-18 clang++-18 clang-17 clang++-17
```

### Instructions

Full set of supported toolchains can be found in [.github/workflows/ci_test.yml](.github/workflows/ci_test.yml).

#### Basic Build

This project strives to be as normal and simple a CMake project as possible. This build workflow in particular will work, producing a static `example` library, ready to package:

```shell
cmake -B ./build -S .
cmake --build ./build
ctest --test-dir ./build
DESTDIR=./build cmake --install ./build --component libbeman_example-dev --prefix /opt/example
```

<details>
<summary> Build example (with logs) </summary>

```shell
# Configure example.
$ cmake -B ./build -S .
-- The CXX compiler identification is GNU 13.2.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done (0.1s)
-- Generating done (0.0s)
-- Build files have been written to: /path/to/repo/build

# Build example.
$ cmake --build ./build
[ 14%] Built target gtest
[ 28%] Built target gmock
[ 42%] Built target gmock_main
[ 57%] Built target gtest_main
[ 71%] Built target beman_example
[ 78%] Building CXX object src/Beman/Example/tests/CMakeFiles/example_gtest.dir/example.t.cpp.o
[ 85%] Linking CXX executable example_gtest
[ 85%] Built target example_gtest
[100%] Built target sample_usage

# Run tests example.
$ ctest --test-dir ./build
Internal ctest changing into directory: /path/to/repo/build
Test project /path/to/repo/build
    Start 1: ExampleTest.call_identity
1/1 Test #1: ExampleTest.call_identity ........   Passed    0.00 sec

100% tests passed, 0 tests failed out of 1

# Run examples.
$ ./build/examples/sample_usage
2024
```
</details>

If all of those steps complete successfully, you should see the library installed in your staging directory.

An example command:
```shell
find /some/staging/dir -type f
```

You will see files like so:

```
/some/staging/dir
└── opt
    └── example
        ├── include
        │   └── example.hxx
        └── lib
            ├── cmake
            │   └── example
            │       ├── example-noconfig.cmake
            │       └── example.cmake
            └── libexample.a
```

#### Disable Tests Build

To build this project with skiped tests and its dependencies, simply use `BUILD_TESTING=OFF` [as documented in upstream CMake documentation](https://cmake.org/cmake/help/latest/module/CTest.html:

```shell
cmake -B /some/build/dir -S . -DBUILD_TESTING=OFF
```

#### Manipulating Warnings

To build this project with warnings enabled, simply use `CMAKE_CXX_FLAGS` [as documented in upstream CMake documentation](https://cmake.org/cmake/help/latest/variable/CMAKE_LANG_FLAGS.html):

```shell
cmake -B /some/build/dir -S . -DCMAKE_CXX_FLAGS='-Werror=all -Wno-error=deprecated-declarations'
```

Otherwise follow the Basic Build workflow as described above.


#### Sanitizers and Coverage Analysis

To build this project with sanitizers enabled, simply use `CMAKE_CXX_FLAGS` [as documented in upstream CMake documentation](https://cmake.org/cmake/help/latest/variable/CMAKE_LANG_FLAGS.html). For instance, to enable an address sanitizer build:

```shell
cmake -B /some/build/dir -S . -DCMAKE_CXX_FLAGS='-sanitize=address'
```

Similarly, but enabling coverage analysis:

```shell
cmake -B /some/build/dir -S . -DCMAKE_CXX_FLAGS='--coverage'
```

Otherwise follow the Basic Build workflow as described above.


#### `clang-tidy`

To enable `clang-tidy` on this project, simply use `CMAKE_CXX_CLANG_TIDY` [as documented in upstream CMake documentation](https://cmake.org/cmake/help/latest/variable/CMAKE_LANG_CLANG_TIDY.html). For instance, to enable only the `cppcoreguidelines` checks:

```shell
cmake -B /some/build/dir -S . -DCMAKE_CXX_CLANG_TIDY="clang-tidy;-checks=-*,cppcoreguidelines-*"
```

Otherwise follow the Basic Build workflow as described above.


## Usage

### From C++

If you *really* want to use `Beman.Example` from your project (why???), you can include `Beman/Example/example.hpp` from your C++ source files

```cxx
#include <Beman/Example/example.hpp>
```

`Beman.Example` supports C++11 to C++26. It has no known issues with C++29, though there are no compilation toolchains available to test against in those build modes.


### From CMake

For consumers using CMake, you will need to use the `beman_example` CMake module to define the `beman_example` CMake target:

```cmake
find_package(beman_example REQUIRED)
```

You will also need to add `beman::example` to the link libraries of any libraries or executables that include `example.hpp` in their source or header file.

```cmake
target_link_libraries(yourlib PUBLIC beman::example)
```

### From Other Build Systems

Build systems that support `pkg-config` by providing a `beman_example.pc` file. Build systems that support interoperation via `pkg-config` should be able to detect `beman_example` for you automatically.

## Contributing

Please do! Issues and pull requests are appreciated.

Note that adding more C++ code will be out of scope for this project. Changes that further improve or simplify this project given that goal are appreciated. Enhancements to better support packaging ecosystems would also make sense.
