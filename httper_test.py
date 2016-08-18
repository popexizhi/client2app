# -*- coding:utf8 -*-
from httper import httper
import time
import unittest

class TestHttper(unittest.TestCase):
    def test_login(self):
        x = httper("192.168.1.43:18080")
        res = x.login()
        assert res

    def test_register_app_server(self):
        x = httper("192.168.1.43:18080")
        x.login()
        res = x.register_app_server(url_id=3, name="9", key="57d1a7b5-5aeb-9a3e-b5bc-b37321bc83e6", serial="5a9a9bf91bc6206f00ab1a67f72bb75fe70cd4d4003ea1f28aa3eaafc5339416")
        print res
        p_res = 0
        self.assertEqual(type(p_res), type(res["result"]))

    def test_add_appserver_lic(self):
        x = httper("192.168.1.43:18080")
        res = x.add_appserver_lic(str(time.time()))
        pre_res = 0
        self.assertEqual(pre_res, res["result"])
        assert res["key"]
        assert res["serial"]
        
            
    def test_add_user(self):
        """eap /api/eap/users  接口测试"""
        x = httper("192.168.1.43:18080")
        res = x.add_user(user_mail = str(time.time()))
        pre_res = 0
        self.assertEqual(pre_res, res["result"])

    def test_add_dev_lic(self):
        """eap /api/eap/users/%d/accesskey?application_id=com.senlime.nexus.app.browser  接口测试"""
        x = httper("192.168.1.43:18080")
        res = x.add_dev_lic(2)
        pre_res = 0
        self.assertEqual(pre_res, res["result"])

if __name__=="__main__":
    unittest.main()
