import unittest

from . Exe import exe

class ExeTest(unittest.TestCase):
    def exe(self, x):
        def maker(name, *args, **kwds):
            return name, args, kwds
        return exe(x, maker)

    def test_trivial(self):
        self.assertEquals(exe(None), None)

    def test_simple(self):
        self.assertEquals(self.exe('test'), ('test', (), {}))
