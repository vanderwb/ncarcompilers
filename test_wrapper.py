import subprocess, os
import wrapper

def check_output(cmd):
    return subprocess.check_output(subprocess.list2cmdline(cmd), shell=True).strip()

def test_name():
    list_to_test = ["wrapper.py"]
    for myfile in os.listdir("./"):
        if os.path.islink(myfile):
            list_to_test.append(myfile)
    for name in list_to_test:
        print name
        assert check_output(["./" + name, "---ncardebug-print-compiler-name"]) == name

def test_quotes():
    quoted_argument = "This is a filename with spaces.exe"
    assert check_output(["./wrapper.py", "---ncardebug-print-arg", quoted_argument]) == quoted_argument

def test_callexternal():
    results = check_output(["./gcc", "--version"])
    assert "Free Software Foundation" in results

def test_single_include():
    results = wrapper.include_str() # before the env var is set
    env = os.environ;
    env['NCAR_INC_FOO'] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'
    assert not "-I" + env['NCAR_INC_FOO'] in results
    results = wrapper.include_str() # after the env var is set
    assert "-I" + env['NCAR_INC_FOO'] in results
    del env['NCAR_INC_FOO']

def test_multiple_includes():
    env = os.environ;
    env['NCAR_INC_FOO'] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'
    env['NCAR_INC_BAR'] = '/glade/apps/opt/bar/7.8.9/intel/10.11.12/include'
    results = wrapper.include_str() # after the env var is set
    assert "-I" + env['NCAR_INC_FOO'] in results
    assert "-I" + env['NCAR_INC_BAR'] in results
    # maybe should check also the space in between, but that's too much logic for a unit test
    del env['NCAR_INC_FOO']
    del env['NCAR_INC_BAR']

def test_single_ldflag():
    results = wrapper.ldflags_str() # before the env var is set
    env = os.environ;
    env['NCAR_LDFLAGS_FOO'] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/lib'
    assert not "-L" + env['NCAR_LDFLAGS_FOO'] in results
    results = wrapper.ldflags_str() # after the env var is set
    assert "-L" + env['NCAR_LDFLAGS_FOO'] in results
    del env['NCAR_LDFLAGS_FOO']

# no need to test multiple ldflags, since the code exercising this is exactly the same for multiple includes
# def test_multiple_ldflags:
#    pass

def test_single_rpath():
    RPATH_FLAG = "-Wl,-rpath," # this depends on the compiler and it is so for gcc and intel, will add pgi later
    results = wrapper.rpath_str() # before the env var is set
    env = os.environ;
    env['NCAR_LDFLAGS_FOO'] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/lib'
    assert not RPATH_FLAG + env['NCAR_LDFLAGS_FOO'] in results
    results = wrapper.rpath_str() # after the env var is set
    assert RPATH_FLAG + env['NCAR_LDFLAGS_FOO'] in results
    del env['NCAR_LDFLAGS_FOO']

def test_single_linklib():
    results = wrapper.linklib_str() # before the env var is set
    env = os.environ;
    env['NCAR_LIBS_FOO'] = '-lfooc -lfoof -lfoo'
    assert not env['NCAR_LIBS_FOO'] in results
    results = wrapper.linklib_str() # after the env var is set
    assert env['NCAR_LIBS_FOO'] in results
    del env['NCAR_LIBS_FOO']

if __name__ == "__main__":
    import test_helper
    test_helper.help()
