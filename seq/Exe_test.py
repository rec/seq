import unittest

from . Exe import exe

class ExeTest(unittest.TestCase):
    def test_simple(self):
        self.assertEquals(exe(None), None)
