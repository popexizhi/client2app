# -*- encoding=utf8 -*-
from logMoner import logMon
import unittest
from datetime import datetime

class logMonerTestCase(unittest.TestCase):
    def test_get_datatime(self):
        print "test_get_datatime"
        x = logMon()
        td = "[2016/05/03/18/10/51/281:195]"
        pre_t = datetime(2016,05,03,18,10,51,281195)
        res = x._get_datatime(td)
        self.assertEqual(pre_t, res)


if __name__ == "__main__":
    unittest.main()
