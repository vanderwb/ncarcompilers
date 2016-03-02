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

def rpath_str():
    return create_str(parse_env = 'NCAR_LDFLAGS_', joinwith='-Wl,-rpath,')

def linklib_str():
    try:
        os.environ['NCAR_EXCLUDE_LIBS']
        return ""
    except:
        return create_str(parse_env = 'NCAR_LIBS_', joinwith='')

def invoke(show):
    compiler_name_with_path = subprocess.check_output("which " + compiler_name(), shell=True).strip()
    cmd = ( subprocess.list2cmdline([compiler_name_with_path] + sys.argv[1:]) + " " +
           include_str() + " "  + ldflags_str() + " " + rpath_str() + " " + linklib_str() )
    if show:
        print cmd
    else:
        subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    show = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "---ncardebug-print-compiler-name":
            print compiler_name()
            sys.exit(0)
        if sys.argv[1] == "---ncardebug-print-arg":
            print sys.argv[2]
            sys.exit(0)
        if sys.argv[1] == "--show":
            show = True
    invoke(show)
