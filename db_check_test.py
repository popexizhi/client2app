# -*- coding:utf8 -*-
import re, os
import sqlite3
from db_check import db_check
import unittest
import os

class Test_db_check(unittest.TestCase):

    def test_db_save(self):
        pa = "test_dir"
        x = db_check()
        res = x.db_save(pa)
        self.assertEqual(res,1)
    def test_get_all_db(self):
        db_pa = "testcase"
        x = db_check()
        res = x.get_all_db(db_pa)
        self.assertEqual(len(res), 6)
        

if __name__=="__main__":
    unittest.main()
