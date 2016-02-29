import wrapper
import subprocess

def test_name():
    for name in ["./wrapper.py", "./link-to-wrapper"]:
        print name
        assert subprocess.check_output([name, "---debug-ncar-wrapper"]).strip() == name
