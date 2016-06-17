#-*- coding:utf8 -*-
import re
import time
import manager_tc #testcase 加载

class agent_c():
    def __init__(self):            
        self.agent_num = 1
        self.tc_man = manager_tc.manager_tc()

    def set_tc(self, tc_list):
        assert type(tc_list) == type([])
        assert len(tc_list) > 0
        self.tc_list = tc_list
        print "tc_list is %s" % str(tc_list)
    
    def setup(self):
        """"
        1.下载self.tc_list 内容,装载tc_d_list
        2.为每个要执行的tc准备<preconditions>部分
        """

        #1.下载self.tc_list 内容,装载tc_d_list
        assert self.tc_list
        self.tc_man.get_tc_list(self.tc_list)
        

        #2.为每个要执行的tc准备<preconditions>部分
        self.tc_man.init_pre()
    
    def teardown(self):
        """
        1.处理tc中恢复部分
        """
        pass

    

    def run_tc(self):
        assert self.tc_list

        self.setup()
        self.doing()
        res = self.teardown()
        return res

    def doing(self):
        """
        根据tc的<step> list执行
        """
        self.tc_man.tc_run()

if __name__ == "__main__":
    a = agent_c()
    a.set_tc([1466129033])
    a.run_tc()
