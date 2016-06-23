#-*- coding:utf8 -*-
import re, os, sys
import time
import manager_tc #testcase 加载

class agent_c():
    def __init__(self, args = 0 ):            
        self.agent_num = 1
        self.check_num = 0
        if args > 0 :
            print "** " * 50
            print "check the result "
            self.check_num = 1
            
        self.tc_man = manager_tc.manager_tc(self.check_num)

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
    tc_id_list = []
    is_check = 0
    for i in sys.argv:
        if "agent.py" == i:
            pass
        else:
            if "CHECK" == i:
                is_check = 1
            else:
                tc_id_list.append(i)
    a = agent_c(is_check) 
    a.set_tc(tc_id_list)
    a.run_tc()
