import os
import unittest


def run_test():
    loader = unittest.TestLoader()
    tests_path = os.path.join(r'.')
    tests = loader.discover(tests_path, pattern='*Test.py')
    unittest.TextTestRunner(verbosity=0).run(tests)


if __name__ == "__main__":
    run_test()
