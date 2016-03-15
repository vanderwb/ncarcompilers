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

def test_remove_current_directory():
    wrapper_path = os.path.dirname(os.path.realpath(__file__))

    # the following is platform independent but it is too cryptic for my like of unit tests
    # mypath = wrapper_path + os.pathsep + os.path.join("one", "of", "my", "paths") + os.pathsep + os.path.join("some", "other", "path")

    mypath = wrapper_path + ":/one/of/my/paths:/some/other/path"             # at the beginning (most important)
    assert wrapper.remove_current_directory(mypath) == "/one/of/my/paths:/some/other/path"

    mypath = "/one/of/my/paths:/some/other/path:" + wrapper_path             # at the end (almost irrelevant, besides to avoid recursion when the actual compiler is missing)
    assert wrapper.remove_current_directory(mypath) == "/one/of/my/paths:/some/other/path"

    mypath = "/one/of/my/paths:" + wrapper_path  + ":/some/other/path"             # in the middle, still important
    assert wrapper.remove_current_directory(mypath) == "/one/of/my/paths:/some/other/path"

def test_quotes():
    quoted_argument = "This is a filename with spaces.exe"
    assert check_output(["./wrapper.py", "---ncardebug-print-arg", quoted_argument]) == quoted_argument

def test_callexternal():
    results = check_output(["./gcc", "--version"])
    assert "Free Software Foundation" in results

def test_single_include():
    name = 'NCAR_INC_FOO'
    value = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'

    env = os.environ
    env.pop(name, None)
    results = wrapper.include_str() # without the env var
    assert not "-I" + value in results

    env[name] = value
    results = wrapper.include_str() # with the env var
    assert "-I" + value in results
    del env[name]

def test_multiple_includes():
    name_foo = 'NCAR_INC_FOO'
    name_bar = 'NCAR_INC_BAR'
    value_foo = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'
    value_bar = '/glade/apps/opt/bar/7.8.9/intel/10.11.12/include'

    env = os.environ
    env[name_foo] = value_foo
    env[name_bar] = value_bar 

    results = wrapper.include_str() # with the env var
    assert "-I" + env[name_foo] in results
    assert "-I" + env[name_bar] in results
    # maybe should check also the space in between, but that's too much logic for a unit test
    del env[name_foo]
    del env[name_bar]

def test_multiple_includes_together():
    name = 'NCAR_INC_FOO'
    value_foo = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/include'
    value_bar = '/glade/apps/opt/bar/7.8.9/intel/10.11.12/include'

    env = os.environ
    env.pop(name, None)
    results = wrapper.include_str() # without the env var
    assert not "-I" + value_foo in results
    assert not "-I" + value_bar in results

    env[name] = value_foo + ":" + value_bar
    results = wrapper.include_str() # with the env var
    assert "-I" + value_foo in results
    assert "-I" + value_bar in results
    del env[name]

def test_single_ldflag():
    name = 'NCAR_LDFLAGS_FOO'
    value = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/lib'

    env = os.environ
    env.pop(name, None)
    results = wrapper.ldflags_str() # without the env var
    assert not "-L" + value in results

    env[name] = value
    results = wrapper.ldflags_str() # with the env var
    assert "-L" + value in results
    del env[name]

# no need to test multiple ldflags, since the code exercising this is exactly the same for multiple includes
# def test_multiple_ldflags:
#    pass

def test_single_rpath():
    RPATH_FLAG = "-Wl,-rpath," # this depends on the compiler and it is so for gcc and intel, will add pgi later
    name = 'NCAR_LDFLAGS_FOO'
    value = '/glade/apps/opt/foo/1.2.3/gcc/3.4.5/lib'

    env = os.environ
    env.pop(name, None)
    results = wrapper.rpath_str() # without the env var
    assert not RPATH_FLAG + value in results

    env[name] = value
    results = wrapper.rpath_str() # with the env var set
    assert RPATH_FLAG + value in results
    del env[name]

def test_single_linklib():
    name = 'NCAR_LIBS_FOO'
    value = '-lfooc -lfoof -lfoo'

    env = os.environ
    env.pop(name, None)
    results = wrapper.linklib_str() # without the env var
    assert not value in results

    env[name] = value
    results = wrapper.linklib_str() # with the env var set
    assert value in results
    del env[name]

def test_overriding_linklibs():
    name_foo = 'NCAR_LIBS_FOO'
    name_bar = 'NCAR_LIBS_BAR'
    value_foo = '-lfooc -lfoof -lfoo'
    value_bar = '-lbar'

    env = os.environ
    env[name_foo] = value_foo
    env[name_bar] = value_bar
    results = wrapper.linklib_str()
    assert value_foo in results
    assert value_bar in results

    env['NCAR_EXCLUDE_LIBS'] = "1"
    results = wrapper.linklib_str()
    assert not value_foo in results
    assert not value_bar in results

    env['NCAR_EXCLUDE_LIBS'] = "False"
    results = wrapper.linklib_str()
    assert not value_foo in results
    assert not value_bar in results

    del env['NCAR_EXCLUDE_LIBS']
    results = wrapper.linklib_str()
    assert value_foo in results
    assert value_bar in results
    del env[name_foo]
    del env[name_bar]

def test_clean_arguments():
    cli_args = ["-lfoo", "-lnetcdff", "-lbar"]      # command line arguments come as a list
    from_modules = "-Bstatic -lnetcdff -Bdynamic"   # module arguments come as a string
    expected_args = ["-lfoo", "-lbar"]              # it needs to remove the duplicate one
    actual_args = wrapper.clean_arguments(cli_args, from_modules)
    assert actual_args == expected_args

if __name__ == "__main__":
    import test_helper
    test_helper.help()
