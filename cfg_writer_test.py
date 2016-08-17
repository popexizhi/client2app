# -*- coding:utf8 -*-
from cfg_writer import filewriter
import time, re
import unittest

class TestCfg_writer(unittest.TestCase):
    def test_change_thrift_port(self):
        x = filewriter("alone_app.cfg")
        new_port = 1001
        new_file = x.change_thrift_port(new_port)
        print "new_file is %s" % new_file
        f = open(new_file)
        con = f.readlines()
        f.close()
        res = ""
        for i in con:
            if re.match("npls_thrift_port", i):
                res = i
                break
       
        print " i is %s" % str(res)
        self.assertIn("npls_thrift_port = %s" % str(new_port), res)

if __name__=="__main__":
    unittest.main()
