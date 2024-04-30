//
// This test runs whatever shell commands are specified in the RUN commands
// below. This provides a lot of flexibility for controlling how the test
// gets built and run.
//

// RUN: %{cxx} %{flags} %s -DTRANSLATION_UNIT_1 -c -o %t.tu1.o
// RUN: %{cxx} %{flags} %s -DTRANSLATION_UNIT_2 -c -o %t.tu2.o
// RUN: %{cxx} %{flags} %t.tu1.o %t.tu2.o -o %t.exe
// RUN:  %t.exe

#include <example.hxx>

#ifdef TRANSLATION_UNIT_1
void f() { }
#endif

#ifdef TRANSLATION_UNIT_2
extern void f();

int main() {
    f();
}
#endif
