# -*- coding:utf8 -*-
from dev_c import dev_c
import time
import unittest

class TestDev_c(unittest.TestCase):
    def test_change_dev_cfg(self):
        """测试生成新的dev cfg """
        x = dev_c()
        user_mail = "%s" % str(int(time.time()))
        server_id = 29
        x.add_user(user_mail, server_id)
        x.add_dev_lic(user_mail)
        res = x.change_dev_cfg(user_mail)
        print res
        self.assertTrue(res)

    def test_add_dev_lic(self):
        """测试增加dev lic """
        x = dev_c()
        res = x.add_dev_lic("1lijie@senlime.com")
        self.assertEqual(res["result"], 0)
    
    def test_add_user(self):
        """测试增加user """
        x = dev_c()
        server_id = 28
        res = x.add_user("%s@senlime.com" % str(time.time()), server_id)
        self.assertTrue(res)

if __name__ == "__main__":
    unittest.main()
