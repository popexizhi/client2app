# -*- coding:utf8 -*-
import re, os
import sqlite3
from db_check import db_check
import unittest
import os

class Test_db_check(unittest.TestCase):

    def test_db_save(self):
        pa = "testcase//"
        tar_pa = "testcaseback//"
        os.system("rm -r %s" % tar_pa)

        x = db_check()
        res = x.db_save(pa, tar_pa)
        self.assertEqual(res,12)
    def test_get_all_db(self):
        db_pa = "testcase"
        x = db_check()
        res = x.get_all_db(db_pa)
        self.assertEqual(len(res), 12)

    def test_save_ue_db(self):    
        db_path = "testcase//npl1792147212.db"
        target_path = "testcase//"
        pre_res = "npl19415.db"
        x = db_check()
        res = x.save_ue_db(db_path, target_path)
        self.assertEqual(res, target_path+pre_res)

    def test_save_app_db(self):    
        db_path = "testcase//nplServer1467704905.db"
        target_path = "testcase//"
        pre_res = "nplServer19414.db"
        x = db_check()
        res = x.save_app_db(db_path, target_path)
        self.assertEqual(res, target_path+pre_res)

if __name__=="__main__":
    unittest.main()
