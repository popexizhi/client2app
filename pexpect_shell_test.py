# -*- coding:utf8 -*-
from pexpect_shell import sh_pex
import time
import unittest
import threading
import err

class TestSh_pex(unittest.TestCase):
    def test_start_dev(self):
        x = sh_pex()
        res = x.start_dev()
        self.assertNotEqual(res, None)
    def test_start_appserver(self):
        x = sh_pex()
        res = x.start_appserver()
        self.assertNotEqual(res, None)
    
    def test_get_args(self):
        "test get_args"        
        x = sh_pex()
        res = x.get_args(["-db", "-server_provision"])
        p_res = " -db -server_provision" 
        self.assertEqual(res, p_res)
    def Nonetest_wait_app_client_num(self):
        """ 
        test wait_app_client_num
        """
        td_path = "testdata/pexpect_use/101459"
        app_p = "../../../app_server"
        dev_p = "../../../slim_engine_test"
        app_cfg = "alone_app.cfg"
        dev_cfg = "alone_dev.cfg"

        x = sh_pex()
        #threading.Thread(target=x.start_appserver, args=(app_p, app_cfg, [], td_path))
        x.start_appserver(app_p, app_cfg, [], td_path)
        time.sleep(3)
        d = sh_pex()
        s1 = threading.Thread(target=d.start_dev, args =(dev_p, dev_cfg, [], ))
        s1.start()
        res = x.wait_app_client_num(dev_num = 1)
        self.assertNotEqual(res, None)
    def test_start_app_path_err(self):
        """ 
        test wait_app_client_num
        """
        app_p = "../../../app_server"
        app_cfg = "alone_app.cfg"

        x = sh_pex()
        try:
            x.start_appserver(app_p, app_cfg, [])
        except err.ProvisionError as e:
            print "[err.ProvisionError] %s"% str(e)
            self.assertEqual(e, e)

if __name__=="__main__":
    unittest.main() 
