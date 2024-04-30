//
// This test runs using clang-verify. This allows checking that specific
// diagnostics are being emitted at compile-time.
//
// Clang-verify supports various directives like 'expected-error',
// 'expected-warning', etc. The full set of directives supported and
// how to use them is documented in https://clang.llvm.org/docs/InternalsManual.html#specifying-diagnostics.
//

#include <string>
#include <example.hxx>

void f() {
    foo<std::string>(); // expected-error@*:* {{static assertion failed due to requirement 'std::is_trivially_copyable_v}}
}
