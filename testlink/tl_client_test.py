# -*- coding:utf8 -*-
import unittest
from tl_client import tl_client
import err

class TestTl_client(unittest.TestCase):
    def test_gettclist(self):
        """
        test tcid for ts_tc_list
        """
        data = [{'node_order': '0', 'is_open': '1', 'id': '16', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '4', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 16:55:53', 'execution_type': '1', 'preconditions': '', 'active': '1', 'creation_ts': '2016-09-12 16:55:11', 'node_table': 'testcases', 'tcversion_id': '3', 'name': '100*100app_dev', 'summary': '', 'author_id': '1', 'external_id': 'test-4'}, {'node_order': '1', 'is_open': '1', 'id': '13', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '3', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 16:55:35', 'execution_type': '1', 'preconditions': '', 'active': '1', 'creation_ts': '2016-09-12 16:55:04', 'node_table': 'testcases', 'tcversion_id': '3', 'name': 'dev provision', 'summary': '', 'author_id': '1', 'external_id': 'test-3'}, {'node_order': '2', 'is_open': '1', 'id': '8', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '2', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 15:51:39', 'execution_type': '1', 'preconditions': '', 'active': '1', 'creation_ts': '2016-09-12 15:51:21', 'node_table': 'testcases', 'tcversion_id': '3', 'name': 'napp provision', 'summary': '', 'author_id': '1', 'external_id': 'test-2'}, {'node_order': '3', 'is_open': '1', 'id': '5', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '1', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 15:57:43', 'execution_type': '1', 'preconditions': '<p>preconditions</p>', 'active': '1', 'creation_ts': '2016-09-01 14:55:27', 'node_table': 'testcases', 'tcversion_id': '3', 'name': 'app provision', 'summary': '<p>summery</p>', 'author_id': '1', 'external_id': 'test-1'}]
        pre_res = "16 13 8 5" 
        x = tl_client()
        res = x.gettclist(data)
        self.assertEqual(res, pre_res)
    def test_init_err(self):
        """
        test _init_ tl_url and key
        e :[testframe err]problems connecting the TestLink Server http://127.0.0.1/testlink/lib/api/xmlrpc.php
        """
        url = "127.0.0.1"
        x = tl_client(url)
        try:
            x.getTestCasesForTestSuite("3")
        except err.TFError as e:
            res = e
            print res.value
        pre_err = "404 Not Found"
        self.assertIn(pre_err, res.value)
    
    def test_init_key(self):
        """
        test _init_ tl_url and key
        e:
        """
        key = "127.0.0.1"
        x = tl_client(key=key)
        try:
            x.getTestCasesForTestSuite("3")
        except err.TFError as e:
            res = e
            print res.value
        pre_err = "invalid developer key"
        self.assertIn(pre_err, res.value)

if __name__=="__main__":
    unittest.main()
