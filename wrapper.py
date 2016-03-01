#!/usr/bin/env python
import os, sys, subprocess

def compiler_name():
    return os.path.basename(__file__)

def create_str(parse_env=None, joinwith=""):
    inc = ""
    for key, value in os.environ.iteritems():
        if key.startswith(parse_env):
            inc += joinwith + value + " "
    return inc

def include_str():
    return create_str(parse_env = 'NCAR_INC_', joinwith='-I')

def ldflags_str():
    return create_str(parse_env = 'NCAR_LDFLAGS_', joinwith='-L')

def invoke():
    compiler_name_with_path = subprocess.check_output("which " + compiler_name(), shell=True).strip()
    subprocess.call([compiler_name_with_path] + sys.argv[1:]) # this should use shell

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "---ncardebug-print-compiler-name":
            print compiler_name()
            sys.exit(0)
        if sys.argv[1] == "---ncardebug-print-arg":
            print sys.argv[2]
            sys.exit(0)
    invoke()
