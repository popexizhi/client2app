# -*- coding:utf8 -*-
# {db调用，myslq/sqllite}
import re, os
import sqlite3
class sqllite():
    def __init__(self):
        """ """
        self.path = None

    def select(self, sql):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        conn.close()
        return res
    
    def select_ue_hostid(self, db_path):
        host_id =""
        self.path = db_path
        sql = "SELECT local_host_id from target_host_info ;"
        res_select = self.select(sql)
        assert len(res_select) == 1
        host_id = res_select[0][0]
        return host_id
    
    def select_ser_hostid(self, db_path):
        host_id =""
        self.path = db_path
        sql = "SELECT host_id from AppServerHostInfo ;"
        res_select = self.select(sql)
        assert len(res_select) == 1
        host_id = res_select[0][0]
        return host_id

    def select_target_hostid(self, db_path):
        sql = "SELECT L2_target_host_id from target_host_info ;"
        self.path = db_path
        res_select = self.select(sql)
        assert len(res_select) == 1
        host_id = res_select[0][0]
        return host_id
        
class g_db():
    def __init__(self):
        self.sqllit = sqllite()

    def get_hostid(self, path):
        if re.search("Server", path):
            return self.sqllit.select_ser_hostid(path)
        else:
            return self.sqllit.select_ue_hostid(path)

    def get_target_hostid(self, path):
        return self.sqllit.select_target_hostid(path)

if __name__ == "__main__":
    db = sqllite()
    ser_path = "test_db\\nplServer1465202670.db"
    ue_path = "test_db\\npl1465202670.db"
    print db.select_ue_hostid(ue_path)
    print db.select_ser_hostid(ser_path)
    print "** " * 5
    g = g_db()
    print "server path hostid %d" % g.get_hostid(ser_path)
    print "ue path hostid %d" % g.get_hostid(ue_path)
    print "ue target_host_id %d" % g.get_target_hostid(ue_path)
