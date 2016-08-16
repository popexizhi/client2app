# -*- coding:utf8 -*-
from httper import httper
import time
import unittest

class TestHttper(unittest.TestCase):
        def test_login(self):
            x = httper()
            cookie = x.login()
            assert cookie

if __name__=="__main__":
    unittest.main()
