# # SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Functions that determine compiler capabilities

include(CheckCXXSourceCompiles)

# Determines if the selected C++ compiler has ranges support.
# Sets 'result_var' to whether support is detected.
function(beman_check_range_support result_var)
    # Check if the C++ standard is at least C++20 or later.
    if(CMAKE_CXX_STANDARD LESS 20)
        set(${result_var} FALSE PARENT_SCOPE)
        return()
    endif()

    check_cxx_source_compiles(
        "
        #include <ranges> // C++20 ranges; note that __cpp_lib_ranges is not defined for all compilers
        int main(){ return 0; }
        "
        _HAVE_RANGE_SUPPORT
    )

    set(${result_var} ${_HAVE_RANGE_SUPPORT} PARENT_SCOPE)
endfunction()
