#!/usr/bin/python3

import glob
import os
import re
import subprocess

def run(command):
    bin = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return bin.decode("ascii")

def get_repo_name():
    remote = run("git config --get remote.origin.url")
    return re.sub("\.git\s*$", "", os.path.basename(remote))

def get_repo_toplevel():
    return run("git rev-parse --show-toplevel").strip()

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

def check_repo_name(name):
    """
    [LIBRARY.NAMES]: snake_case short name
    """
    if not re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_]+[a-z0-9]$)", name):
        print(f'WARN: the name "{name}" should be snake_case')
    return True

def check_top_level_files(toplevel):
    """
    [TOPLEVEL.CMAKE]: toplevel/CMakeLists.txt exists
    [TOPLEVEL.LICENSE]: toplevel/LICENSE.txt exists
    [TOPLEVEL.README]: toplevel/LICENSE.txt exists
    """
    result = True
    for file in ["CMakeLists.txt", "LICENSE", "README.md"]:
        if not os.path.isfile(os.path.join(toplevel, file)):
            print(f'ERROR: missing top level {file}')
            result = False
    return result

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


toplevel = get_repo_toplevel()
name = get_repo_name()

if check_repo_name(name) and \
    check_top_level_files(toplevel) and \
    check_readme(os.path.join(toplevel, "README.md"), name) and \
    check_directory_layout(toplevel, name) and \
    True:
    print("all checks passed!")
