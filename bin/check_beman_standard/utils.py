#!/usr/bin/python3

import subprocess
import os
import re

def run(command):
    bin = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return bin.decode("ascii")

def run_check(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).wait()

class Git:
    def __init__(self):
        pass

    def has_uncommited_changes(self):
        return run_check("git diff --quiet HEAD")

    def add(self, file):
        run(f"git add {file}")

    def get_repo_name(self):
        remote = run("git config --get remote.origin.url")
        return re.sub("\.git\s*$", "", os.path.basename(remote))

    def get_repo_toplevel(self):
        return run("git rev-parse --show-toplevel").strip()


git = Git()


def is_snake_case(name):
    return re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_.]+[a-z0-9]$)", name)
