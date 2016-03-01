import wrapper
import subprocess

def check_output(cmd):
    return subprocess.check_output(subprocess.list2cmdline(cmd), shell=True).strip()

def test_name():
    for name in ["wrapper.py", "link-to-wrapper", "gcc"]:
        print name
        assert check_output(["./" + name, "---ncardebug-print-compiler-name"]) == name

def test_quotes():
    quoted_argument = "This is a filename with spaces.exe"
    assert check_output(["./wrapper.py", "---ncardebug-print-arg", quoted_argument]) == quoted_argument

def test_callexternal():
    results = check_output(["./gcc", "--version"])
    assert "Free Software Foundation" in results

if __name__ == "__main__":
    import unittest
    def my_wrapper(func):
        def wrapped(argument_to_forget):
            func()
        return wrapped

    class myTest(unittest.TestCase):
        pass

    setattr(myTest, "test_name", classmethod(my_wrapper(test_name)))
    #myTest.test_name = my_wrapper(test_name)
 #   a = myTest()
  #  print a.test_name
   # print a.test_name()

    unittest.main()
