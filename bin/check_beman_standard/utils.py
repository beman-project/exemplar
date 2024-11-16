#!/usr/bin/python3

import subprocess
import os
import re

def run(command):
    bin = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    return bin.decode("ascii")

def run_check(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).wait()

def get_repo_name():
    remote = run("git config --get remote.origin.url")
    return re.sub("\.git\s*$", "", os.path.basename(remote))

def get_repo_toplevel():
    return run("git rev-parse --show-toplevel").strip()

def is_snake_case(name):
    return re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_.]+[a-z0-9]$)", name)
