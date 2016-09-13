# -*- coding:utf8 -*-
import unittest
from tl_client import tl_client
import err

class TestTL_client(unittest.TestCase):
    def test_gettclist(self):
        """
        test tcid for ts_tc_list
        """
        data = [{'node_order': '0', 'is_open': '1', 'id': '16', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '4', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 16:55:53', 'execution_type': '1', 'preconditions': '', 'active': '1', 'creation_ts': '2016-09-12 16:55:11', 'node_table': 'testcases', 'tcversion_id': '3', 'name': '100*100app_dev', 'summary': '', 'author_id': '1', 'external_id': 'test-4'}, {'node_order': '1', 'is_open': '1', 'id': '13', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '3', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 16:55:35', 'execution_type': '1', 'preconditions': '', 'active': '1', 'creation_ts': '2016-09-12 16:55:04', 'node_table': 'testcases', 'tcversion_id': '3', 'name': 'dev provision', 'summary': '', 'author_id': '1', 'external_id': 'test-3'}, {'node_order': '2', 'is_open': '1', 'id': '8', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '2', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 15:51:39', 'execution_type': '1', 'preconditions': '', 'active': '1', 'creation_ts': '2016-09-12 15:51:21', 'node_table': 'testcases', 'tcversion_id': '3', 'name': 'napp provision', 'summary': '', 'author_id': '1', 'external_id': 'test-2'}, {'node_order': '3', 'is_open': '1', 'id': '5', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '1', 'parent_id': '3', 'version': '1', 'updater_id': '1', 'status': '1', 'tsuite_name': 'provision', 'importance': '2', 'modification_ts': '2016-09-12 15:57:43', 'execution_type': '1', 'preconditions': '<p>preconditions</p>', 'active': '1', 'creation_ts': '2016-09-01 14:55:27', 'node_table': 'testcases', 'tcversion_id': '3', 'name': 'app provision', 'summary': '<p>summery</p>', 'author_id': '1', 'external_id': 'test-1'}]
        pre_res = "16 13 8 5" 
        x = tl_client()
        res = x.gettclist(data)
        self.assertEqual(res, pre_res)
    
    def test_gettclist_tp(self):
        """
        test tcid for ts_tc_list(testcases for plan)
        """
        data={'25': [{'executed': '', 'execution_notes': '', 'tcversion_number': '', 'tc_id': '25', 'assigner_id': '', 'execution_order': '10', 'platform_name': '', 'linked_ts': '2016-09-13 10:23:51', 'tsuite_name': 'socket_L2', 'assigned_build_id': '', 'exec_on_tplan': '', 'execution_run_type': '', 'feature_id': '9', 'version': '1', 'exec_on_build': '', 'testsuite_id': '20', 'exec_status': 'n', 'status': '', 'importance': '2', 'execution_type': '1', 'execution_ts': '', 'active': '1', 'user_id': '', 'tester_id': '', 'exec_id': '', 'tcversion_id': '26', 'name': 'L2_TCP_send_random_packages', 'linked_by': '1', 'type': '', 'summary': u'<p>\u4f7f\u7528libNexus_Engine_SDK.so\u548c App_Server_SDK.so \u5efa\u7acbtcp</p>\n<p>client \u4f7f\u7528TCP \u53d1\u9001\u957f\u5ea6\u968f\u673a\u7684\u5185\u5bb9</p>', 'platform_id': '0', 'z': '1', 'external_id': '2', 'urgency': '2', 'priority': '4'}], '21': [{'executed': '', 'execution_notes': '', 'tcversion_number': '', 'tc_id': '21', 'assigner_id': '', 'execution_order': '0', 'platform_name': '', 'linked_ts': '2016-09-13 10:23:51', 'tsuite_name': 'socket_L2', 'assigned_build_id': '', 'exec_on_tplan': '', 'execution_run_type': '', 'feature_id': '8', 'version': '1', 'exec_on_build': '', 'testsuite_id': '20', 'exec_status': 'n', 'status': '', 'importance': '2', 'execution_type': '1', 'execution_ts': '', 'active': '1', 'user_id': '', 'tester_id': '', 'exec_id': '', 'tcversion_id': '22', 'name': 'clinet send 10 tcp packages', 'linked_by': '1', 'type': '', 'summary': u'<p>\u4f7f\u7528libNexus_Engine_SDK.so\u548c App_Server_SDK.so \u5efa\u7acbtcp</p>\n<p>client \u5411appserver\u53d1\u900110\u4e2a\u5305</p>', 'platform_id': '0', 'z': '0', 'external_id': '1', 'urgency': '2', 'priority': '4'}], '33': [{'executed': '', 'execution_notes': '', 'tcversion_number': '', 'tc_id': '33', 'assigner_id': '', 'execution_order': '10', 'platform_name': '', 'linked_ts': '2016-09-13 10:23:46', 'tsuite_name': 'provision', 'assigned_build_id': '', 'exec_on_tplan': '', 'execution_run_type': '', 'feature_id': '6', 'version': '1', 'exec_on_build': '', 'testsuite_id': '19', 'exec_status': 'n', 'status': '', 'importance': '2', 'execution_type': '1', 'execution_ts': '', 'active': '1', 'user_id': '', 'tester_id': '', 'exec_id': '', 'tcversion_id': '34', 'name': '1 appserver 10 dev provision', 'linked_by': '1', 'type': '', 'summary': u'<p>1\u4e2aappserver provision \u540e\uff0c\u6b64appserver\u768410dev provision</p>', 'platform_id': '0', 'z': '1', 'external_id': '4', 'urgency': '2', 'priority': '4'}], '37': [{'executed': '', 'execution_notes': '', 'tcversion_number': '', 'tc_id': '37', 'assigner_id': '', 'execution_order': '0', 'platform_name': '', 'linked_ts': '2016-09-13 10:23:46', 'tsuite_name': 'provision', 'assigned_build_id': '', 'exec_on_tplan': '', 'execution_run_type': '', 'feature_id': '5', 'version': '1', 'exec_on_build': '', 'testsuite_id': '19', 'exec_status': 'n', 'status': '', 'importance': '2', 'execution_type': '1', 'execution_ts': '', 'active': '1', 'user_id': '', 'tester_id': '', 'exec_id': '', 'tcversion_id': '38', 'name': '2 appserver 5 dev provision', 'linked_by': '1', 'type': '', 'summary': u'<p>2\u4e2aappserver provision \uff0c\u6bcf\u4e2aappserver provision\u6210\u529f\u540e\u5206\u522b\u518d\u67095dev provision</p>', 'platform_id': '0', 'z': '0', 'external_id': '5', 'urgency': '2', 'priority': '4'}], '29': [{'executed': '', 'execution_notes': '', 'tcversion_number': '', 'tc_id': '29', 'assigner_id': '', 'execution_order': '20', 'platform_name': '', 'linked_ts': '2016-09-13 10:23:46', 'tsuite_name': 'provision', 'assigned_build_id': '', 'exec_on_tplan': '', 'execution_run_type': '', 'feature_id': '7', 'version': '1', 'exec_on_build': '', 'testsuite_id': '19', 'exec_status': 'n', 'status': '', 'importance': '2', 'execution_type': '1', 'execution_ts': '', 'active': '1', 'user_id': '', 'tester_id': '', 'exec_id': '', 'tcversion_id': '30', 'name': '1 appserver provision', 'linked_by': '1', 'type': '', 'summary': u'<p>1\u4e2aappserver provision</p>', 'platform_id': '0', 'z': '2', 'external_id': '3', 'urgency': '2', 'priority': '4'}], '41': [{'executed': '', 'execution_notes': '', 'tcversion_number': '', 'tc_id': '41', 'assigner_id': '', 'execution_order': '20', 'platform_name': '', 'linked_ts': '2016-09-13 10:23:51', 'tsuite_name': 'socket_L2', 'assigned_build_id': '', 'exec_on_tplan': '', 'execution_run_type': '', 'feature_id': '10', 'version': '1', 'exec_on_build': '', 'testsuite_id': '20', 'exec_status': 'n', 'status': '', 'importance': '2', 'execution_type': '1', 'execution_ts': '', 'active': '1', 'user_id': '', 'tester_id': '', 'exec_id': '', 'tcversion_id': '42', 'name': 'tname_ue_socket_senddata', 'linked_by': '1', 'type': '', 'summary': u'<pre class="code highlight"><code><span class="line" id="LC4">client\u901a\u8fc7socket\u63a5\u53e3\u5411appserver\u53d1\u9001\u6570\u636e</span></code></pre>', 'platform_id': '0', 'z': '2', 'external_id': '6', 'urgency': '2', 'priority': '4'}]}

        pre_res = "25 21 33 37 29 41" 
        x = tl_client()
        res = x.gettclist(data, "tp")
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

    def test_getTestPlanByName(self):
        x = tl_client()
        res = x.getTestPlanByName("integration_tester")
        #res = x.getTestPlanByName("test_plan", "test")
        print res
    
    def test_getTestPlanByName_Err(self):
        x = tl_client()
        try:
            res = x.getTestPlanByName("integration_tester", "test")
        except err.TFError as e:
            res = e
            print res.value
        pre_err = "does not exist on Test Project"
        self.assertIn(pre_err, res.value)
        
    def test_getTestCasesForTestPlan(self):
        x = tl_client()
        res = x.getTestCasesForTestPlan(44)
        print res
    
    def test_getTestCasesForTestPlan_Err(self):
        """
        "[testframe err]3000: (getTestCasesForTestPlan) - The Test Plan ID (3) provided does not exist!\ngetTestCasesForTestPlan({'testplanid': 3, 'devKey': '641a49a91c63fe1a803ec1c5dc62a4e6'})"
        """
        x = tl_client()
        try:
            res = x.getTestCasesForTestPlan(13)
        except err.TFError as e:
            res = e
            print res.value
        pre_err = "provided does not exist"
        self.assertIn(pre_err, res.value)
if __name__=="__main__":
    unittest.main()
