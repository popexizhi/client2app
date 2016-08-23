# -*- coding:utf8 -*-
from pexpect_shell import sh_pex
import time
import unittest
import threading

class TestSh_pex(unittest.TestCase):
    def test_start_appserver(self):
        x = sh_pex()
        res = x.start_dev()
        self.assertNotEqual(res, None)
    def test_start_dev(self):
        x = sh_pex()
        res = x.start_appserver()
        self.assertNotEqual(res, None)
    
    def test_get_args(self):
        "test get_args"        
        x = sh_pex()
        res = x.get_args(["-db", "-server_provision"])
        p_res = " -db -server_provision" 
        self.assertEqual(res, p_res)

if __name__=="__main__":
    unittest.main() 
