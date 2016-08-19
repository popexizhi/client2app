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
        res = self.__find_in_file(new_file)
        self.assertIn("npls_thrift_port = %s" % str(new_port), res)


    def test_change_dev_pincode(self):
        x = filewriter("alone_dev.cfg")
        email = str(time.time())
        new_pincode = "1001"
        new_file = x.change_dev_pincode(email, new_pincode)
        print "new_dev is %s" % new_file
        res = self.__find_in_file(new_file, "dev_prov_email_addr")
        self.assertIn("dev_prov_email_addr = %s" % str(email), res)
        res = self.__find_in_file(new_file, "dev_prov_pincode")
        self.assertIn("dev_prov_pincode = %s" % str(new_pincode), res)

    def __find_in_file(self, new_file, key = "npls_thrift_port"):
        f = open(new_file)
        con = f.readlines()
        f.close()
        res = ""
        for i in con:
            if re.match("#?%s" % str(key), i):
                res = i
                break
       
        print " i is %s" % str(res)
        return res

if __name__=="__main__":
    unittest.main()
