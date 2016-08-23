# -*- coding:utf8 -*-
from db_Driver import sqlite_Driver
import unittest

class TestSqlite_Driver(unittest.TestCase):
    def test_select(self):
        """ 基准测试select 使用 nplServer1.db """
        p_d_list = [(3,)]
        x = sqlite_Driver("testdata//nplServer1.db")
        #sql = "SELECT server_id, prov_status from table_provision_status;"
        sql = "SELECT server_id from table_provision_status;"
        res = x.select(sql)
        self.assertEqual(p_d_list, res)
    
    def test_get_server_id(self):
        """测试 server_id 使用 nplServer1.db """
        p_server_id = 3
        x = sqlite_Driver("testdata//nplServer1.db")
        res = x.get_server_id()
        self.assertEqual(p_server_id, res)
    
    def test_get_server_id(self):
        """测试 host_id 使用 npl1.db """
        dev_host_id = (100350, 100220)
        x = sqlite_Driver("testdata//npl1.db")
        res = x.get_dev_host_id()
        self.assertEqual(dev_host_id, res)

    def test_get_prov_status(self):
        """测试 prov_status 使用 nplServer1.db """
        p_status = "Waiting_active"
        x = sqlite_Driver("testdata//nplServer1.db")
        res = x.get_prov_status()
        self.assertEqual(p_status, res)
    
    def test_get_app_host_id(self):
        """测试 appserver的hostid 使用 nplServerok.db """
        x = sqlite_Driver("testdata//nplServerok.db")
        res = x.get_app_host_id()
        self.assertEqual(100155, res)

    def test_no_get_server_id(self):
        """测试 server_id is Null 使用  """
        p_server_id = None
        x = sqlite_Driver("testdata//nplServer1_no_serverid.db")
        res = x.get_server_id()
        self.assertEqual(p_server_id, res)
    
    def test_no_get_prov_status(self):
        """测试 prov_status is Null 使用 nplServer1_no_serverid.db """
        p_status = None
        x = sqlite_Driver("testdata//nplServer1_no_serverid.db")
        res = x.get_prov_status()
        self.assertEqual(p_status, res)
if __name__=="__main__":
    unittest.main()
