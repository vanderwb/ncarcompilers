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
    env = os.environ
    name = 'NCAR_INC_FOO'
    env[name] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'
    assert not "-I" + env[name] in results
    results = wrapper.include_str() # after the env var is set
    assert "-I" + env[name] in results
    del env[name]

def test_multiple_includes():
    env = os.environ
    name_foo = 'NCAR_INC_FOO'
    name_bar = 'NCAR_INC_BAR'
    env[name_foo] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'
    env[name_bar] = '/glade/apps/opt/bar/7.8.9/intel/10.11.12/include'
    results = wrapper.include_str() # after the env var is set
    assert "-I" + env[name_foo] in results
    assert "-I" + env[name_bar] in results
    # maybe should check also the space in between, but that's too much logic for a unit test
    del env[name_foo]
    del env[name_bar]

def test_single_ldflag():
    name = 'NCAR_LDFLAGS_FOO'
    results = wrapper.ldflags_str() # before the env var is set
    env = os.environ
    env[name] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/lib'
    assert not "-L" + env[name] in results
    results = wrapper.ldflags_str() # after the env var is set
    assert "-L" + env[name] in results
    del env[name]

# no need to test multiple ldflags, since the code exercising this is exactly the same for multiple includes
# def test_multiple_ldflags:
#    pass

def test_single_rpath():
    RPATH_FLAG = "-Wl,-rpath," # this depends on the compiler and it is so for gcc and intel, will add pgi later
    name = 'NCAR_LDFLAGS_FOO'
    results = wrapper.rpath_str() # before the env var is set
    env = os.environ
    env[name] = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/lib'
    assert not RPATH_FLAG + env[name] in results
    results = wrapper.rpath_str() # after the env var is set
    assert RPATH_FLAG + env[name] in results
    del env[name]

def test_single_linklib():
    name = 'NCAR_LIBS_FOO'
    results = wrapper.linklib_str() # before the env var is set
    env = os.environ
    env[name] = '-lfooc -lfoof -lfoo'
    assert not env[name] in results
    results = wrapper.linklib_str() # after the env var is set
    assert env[name] in results
    del env[name]

if __name__ == "__main__":
    import test_helper
    test_helper.help()
