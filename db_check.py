# -*- coding:utf8 -*-
import re, os
import sqlite3

class db_check():
    def __init__(self):
        pass

    def db_save(self, dir_p=".//", t_pa = "back_db//"):
        pa = t_pa
        pre = "nplServer"
        os.system("mkdir %s" % t_pa)
        file_list = self.get_all_db(dir_p)
        res = 0
        for i in file_list:
            self.log("now process db is %s" % i)
            if re.findall(pre, i):
                self.log("serverdb is %s"% str(i))
                #serverdb process
                res_db = self.save_app_db(i, t_pa)
                self.log("target app db is %s" % str(res_db))
                self.backdb(i, res_db)
                res = res + 1
            else:
                #client process
                res_db = self.save_ue_db(i, t_pa)
                self.log("target ue db is %s" % str(res_db))
                self.backdb(i, res_db)
                res = res + 1

        return res

    def backdb(self, d_pa, t_pa):
        cmd = "cp %s %s" % (str(d_pa), str(t_pa))
        os.system(cmd)


    def save_app_db(self, db_p, target_p):
        sql = "SELECT host_id from AppServerHostInfo"
        host_id = self.get_host_id(sql, db_p)
        return "%snplServer%s.db" % (target_p, str(host_id))

    def save_ue_db(self, db_p, target_p):
        sql = "SELECT local_host_id from target_host_info ;"
        host_id = self.get_host_id(sql, db_p)
        return "%snpl%s.db" % (target_p, str(host_id))
    
    def get_host_id(self, sql, db_p):
        con  = sqlite3.connect(db_p)
        cursor = con.execute(sql)
        for j in cursor:
            self.log("host_id: %s" % str(j[0]))
            res = j[0]
        return res

    def get_all_db(self, pa="."):
        path = pa
        suf = "\.db$"
        self.log("path = %s" % path)
        res = []
        x_dir = {}
        for i in os.listdir(path):
            if re.findall(suf, i):
                res.append(path+"//"+i) 
                x_dir[i] = "0"
            else:
                #self.log(i)
                pass

        return res

    def log(self, message):
        print "** " * 20
        print message

if __name__=="__main__":
    a = db_check()
    a.db_save(".//", "back_up//")
