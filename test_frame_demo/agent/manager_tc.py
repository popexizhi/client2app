#-*-coding:utf8-*-
import httper
import re

from tc_use import testcase, tc_stru
from mapping import *
from tc_check import *

class manager_tc():
    def __init__(self, check_num = 0):
        self.tc_from = "http" #mysql
        
        self.httper = httper.httper(url_base = environment_map["httper"]["url"])
        self.tc_f_list = []
        self.tc_con_list = {}
        self.is_check = check_num # 是否为check res使用

    def get_tc_list(self, id_list):
        assert type(id_list) == type([])
        if self.is_check > 0 :
            tc_d = tc_check #检查res使用
            print "** " * 20
            print "start tc_check"
        else:
            tc_d = testcase #执行testcase使用
            print "** " * 20
            print "start testcase doing"

        #get testcase file
        for i in id_list:
            print "tc num is %s" % str(i)
            print "start get testcase con .. . . ."
            i_tc_f, i_tc_c = self.get_tc(i)
            self.tc_f_list.append(i_tc_f)         #get testcase file
            i_tc = tc_d(tc_stru(i_tc_c)) 
            self.tc_con_list[i_tc_f] = i_tc #get testcase strcut 

    def get_tc(self, tc_id):
        tc_con = self.httper.get_xml(tc_id)

        tc_path = environment_map["agent"]["tc_path"] 
        tc_file = tc_path + str(tc_id) + ".feature_xml"
        
        f = open(tc_file,"w")
        f.write(tc_con)
        f.close()

        return tc_file, tc_con

    def init_pre(self):
        """ for all tc_con_list init_pre"""
        for i in self.tc_con_list:
            self.tc_con_list[i].init_pre()


    def tc_run(self):
        """ for all step run"""
        if self.is_check > 0 :
            for i in self.tc_con_list:
                self.tc_con_list[i].get_step_expectedresults()
                self.tc_con_list[i].step_check_doing_all()
        else :
            for i in self.tc_con_list:
                self.tc_con_list[i].get_step()
                self.tc_con_list[i].step_doing_all()

def test_manager():
    a = manager_tc()
    a.get_tc_list([1466129033])
    a.init_pre()
    a.tc_run()


if __name__ == "__main__":
    test_manager()
    #test_tc_stru()
