# -*- coding:utf8 -*-
from dev_c import dev_c
import time
import unittest
import err

class TestDev_c(unittest.TestCase):
    def test_dev_provision(self):
        """ 
        测试dev provision 流程
        """
        x = dev_c()
        user_mail = "%s" % str(int(time.time()))
        server_id = 29
        res = x.dev_provision(user_mail, server_id)
        #assert res

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
    def test_start_dev(self):
        """测试启动devprovision """
        x = dev_c()
        res = x.start_dev("alone_dev.cfg")
        self.assertNotEqual(res, None)
    
    def test_try_dev_provision(self):
        """
        test try dev_provision
        1. test eap_provision_server err
        2. test dev path err
        3. 
        """
        #1
        x =  dev_c(eap_ip = "1.1.1.1")
        res = x.try_dev_provision()
        print "*" * 20
        print res
        #2
#        x =  dev_c()
#        res = x.try_dev_provision()
#        print "*" * 20
#        print res

if __name__ == "__main__":
    unittest.main()
