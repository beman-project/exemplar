#!/usr/bin/python3

import os
import re

class BemanStandardCheckBase:
    def __init__(self, name, level):
        self.name = name
        self.log_level = 'ERROR' if level == 'REQUIREMENT' else 'WARN'

    def set_repo_name(self, repo_name):
        self.repo_name = repo_name

    def set_top_level(self, top_level):
        self.top_level = top_level

    # Checks if the Beman Standard is already applied.
    # - If the standard is applied, the check should return True.
    # - If the standard is not applied, the check should return False and self.fix() should be able to fix the issue.
    def check(self):
        if self.name is None:
            self.log('The name is not set.')
            return False
        
        if self.repo_name is None:
            self.log('The repo_name is not set.')
            return False

        if self.top_level is None:
            self.log('The top_level is not set.')
            return False

        return True

    # Fixes the issue if the standard is not applied.
    # - If the standard is applied, the check should return True.
    # - Otherwise, the check should be applied inplace. If the check cannot be applied inplace, the check should return False.
    def fix(self):
        print(f'{self.log_level} [{self.name}]: Fixing the issue - N/A!!!')
        return True

    # Logs a message with the check's log level.
    # e.g. WARN REPOSITORY.NAME: The name "${name}" should be snake_case.'
    # e.g. ERROR TOPLEVEL.CMAKE: Missing top level CMakeLists.txt.'
    def log(self, message):
        print(f'{self.log_level} [{self.name}]: {message}')  


class BemanStandardCheckRepoName(BemanStandardCheckBase):
    def __init__(self):
        super().__init__("REPOSITORY.NAME", "RECOMMENDATION")

    def check(self):
        """
        [REPOSITORY.NAME] RECOMMENDATION: The repository should be named after the library name excluding the `beman.` prefix.
        Examples: A beman.smart_pointer library's repository should be named smart_pointer.
        """
        if not super().check():
            return False

        if re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_]+[a-z0-9]$)", self.repo_name):
            return True

        # Check failed.
        self.log(f'The name "{self.repo_name}" should be snake_case')
        return False


class BemanStandardCheckTopLevel(BemanStandardCheckBase):
    def __init__(self):
        super().__init__("REPOSITORY.NAME", "REQUIREMENT")

    def check(self):
        """
        The top-level of a Beman library repository must consist of CMakeLists.txt, LICENSE, and README.md files.

        [TOPLEVEL.CMAKE] REQUIREMENT: There must be a CMakeLists.txt file at the repository's root that builds and tests (via. CTest) the library.

        [TOPLEVEL.LICENSE] REQUIREMENT: There must be a LICENSE file at the repository's root with the contents of an approved license that covers the contents of the repository.

        [TOPLEVEL.README] REQUIREMENT: There must be a markdown-formatted README.md file at the repository's root that describes the library, explains how to build it, and links to further documentation.
        """
        if not super().check():
            return False

        def check_file(file):
            if os.path.isfile(os.path.join(self.top_level, file)):
                return True

            self.log(f'Missing top level {file}')
            return False

        top_level_files = ['CMakeLists.txt', 'LICENSE', 'README.md']
        return all(map(check_file, top_level_files))
