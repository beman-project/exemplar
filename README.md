<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

# beman.exemplar: A Beman Library Exemplar

![Continuous Integration Tests](https://github.com/beman-project/exemplar/actions/workflows/ci_tests.yml/badge.svg)

`beman.exemplar` is a minimal C++ library conforming to [The Beman Standard](https://github.com/beman-project/beman/blob/main/docs/beman-standard.md).
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

Full runable examples can be found in `examples/` (e.g., [./examples/identity_as_default_projection.cpp.cpp](./examples/identity_as_default_projection.cpp.cpp)).

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
cmake -B build -S . -DCMAKE_CXX_STANDARD=20
cmake --build build
ctest --test-dir build
cmake --install build --prefix /opt/beman.exemplar
```

<details>
<summary> Build beman.exemplar (verbose logs) </summary>

```shell
# Configure beman.exemplar.
$ cmake -B build -S . -DCMAKE_CXX_STANDARD=20
-- The CXX compiler identification is GNU 13.2.0
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Configuring done (0.1s)
-- Generating done (0.0s)
-- Build files have been written to: /path/to/repo/build

# Build beman.exemplar.
$ cmake --build build
[ 10%] Building CXX object src/beman/exemplar/CMakeFiles/beman.exemplar.dir/identity.cpp.o
[ 20%] Linking CXX static library libbeman.exemplar.a
[ 20%] Built target beman.exemplar
[ 30%] Building CXX object _deps/googletest-build/googletest/CMakeFiles/gtest.dir/src/gtest-all.cc.o
[ 40%] Linking CXX static library ../../../lib/libgtest.a
[ 40%] Built target gtest
[ 50%] Building CXX object _deps/googletest-build/googletest/CMakeFiles/gtest_main.dir/src/gtest_main.cc.o
[ 60%] Linking CXX static library ../../../lib/libgtest_main.a
[ 60%] Built target gtest_main
[ 70%] Building CXX object src/beman/exemplar/tests/CMakeFiles/beman.exemplar.Test.dir/identity.t.cpp.o
[ 80%] Linking CXX executable beman.exemplar.Test
[ 80%] Built target beman.exemplar.Test
[ 90%] Building CXX object examples/CMakeFiles/identity_usage.dir/identity_usage.cpp.o
[100%] Linking CXX executable identity_usage
[100%] Built target identity_usage

# Run beman.exemplar tests.
$ ctest --test-dir build
Internal ctest changing into directory: /path/to/your/repo/build
Test project /path/to/your/repo/build
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
$ build/exemplar/beman.exemplar.examples.identity_direct_usage
2024

```

</details>

<details>
<summary> Install beman.exemplar (verbose logs) </summary>

```shell
# Install build artifacts from `build` directory into `opt/beman.exemplar` path.
$ cmake --install build --prefix /opt/beman.exemplar
-- Install configuration: ""
-- Up-to-date: /opt/beman.exemplar/lib/libbeman.exemplar.a
-- Up-to-date: /opt/beman.exemplar/include
-- Up-to-date: /opt/beman.exemplar/include/beman
-- Up-to-date: /opt/beman.exemplar/include/beman/exemplar
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

5 directories, 2 files
```

</details>

<details>
<summary> Disable tests build </summary>

To build this project with tests disabled (and their dependencies),
simply use `BUILD_TESTING=OFF` as documented in upstream [CMake documentation](https://cmake.org/cmake/help/latest/module/CTest.html):

```shell
cmake -B build -S . -DBUILD_TESTING=OFF
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
