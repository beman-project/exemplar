<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

# beman.exemplar: A Beman Library Exemplar

![Continuous Integration Tests](https://github.com/bemanproject/exemplar/actions/workflows/ci_tests.yml/badge.svg)

`beman.exemplar` is a minimal C++ library conforming to [The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md).
This can be used as a template for those intending to write Beman libraries.
It may also find use as a minimal and modern  C++ project structure.

Implements: `std::identity` proposed in [Standard Library Concepts (P0898R3)](https://wg21.link/P0898R3).

## Usage

`std::identity` is a function object type whose `operator()` returns its argument unchanged.
`std::identity` serves as the default projection in constrained algorithms.
Its direct usage is usually not needed.

### Usage: default projection in constrained algorithms

 The following code snippet illustrates how we can achieve a default projection using `beman::exemplar::identity`:

```cpp
#include <beman/exemplar/identity.hpp>

namespace exe = beman::exemplar;

// Class with a pair of values.
struct Pair
{
    int n;
    std::string s;

    // Output the pair in the form {n, s}.
    // Used by the range-printer if no custom projection is provided (default: identity projection).
    friend std::ostream &operator<<(std::ostream &os, const Pair &p)
    {
        return os << "Pair" << '{' << p.n << ", " << p.s << '}';
    }
};

// A range-printer that can print projected (modified) elements of a range.
// All the elements of the range are printed in the form {element1, element2, ...}.
// e.g., pairs with identity: Pair{1, one}, Pair{2, two}, Pair{3, three}
// e.g., pairs with custom projection: {1:one, 2:two, 3:three}
template <std::ranges::input_range R,
          typename Projection>
void print(const std::string_view rem, R &&range, Projection projection = exe::identity>)
{
    std::cout << rem << '{';
    std::ranges::for_each(
        range,
        [O = 0](const auto &o) mutable
        { std::cout << (O++ ? ", " : "") << o; },
        projection);
    std::cout << "}\n";
};

int main()
{
    // A vector of pairs to print.
    const std::vector<Pair> pairs = {
        {1, "one"},
        {2, "two"},
        {3, "three"},
    };

    // Print the pairs using the default projection.
    print("\tpairs with beman: ", pairs);

    return 0;
}

```

Full runnable examples can be found in `examples/` (e.g., [./examples/identity_as_default_projection.cpp](./examples/identity_as_default_projection.cpp)).

## Building beman.exemplar

### Dependencies
<!-- TODO Darius: rewrite section!-->

This project has no C or C++ dependencies.

Build-time dependencies:

- `cmake`
- `ninja`, `make`, or another CMake-supported build system
  - CMake defaults to "Unix Makefiles" on POSIX systems

#### How to install dependencies

<!-- TODO Darius: rewrite section!-->

<details>
<summary>Dependencies install exemplar on Ubuntu 24.04  </summary>

<!-- TODO Darius: rewrite section!-->

```shell
# Install tools:
apt-get install -y cmake make ninja-build

# Toolchains:
apt-get install                           \
  g++-14 gcc-14 gcc-13 g++-14             \
  clang-18 clang++-18 clang-17 clang++-17
```

</details>

<details>
<summary>Dependencies install exemplar on MAC OS $VERSION </summary>

<!-- TODO Darius: rewrite section!-->
```shell
# TODO
```

</details>

<details>
<summary>Dependencies install exemplar on Windows $VERSION  </summary>
<!-- TODO Darius: rewrite section!-->

```shell
# TODO
```

</details>

### How to build beman.exemplar

This project strives to be as normal and simple a CMake project as possible.
This build workflow in particular will work,
producing a static `libbeman.exemplar.a` library, ready to package with its headers:

```shell
cmake --workflow --preset gcc-debug
cmake --workflow --preset gcc-release
cmake --install build/gcc-release --prefix /opt/beman.exemplar
```

<details>
<summary> Build beman.exemplar (verbose logs) </summary>

```shell
# Configure beman.exemplar via gcc-debug workflow for development.
$ cmake --workflow --preset gcc-debug
Executing workflow step 1 of 3: configure preset "gcc-debug"

Preset CMake variables:

  CMAKE_BUILD_TYPE="Debug"
  CMAKE_CXX_COMPILER="g++"
  CMAKE_CXX_FLAGS="-fsanitize=address -fsanitize=pointer-compare -fsanitize=pointer-subtract -fsanitize=leak -fsanitize=undefined"
  CMAKE_CXX_STANDARD="20"

-- The CXX compiler identification is GNU 11.4.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/g++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- The C compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Found Python3: /usr/bin/python3.10 (found version "3.10.12") found components: Interpreter
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE
-- Configuring done
-- Generating done
-- Build files have been written to: /home/runner/work/exemplar/exemplar/build/gcc-debug

Executing workflow step 2 of 3: build preset "gcc-debug"

[1/14] Building CXX object src/beman/exemplar/CMakeFiles/beman.exemplar.dir/identity.cpp.o
[2/14] Linking CXX static library src/beman/exemplar/libbeman.exemplar.a
[3/14] Building CXX object examples/CMakeFiles/beman.exemplar.examples.identity_direct_usage.dir/identity_direct_usage.cpp.o
[4/14] Linking CXX executable examples/beman.exemplar.examples.identity_direct_usage
[5/14] Building CXX object _deps/googletest-build/googletest/CMakeFiles/gtest_main.dir/src/gtest_main.cc.o
[6/14] Building CXX object src/beman/exemplar/CMakeFiles/beman.exemplar.tests.dir/identity.t.cpp.o
[7/14] Building CXX object _deps/googletest-build/googlemock/CMakeFiles/gmock_main.dir/src/gmock_main.cc.o
[8/14] Building CXX object _deps/googletest-build/googlemock/CMakeFiles/gmock.dir/src/gmock-all.cc.o
[9/14] Building CXX object _deps/googletest-build/googletest/CMakeFiles/gtest.dir/src/gtest-all.cc.o
[10/14] Linking CXX static library lib/libgtest.a
[11/14] Linking CXX static library lib/libgtest_main.a
[12/14] Linking CXX static library lib/libgmock.a
[13/14] Linking CXX static library lib/libgmock_main.a
[14/14] Linking CXX executable src/beman/exemplar/beman.exemplar.tests

Executing workflow step 3 of 3: test preset "gcc-debug"

Test project /home/runner/work/exemplar/exemplar/build/gcc-debug
    Start 1: IdentityTest.call_identity_with_int
1/4 Test #1: IdentityTest.call_identity_with_int ...........   Passed    0.13 sec
    Start 2: IdentityTest.call_identity_with_custom_type
2/4 Test #2: IdentityTest.call_identity_with_custom_type ...   Passed    0.01 sec
    Start 3: IdentityTest.compare_std_vs_beman
3/4 Test #3: IdentityTest.compare_std_vs_beman .............   Passed    0.01 sec
    Start 4: IdentityTest.check_is_transparent
4/4 Test #4: IdentityTest.check_is_transparent .............   Passed    0.01 sec

100% tests passed, 0 tests failed out of 4

Total Test time (real) =   0.18 sec

# Configure beman.exemplar via gcc-release workflow for direct usage.
$ cmake --workflow --preset gcc-release
Executing workflow step 1 of 3: configure preset "gcc-release"

Preset CMake variables:

  CMAKE_BUILD_TYPE="RelWithDebInfo"
  CMAKE_CXX_COMPILER="g++"
  CMAKE_CXX_FLAGS="-O3"
  CMAKE_CXX_STANDARD="20"

-- The CXX compiler identification is GNU 11.4.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/g++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- The C compiler identification is GNU 11.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Found Python3: /usr/bin/python3.10 (found version "3.10.12") found components: Interpreter
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE
-- Configuring done
-- Generating done
-- Build files have been written to: /home/runner/work/exemplar/exemplar/build/gcc-release

Executing workflow step 2 of 3: build preset "gcc-release"

[1/14] Building CXX object src/beman/exemplar/CMakeFiles/beman.exemplar.dir/identity.cpp.o
[2/14] Linking CXX static library src/beman/exemplar/libbeman.exemplar.a
[3/14] Building CXX object examples/CMakeFiles/beman.exemplar.examples.identity_direct_usage.dir/identity_direct_usage.cpp.o
[4/14] Linking CXX executable examples/beman.exemplar.examples.identity_direct_usage
[5/14] Building CXX object _deps/googletest-build/googletest/CMakeFiles/gtest_main.dir/src/gtest_main.cc.o
[6/14] Building CXX object src/beman/exemplar/CMakeFiles/beman.exemplar.tests.dir/identity.t.cpp.o
[7/14] Building CXX object _deps/googletest-build/googlemock/CMakeFiles/gmock_main.dir/src/gmock_main.cc.o
[8/14] Building CXX object _deps/googletest-build/googlemock/CMakeFiles/gmock.dir/src/gmock-all.cc.o
[9/14] Building CXX object _deps/googletest-build/googletest/CMakeFiles/gtest.dir/src/gtest-all.cc.o
[10/14] Linking CXX static library lib/libgtest.a
[11/14] Linking CXX static library lib/libgtest_main.a
[12/14] Linking CXX static library lib/libgmock.a
[13/14] Linking CXX executable src/beman/exemplar/beman.exemplar.tests
[14/14] Linking CXX static library lib/libgmock_main.a

Executing workflow step 3 of 3: test preset "gcc-release"

Test project /home/runner/work/exemplar/exemplar/build/gcc-release
    Start 1: IdentityTest.call_identity_with_int
1/4 Test #1: IdentityTest.call_identity_with_int ...........   Passed    0.00 sec
    Start 2: IdentityTest.call_identity_with_custom_type
2/4 Test #2: IdentityTest.call_identity_with_custom_type ...   Passed    0.00 sec
    Start 3: IdentityTest.compare_std_vs_beman
3/4 Test #3: IdentityTest.compare_std_vs_beman .............   Passed    0.00 sec
    Start 4: IdentityTest.check_is_transparent
4/4 Test #4: IdentityTest.check_is_transparent .............   Passed    0.00 sec

100% tests passed, 0 tests failed out of 4

Total Test time (real) =   0.01 sec

# Run examples.
$ build/gcc-release/examples/beman.exemplar.examples.identity_direct_usage
2024

```

</details>

<details>
<summary> Install beman.exemplar (verbose logs) </summary>

```shell
# Install build artifacts from `build` directory into `opt/beman.exemplar` path.
$ cmake --install build/gcc-release --prefix /opt/beman.exemplar
-- Install configuration: "RelWithDebInfo"
-- Up-to-date: /opt/beman.exemplar/lib/libbeman.exemplar.a
-- Up-to-date: /opt/beman.exemplar/include/beman/exemplar/identity.hpp


# Check tree.
$ tree /opt/beman.exemplar
/opt/beman.exemplar
├── include
│   └── beman
│       └── exemplar
│           └── identity.hpp
└── lib
    └── libbeman.exemplar.a

4 directories, 2 files
```

</details>

<details>
<summary> Disable tests build </summary>

To build this project with tests disabled (and their dependencies),
simply use `BEMAN_EXEMPLAR_BUILD_TESTING=OFF` as documented in upstream [CMake documentation](https://cmake.org/cmake/help/latest/module/CTest.html):

```shell
cmake -B build -S . -DBEMAN_EXEMPLAR_BUILD_TESTING=OFF
```

</details>

## Integrate beman.exemplar into your project

<details>
<summary> Use beman.exemplar directly from C++ </summary>
<!-- TODO Darius: rewrite section!-->

If you want to use `beman.exemplar` from your project,
you can include `beman/exemplar/*.hpp`  files from your C++ source files

```cpp
#include <beman/exemplar/identity.hpp>
```

and directly link with `libbeman.exemplar.a`

```shell
# Assume /opt/beman.exemplar staging directory.
$ c++ -o identity_usage examples/identity_usage.cpp \
    -I /opt/beman.exemplar/include/ \
    -L/opt/beman.exemplar/lib/ -lbeman.exemplar
```

</details>

<details>
<summary> Use beman.exemplar directly from CMake </summary>

<!-- TODO Darius: rewrite section! Add examples. -->

For CMake based projects, you will need to use the `beman.exemplar` CMake module to define the `beman::exemplar` CMake target:

```cmake
find_package(beman.exemplar REQUIRED)
```

You will also need to add `beman::exemplar`
to the link libraries of any libraries or executables that include `beman/exemplar/*.hpp` in their source or header file.

```cmake
target_link_libraries(yourlib PUBLIC beman::exemplar)
```

</details>

<details>
<summary> Use beman.exemplar from other build systems </summary>

<!-- TODO Darius: rewrite section! Add examples. -->

Build systems that support `pkg-config` by providing a `beman.exemplar.pc` file.
Build systems that support interoperation via `pkg-config` should be able to detect `beman.exemplar` for you automatically.

</details>

## Contributing

Please do! Issues and pull requests are appreciated.
