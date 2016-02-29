#!/bin/env python
import os, sys

if __name__ == "__main__":
    if sys.argv[1] == "---debug-ncar-wrapper":
        #print "OS way", os.path.basename(__file__)
        print sys.argv[0]
