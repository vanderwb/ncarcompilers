#!/usr/bin/env python
import os, sys, subprocess

def compiler():
    return os.path.basename(__file__)

def invoke():
    my_path = subprocess.check_output("which " + compiler(), shell=True).strip()
    subprocess.call([my_path] + sys.argv[1:])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "---ncardebug-print-compiler-name":
            print compiler()
            sys.exit(0)
        if sys.argv[1] == "---ncardebug-print-arg":
            print sys.argv[2]
            sys.exit(0)
    invoke()
