import wrapper
import subprocess

def test_name():
    for name in ["./wrapper.py", "./link-to-wrapper"]:
        print name
        assert subprocess.check_output([name, "---ncardebug-print-compiler-name"]).strip() == name

def test_quotes():
    # this should work because when someone in the shell uses quotes, they are stripped by the shell and passed
    # as single argument to the wrapper which would use it as follows
    quoted_argument = "This is a filename with spaces.exe"
    assert subprocess.check_output(["./wrapper.py", "---ncardebug-print-arg", quoted_argument]).strip() == quoted_argument
