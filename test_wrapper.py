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

if __name__ == "__main__":
    import test_helper
    test_helper.help()
