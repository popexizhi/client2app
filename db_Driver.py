# -*- conding:utf8 -*-
import sqlite3
import re
class sqlite_Driver():
    def __init__(self, dbpath):
        self.path = dbpath
    def log(self, message):
        print "*" * 20
        print message

    def select(self, sql):
        """retunr [(), ()...] for all data """
        self.log(self.path)
        conn = sqlite3.connect(self.path)
        res = []
        self.log("select sql is %s" % str(sql))
        try:
            cursor = conn.execute(sql)
            #self.log(str(cursor))
            if 0 == cursor:
                self.log("cursor is 0:%s" % str(cursor))
                
            for i in cursor:
                res.append(i) 
            
            self.log("select res is %s" % str(res))
        except:
            self.log("except err ... ")
        conn.close()     
        
        return res
    def get_prov_status(self):
        """
        return SELECT prov_status from table_provision_status;
        """
        sql = "SELECT prov_status from table_provision_status;"
        res = self.select(sql)
        if len(res)>0 :
            assert 1 == len(res)
            status = res[0][0]
            assert status
        else:
            status = None
        return status

    def get_dev_host_id(self):
        """
        return select host_id,L2_target_host_id  from host_info;
        [for dev db]
        """
        sql = "select host_id,L2_target_host_id  from host_info;"
        res = self.select(sql)
        assert 1 == len(res)
        return res[0]

    def get_app_host_id(self):
        """
        return select host_id from table_L1_info;
        """
        sql = "select host_id from table_L1_info;"
        res = self.select(sql)
        assert 1 == len(res)
        return res[0][0]

    def get_server_id(self):
        """
        return SELECT server_id from table_provision_status;
        """
        sql = "SELECT server_id from table_provision_status;"
        res = self.select(sql)
        if len(res) > 0 :
            assert 1 == len(res)
            status = res[0][0]
            assert status
        else:
            status = None
        return status


if __name__ == "__main__":
    x =  sqlite_Driver("nplServer1.db")
    print x.get_server_id()
