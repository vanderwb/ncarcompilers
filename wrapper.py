#!/bin/env python
import os, sys

def compiler():
    return sys.argv[0] # can be os.path.basename(__file__)

if __name__ == "__main__":
    if sys.argv[1] == "---ncardebug-print-compiler-name":
        print compiler()