#!/usr/bin/python3

import glob
import os
import re
import argparse

from check_beman_standard.checks import *
from check_beman_standard.utils import *

def skip_md_header(lines):
    index = 0
    empty_re = re.compile("^\s*$")
    comment_start = re.compile("^\s*<!--")
    comment_end = re.compile("-->")
    while index < len(lines):
        if empty_re.match(lines[index]):
            pass
        elif comment_start.match(lines[index]):
            while not comment_end.match(lines[index]):
                index += 1
        else:
            break
        index += 1

    return lines[index:]

def check_readme(readme, name):
    """
    [README.TITLE]: the first line is the title
    [README.IMPLEMENTS]: there should be a mention of at least one paper
    """
    with open(readme) as file:
        lines = [line.rstrip() for line in file]
        lines = skip_md_header(lines)
        if len(lines) == 0:
            print(f'ERROR: the file {readme} is empty (or only contains comments or spaces)')
            return False

        if not re.match(f"# beman.{name}", lines[0]):
            print(f'WARN: the README.md title should mention the library name "{lines[0]}"')

        has_implements = False
        ref_re = re.compile(".*https://wg21.link/P[0-9]*.*")
        for line in lines:
            if ref_re.match(line):
                has_implements = True
        if not has_implements:
            print(f'WARN: the README.md should mention at least on paper')
    return True

def check_directory_layout(toplevel, name):
    """
    [DIRECTORY.INTERFACE_HEADERS]: headers are in include/beman/<name>
    """
    result = True
    include_path = os.path.join(toplevel, "include", "beman", name)
    if not os.path.isdir(include_path):
        print(f'ERROR: there needs to be an include path "{include_path}"')
        result = False
    elif 0 == len(glob.glob(os.path.join(include_path, "*.hpp"))):
        print(f'ERROR: there needs to be at least on header ("*.hpp")')
        result = False

    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", help="fix fixable problems", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    toplevel = git.get_repo_toplevel()
    repo_name = git.get_repo_name()
    print(f"Checking {repo_name} at {toplevel}")

    # Apply the [Beman Standard](https://github.com/beman-project/beman/blob/main/docs/BEMAN_STANDARD.md).
    # Manually update this list as you add checks:
    checks = [
        ## License
        # LICENSE.APPROVED
        # LICENSE.APACHE_LLVM
        # LICENSE.CRITERIA

        ## General
        # LIBRARY.NAMES
        # REPOSITORY.NAME
        BemanStandardCheckRepoName(),
        # REPOSITORY.CODEOWNERS

        ## Top-level
        BemanStandardCheckCmakeExists(), # TOPLEVEL.CMAKE
        BemanStandardCheckLicenseExists(), # TOPLEVEL.LICENSE
        BemanStandardCheckReadmeExists(), # TOPLEVEL.README

        ## README.md
        BemanStandardCheckReadmeTitle(), # README.TITLE
        # README.PURPOSE
        BemanStandardCheckReadmeImplements(), # README.IMPLEMENTS

        ## CMake
        # CMAKE.DEFAULT
        # TODO: Darius: actually check the CMakeLists.txt.
        # CMAKE.PROJECT_NAME
        BemanStandardCheckCMakeProjectName(),
        # CMAKE.LIBRARY_NAME
        BemanStandardCheckCMakeLibraryName(),
        # CMAKE.LIBRARY_ALIAS
        BemanStandardCheckCMakeLibraryAlias(),
        # CMAKE.TARGET_NAMES
        # CMAKE.CONFIG
        # CMAKE.SKIP_TESTS
        # CMAKE.SKIP_EXAMPLES
        # CMAKE.AVOID_PASSTHROUGHS

        ## Directory Layout
        # DIRECTORY.INTERFACE_HEADERS
        # DIRECTORY.IMPLEMENTATION_HEADERS
        # DIRECTORY.SOURCES
        # DIRECTORY.TESTS
        # DIRECTORY.EXAMPLES
        # DIRECTORY.DOCS
        # DIRECTORY.PAPERS

        ## File contents
        # FILE.NAME
        # FILE.TEST_NAMES
        # FILE.LICENSE_ID
        # FILE.COPYRIGHT

        ## C++
        # CPP.NAMESPACE
    ]
    # Append dynamic values to the checks.
    for check in checks:
        check.set_repo_name(repo_name)
        check.set_top_level(toplevel)

    # Actually run the checks
    fix_inplace = args.fix == True
    if fix_inplace and git.has_uncommited_changes():
        print("ERROR: there are uncommited changes and a request for fixes.")
        print("    Please commit the changes before running the checks with fixes.")
        return

    for check in checks:
        print(f'CHECK {check.name} ++')
        if not check.check() and fix_inplace and check.fix():
            print(f"      [{check.name}] fixed")
        print(f'CHECK {check.name} --\n\n\n')

if __name__ == "__main__":
    main()
