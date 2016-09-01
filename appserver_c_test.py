# -*- coding:utf8 -*-
from appserver_c import appserver_c
import time
import unittest
import sqlite3
import threading

class TestAppserver_C(unittest.TestCase):
    def test_start_provision(self):
        x = appserver_c()
        res = x.start_provision()
        p_d = None
        self.assertNotEqual(p_d, res)
    def test_get_url(self):
        x = appserver_c(db_name="testdata//nplServer1.db")
        res = x.get_url()
        p_d = 3
        self.assertEqual(p_d, res)
    
    def test_appserver_provision(self):
        db_name = "testdata//nplServerPro.db"
        x = appserver_c(db_name)
        x.get_url() #get db
        res = x.wait_provision()
        self.assertEqual(res, "Actived")
    
        

    def test_wait_get_url(self):
        db_name = "testdata//nplServer1_wait.db"
        x = appserver_c(db_name)        
        p_d = 3
        s1 = threading.Thread(target=self._chang_db, args=(db_name,)) 
        s1.start()
        time.sleep(3)
        res = x.get_url()
        self.assertEqual(p_d, res)
    
    def test_timeout_get_url(self):
        db_name = "testdata//nplServer1_timeout.db"
        x = appserver_c(db_name)        
        p_d = "timeout err"
        s1 = threading.Thread(target=self._chang_db, args=(db_name, "no_insert",)) 
        s1.start()
        time.sleep(3)
        res = x.get_url()
        self.assertEqual(p_d, res)

    def _chang_db(self, db_name, has_insert = "has_insert"):
        conn = sqlite3.connect(db_name)
        drop_sql = """
            DROP TABLE IF EXISTS "table_provision_status";
            """
        create_sql = """
            CREATE TABLE "table_provision_status" (
            "server_id"  INTEGER NOT NULL,
            "prov_status"  TEXT NOT NULL,
            "token"  TEXT NOT NULL,
            PRIMARY KEY ("server_id" ASC)
            );
        """
        c = conn.cursor()
        c.execute(drop_sql)
        c.execute(create_sql)
        conn.commit()
        if "has_insert" == has_insert :
            time.sleep(10)
            #conn = sqlite3.connect(db_name)
            insert_sql = """INSERT INTO "table_provision_status" ("server_id", "prov_status", "token") VALUES ('3', 'Waiting_active', '1');"""
            #c = conn.cursor()
            c.execute(insert_sql)
            conn.commit()
        conn.close()
    def x_test_app_provision(self):
        """test app provision all """
        x = appserver_c(db_name="nplServer1.db")       
        x.app_provision(num=str(time.time()), app_Mon =1)

    def test_try_app_provision(self):
        """test app provision all """
        x = appserver_c(db_name="nplServerx.db", cfg="testdata/err_eap.cfg", eap_provision_server ="1.1.1.1", path="noapp_path")       
        res = x.try_app_provision(num=str(time.time()), app_Mon =1)
        print res

if __name__=="__main__":
    unittest.main()
