# -*- coding:utf8 -*-
from dbget import db_mod
import time
import unittest

class TestDb_mod(unittest.TestCase):

    def test_get_dev_pin_for_last(self):
        """testdata 为在44库预先存储完成i,
            bug fix:adduser后系统默认生成一个pincode，修改server_id后使用接口生成的为第二个dev_code,测试get_dev_code为最后一个添加内容
        """
        x = db_mod()
        email_two_code = "1471933191"
        res = x.get_dev_pin(email_two_code)[0]
        print res
        self.assertEqual(str(res), "72a1baa67b7e")
    
    def test_change_user_appserver(self):
        """testdata 为在44库预先存储完成 """
        x = db_mod()
        appserver_id = 29
        res = x.change_user_appserver("10lijie@senlime.com", appserver_id)
        print res
        self.assertEqual(str(res), str(appserver_id))
    def test_get_dev_user_id(self):
        """testdata 10lijie@senlime.com user_id = 2 在44库存储完成  """
        x = db_mod()
        res = x.get_dev_user_id("10lijie@senlime.com")
        self.assertEqual(res, 2)

    def test_get_dev_pin(self):
        """testdata 10lijie@senlime.com  在44库存储完成  """
        x = db_mod()
        res = x.get_dev_pin("10lijie@senlime.com")
        print res
        self.assertEqual(len(res), 1)

if __name__=="__main__":
    unittest.main()
