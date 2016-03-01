#!/usr/bin/env python
import os, sys, subprocess

def compiler_name():
    return os.path.basename(__file__)

def include_str():
    inc = ""
    for key, value in os.environ.iteritems():
        if key.startswith('NCAR_INC_'):
            inc += "-I" + value + " "
    return inc

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
