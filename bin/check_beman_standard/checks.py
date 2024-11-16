#!/usr/bin/python3

import os
import re
from .utils import *

class BemanStandardCheckBase:
    def __init__(self, name, level):
        self.name = name
        self.log_level = 'ERROR' if level == 'REQUIREMENT' else 'WARN'

    def set_repo_name(self, repo_name):
        self.repo_name = repo_name

    def set_top_level(self, top_level):
        self.top_level = top_level
        self.cmakelists_path = os.path.join(self.top_level, 'CMakeLists.txt')


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

        if is_snake_case(self.repo_name):
            return True

        # Check failed.
        self.log(f'The name "{self.repo_name}" should be snake_case')
        return False


class BemanStandardCheckTopLevel(BemanStandardCheckBase):
    def __init__(self):
        super().__init__("TOPLEVEL", "REQUIREMENT")

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

class BemanStandardCheckCMakeBase(BemanStandardCheckBase):
    def __init__(self, name, level):
        super().__init__(name, level)

    # Reads the CMakeLists.txt file and returns a string.
    def read(self, path=None, log=True):
        path = path if path is not None else self.cmakelists_path
        with open(path) as f:
            if not f:
                if log:
                    self.log(f'Missing {path} or cannot open.)')
                return None

            return f.read()


class BemanStandardCheckCMakeProjectName(BemanStandardCheckCMakeBase):
    """
    Extract project name, description, and languages considering comments everywhere.

    Example:

    project(# can have comments here and parsing should still work
        # can have comments here and parsing should still work
        beman.exemplar # can have comments here and parsing should still work
        # can have comments here and parsing should still work
        DESCRIPTION "A Beman library exemplar" # can have comments here and parsing should still work
        # can have comments here and parsing should still work
        LANGUAGES CXX # can have comments here and parsing should still work
        # can have comments here and parsing should still work
    )
    """
    def __init__(self):
        super().__init__("CMAKE.PROJECT_NAME", "REQUIREMENT")

    def check(self):
        if not super().check():
            return False

        cmakelists_content = self.read()
        if not cmakelists_content:
            return False

        # Should have project(...) in CMakeLists.txt set exactly once.
        all_matches = re.findall(r'project\((?:[^#()]*|#[^\n]*|\([^)]*\))*\)', cmakelists_content, re.DOTALL)
        # print('all:', all_matches)
        if not all_matches:
            self.log(f'Missing project(...) in CMakeLists.txt.')
            return False
        if len(all_matches) > 1:
            self.log(f'Multiple project(...) in CMakeLists.txt.')
            return False
        match = all_matches[0]

        # Get and check project name.
        print(f'Checking project name ...')
        project_name = re.search(r'beman\.([a-z0-9_]+)', match)
        if not project_name:
            self.log(f'Missing or invalid project name in CMakeLists.txt. Expected: beman.{self.repo_name}')
            return False
        project_name = project_name.group(1)
        if not is_snake_case(project_name):
            self.log(f'The project name "{project_name}" should be snake_case.')
            return False

        # Get and check project description.
        print(f'Checking project description ...')
        project_description = re.search(r'DESCRIPTION\s+"(.*?)"', match)
        if not project_description:
            self.log(f'Missing project description in CMakeLists.txt.')
            return False
        project_description = project_description.group(1)
        if len(project_description) < 10:
            self.log(f'Invalid project description "{project_description}". Too short (<10 characters).')
            return False

        # Get and check project version.
        # TODO: Darius: 2.1.1a is not valid version, but this check will pass.
        print(f'Checking project version ...')
        project_version = re.search(r'VERSION\s+((\d+\.\d+\.\d+)?)', match)
        if not project_version:
            self.log(f'Missing project version in CMakeLists.txt.')
            return False
        project_version = project_version.group(1)
        if not re.match(r'^\d+\.\d+\.\d+$', project_version):
            self.log(f'Invalid project version in CMakeLists.txt. \"{project_version}\" vs [0-9]*.[0-9]*.[0-9]*')
            return False

        # Get and check project languages.
        print(f'Checking project languages ...')
        project_languages = re.search(r'LANGUAGES\s+(.*)', match)
        if not project_languages:
            self.log(f'Missing project languages in CMakeLists.txt.')
            return False
        project_languages = project_languages.group(1).split()
        if not all(map(lambda lang: lang in ['C', 'CXX'], project_languages)):
            self.log(f'Invalid project languages "{project_languages}".')
            return False

        return True

class BemanStandardCheckCMakeSingleRule(BemanStandardCheckCMakeBase):
    def __init__(self, name, level, rule):
        super().__init__(name, level)
        self.rule = rule
    
    def check(self):
        if not super().check():
            return False

        def get_add_library_lines(path):
            cmakelists_content = self.read(path, log=False)
            if not cmakelists_content:
                return None
            all_matches = re.findall(self.rule, cmakelists_content, re.DOTALL)
            if not all_matches:
                return None
            return all_matches
        
        # Check root CMakeLists.txt.
        root_matches = get_add_library_lines(self.cmakelists_path)
        non_root_matches = get_add_library_lines(f'{self.top_level}/src/beman/{self.repo_name}/CMakeLists.txt')
        if root_matches is None and non_root_matches is None:
            self.log(f'Missing add_library(...) in CMakeLists.txt. Expected: "add_library(beman.{self.repo_name} ...)".')
            return False
        # At least one of results should be empty.
        if root_matches and non_root_matches:
            self.log(f'Multiple add_library(...) in CMakeLists.txt. Expected: "add_library(beman.{self.repo_name} ...)" in a single file.')
            return False
        match = root_matches[0] if root_matches else non_root_matches[0]
        print(f'match: {match}')

        # Get and check library name.
        print(f'Checking library name ...')
        library_name = re.search(r'beman\.([a-z0-9_]+)', match)
        if not library_name:
            self.log(f'Missing or invalid library name in CMakeLists.txt. Expected: beman.{self.repo_name}')
            return False
        library_name = f'beman.{library_name.group(1)}'
        if not is_snake_case(library_name):
            self.log(f'The library name "{library_name}" should be snake_case. Expected: beman.{self.repo_name}')
            return False
        if library_name != f'beman.{self.repo_name}':
            self.log(f'The library name "{library_name}" should match the repository name "{self.repo_name}". Expected: beman.{self.repo_name}')
            return False

        return True

class BemanStandardCheckCMakeLibraryName(BemanStandardCheckCMakeSingleRule):
    """
    Example: add_library(beman.exemplar STATIC)
    """
    def __init__(self):
        super().__init__("CMAKE.LIBRARY_NAME", "REQUIREMENT", r'add_library\((?:[^#()]*|#[^\n]*|\([^)]*\))*\)')

class BemanStandardCheckCMakeLibraryAlias(BemanStandardCheckCMakeSingleRule):
    """
    Example: add_library(beman::exemplar ALIAS beman.exemplar)
    """
    # TODO: Darius: This rule is not correct. It should be more general.
    def __init__(self):
        super().__init__("CMAKE.LIBRARY_ALIAS", "REQUIREMENT", r'add_library\(\s*([a-zA-Z_][a-zA-Z0-9_:]*)\s+ALIAS\s+\1\)')
