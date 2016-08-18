# -*- coding:utf8 -*-
from dbget import db_mod
import time
import unittest

class TestDb_mod(unittest.TestCase):
    def test_change_user_appserver(self):
        """testdata 为在44库预先存储完成 """
        x = db_mod()
        appserver_id = 29
        res = x.change_user_appserver("10lijie@senlime.com", appserver_id)
        print res
        self.assertEqual(str(res), str(appserver_id))

if __name__=="__main__":
    unittest.main()
