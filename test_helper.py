import unittest, inspect

# this helper needs to be a separate file from test_wrapper and
# should not include any fuction whose name starts with test

def help():
    print "**************************************************"
    print "*   WARNING: running with py.test preferred      *"
    print "*   On Yellowstone, run:                         *"
    print "*          module load python py.test            *"
    print "**************************************************"
    def my_wrapper(func):
        def wrapped(argument_to_forget):
            func()
        return wrapped

    class myTest(unittest.TestCase):
        pass

    import test_wrapper
    all_functions=inspect.getmembers(test_wrapper, inspect.isfunction)
    for func_name, func_id in all_functions:
        setattr(myTest, func_name, classmethod(my_wrapper(func_id)))

    suite = unittest.TestLoader().loadTestsFromTestCase(myTest)
    unittest.TextTestRunner().run(suite)

