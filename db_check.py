# -*- coding:utf8 -*-
import re, os
import sqlite3

class db_check():
    def __init__(self):
        pass

    def db_save(self, dir_p="back_db"):
        pa = dir_p
        
    def get_all_db(self, pa="."):
        path = pa
        self.log("pa = %s" % pa)
        res = []
        x_dir = {}
        for i in os.listdir(path):
            if re.findall("db$", i):
                res.append(i) 
                x_dir[i] = "0"
            else:
                self.log(i)

        return res

    def log(self, message):
        print "** " * 20
        print message

if __name__=="__main__":
    a = db_check()
    a.db_save()
