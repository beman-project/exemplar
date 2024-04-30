import lit
import os
import re

def _parseScript(test, preamble):
    """
    Extract the script from a test, with substitutions applied.

    Returns a list of commands ready to be executed.

    - test
        The lit.Test to parse.

    - preamble
        A list of commands to perform before any command in the test.
        These commands can contain unexpanded substitutions, but they
        must not be of the form 'RUN:' -- they must be proper commands
        once substituted.
    """
    # Get the default substitutions
    tmpDir, tmpBase = lit.TestRunner.getTempPaths(test)
    substitutions = lit.TestRunner.getDefaultSubstitutions(test, tmpDir, tmpBase)

    # Parse the test file, including custom directives
    scriptInTest = lit.TestRunner.parseIntegratedTestScript(test, require_script=not preamble)
    if isinstance(scriptInTest, lit.Test.Result):
        return scriptInTest

    script = preamble + scriptInTest
    return lit.TestRunner.applySubstitutions(script, substitutions, recursion_limit=10)

class CxxStandardLibraryTest(lit.formats.FileBasedTest):
    def getTestsForPath(self, testSuite, pathInSuite, litConfig, localConfig):
        SUPPORTED_SUFFIXES = [
            "[.]pass[.]cpp$",
            "[.]compile[.]pass[.]cpp$",
            "[.]sh[.][^.]+$",
            "[.]verify[.]cpp$",
        ]

        sourcePath = testSuite.getSourcePath(pathInSuite)
        filename = os.path.basename(sourcePath)

        # Ignore dot files, excluded tests and tests with an unsupported suffix
        hasSupportedSuffix = lambda f: any([re.search(ext, f) for ext in SUPPORTED_SUFFIXES])
        if filename.startswith(".") or filename in localConfig.excludes or not hasSupportedSuffix(filename):
            return

        yield lit.Test.Test(testSuite, pathInSuite, localConfig)

    def execute(self, test, litConfig):
        supportsVerify = "verify-support" in test.config.available_features
        filename = test.path_in_suite[-1]

        if re.search("[.]sh[.][^.]+$", filename):
            steps = []  # The steps are already in the script
            return self._executeShTest(test, litConfig, steps)
        elif filename.endswith(".compile.pass.cpp"):
            steps = ["%dbg(COMPILED WITH) %{cxx} %s %{flags} -fsyntax-only"]
            return self._executeShTest(test, litConfig, steps)
        elif filename.endswith(".verify.cpp"):
            if not supportsVerify:
                return lit.Test.Result(
                    lit.Test.UNSUPPORTED,
                    "Test {} requires support for Clang-verify, which isn't supported by the compiler".format(test.getFullName()),
                )
            steps = ["%dbg(COMPILED WITH) %{cxx} %s %{flags} -fsyntax-only -Xclang -verify -Xclang -verify-ignore-unexpected=note -ferror-limit=0"]
            return self._executeShTest(test, litConfig, steps)
        elif filename.endswith(".pass.cpp"):
            steps = [
                "%dbg(COMPILED WITH) %{cxx} %s %{flags} -o %t.exe",
                "%dbg(EXECUTED AS) %t.exe",
            ]
            return self._executeShTest(test, litConfig, steps)
        else:
            return lit.Test.Result(lit.Test.UNRESOLVED, "Unknown test suffix for '{}'".format(filename))

    def _executeShTest(self, test, litConfig, steps):
        if test.config.unsupported:
            return lit.Test.Result(lit.Test.UNSUPPORTED, "Test is unsupported")

        script = _parseScript(test, steps)
        if isinstance(script, lit.Test.Result):
            return script

        if litConfig.noExecute:
            return lit.Test.Result(lit.Test.XFAIL if test.isExpectedToFail() else lit.Test.PASS)
        else:
            _, tmpBase = lit.TestRunner.getTempPaths(test)
            useExternalSh = False
            return lit.TestRunner._runShTest(test, litConfig, useExternalSh, script, tmpBase)
