#!/usr/bin/env python
import os, sys, subprocess, filecmp
from collections import OrderedDict

def compiler_name():
    return os.path.basename(__file__)

def remove_current_directory(s):
    wrapper_path = os.path.dirname(os.path.realpath(__file__))
    ss = s.replace(wrapper_path, "").replace(os.pathsep + os.pathsep, os.pathsep)
    return ss.strip(os.pathsep)

def create_str(parse_env=None, joinwith=""):
    myenv = os.environ.copy()
    unsorted_libs = {}
    for key, values in myenv.iteritems():
        if key.startswith(parse_env):
            lib_name = key.split("_")[-1]
            try:
                rank = int(myenv['NCAR_RANK_' + lib_name])
            except KeyError:
                rank = 0
            unsorted_libs[lib_name] = (rank, values)

    sorted_libs = OrderedDict(sorted(unsorted_libs.items(), key=lambda t: t[1][0]))
    inc = ""
    for values in sorted_libs.itervalues():
        for value in values[1].split(os.pathsep):
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

def asneeded_str():
    try:
        os.environ['NCAR_EXCLUDE_ASNEEDED']
        return ""
    except:
        return "-Wl,--as-needed"

def compiler_name_with_path():
    myenv = os.environ.copy()
    myenv["PATH"] = remove_current_directory(myenv["PATH"])
    full_name = subprocess.check_output("which " + compiler_name(), env = myenv, shell=True).strip()
    return full_name

def avoid_recursion():
    avoid_recursion_env_var = "NCAR_COMPILER_PATH_RECURSION"
    myenv = os.environ.copy()
    try:
        foo = myenv[avoid_recursion_env_var]
        if filecmp.cmp(__file__, compiler_name_with_path()):
            print "Compiler recursion detected: ", compiler_name_with_path()
            sys.exit(1)
    except KeyError:
        pass

    myenv[avoid_recursion_env_var] = "1"
    return myenv

def clean_arguments(args, duplicates):
    clean_args = []
    tbr = [d for d in duplicates.split(" ") if d.startswith("-l")]    # stuff to be removed, only -lsomething, ignoring duplicates in tbr itself 
    for arg in args:
        if not arg in tbr:
            clean_args.append(arg)

    return clean_args

def invoke(show):
    ncar_linklib = linklib_str()
    arguments = clean_arguments(sys.argv[1:], ncar_linklib)
    cmd = ( subprocess.list2cmdline([compiler_name_with_path()] + arguments) + " " +
           include_str() + " "  + ldflags_str() + " " + rpath_str() + " " + 
           asneeded_str() + " " + ncar_linklib )
    if show:
        print cmd
    else:
        subprocess.call(cmd, env=avoid_recursion(), shell=True)

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
