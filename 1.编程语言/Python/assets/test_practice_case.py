import unittest
import inspect

try:
    from practice_case import *
except SystemExit as e:
    pre_locals = inspect.trace()[-1][0].f_locals
    locals().update({k:v for k,v in pre_locals.items() if not k.startswith('_')})
    pass

class TestPracticeCase(unittest.TestCase):

    def test_f3(self):
        f3()
        self.assertTrue(True)