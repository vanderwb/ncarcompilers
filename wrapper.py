#!/bin/env python
import os, sys, subprocess

def compiler():
    return os.path.basename(__file__)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "---ncardebug-print-compiler-name":
            print compiler()
        if sys.argv[1] == "---ncardebug-print-arg":
            print sys.argv[2]
