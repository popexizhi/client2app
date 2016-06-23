# -*- coding:utf8 -*-

from tc_use import *
from logMonitor import logMonitor
from mapping import *

class tc_check(testcase):
    def __init__(self, tc_stru):

        CHECK_LIST["ue (\d*) start ok"] = self.check_start_ue
        CHECK_LIST["appserver received (.*).log"] = self.check_recevied_log
        testcase.__init__(self, tc_stru) 
        self.logMonitor = logMonitor(environment_map["agent"]["log_path"])
    
    def init_pre(self):
        testcase.init_pre(self) 


    def get_step_expectedresults(self):
        """<expectedresults> """
        #get_step_expectedresults
        self.step_expectedresults_list = []
        for i in self.tc_stru.get_step_expectedresults():
            checkres, par = self.check_step(i, list_use = CHECK_LIST)
            if "ERR_STEP_NO_INIT" == checkres:
                print "*** " * 20
                print "%s is ERR_STEP_NO_INIT" % i 
                break
            else:
                self.step_expectedresults_list.append([checkres, par, i]) #将结果作为队列存储
        print "[step_expectedresults_list]" + "** " * 10 
        for i in self.step_expectedresults_list:
            print i           
        print "[step_expectedresults_list]" + "-- " * 10 


    def step_check_doing_all(self):
        #self.step_doing_all(2) #[?] 好奇怪的问题，子类初始化过但是调用父类的方法后此方法为None，why?
        list_d = self.step_expectedresults_list
        print "[check num is %d] start .." % len(list_d)
        print "**" * 50
        for i in list_d:
            self.step_check_doing(i)        

    def step_check_doing(self, step_arg_li):
        list_d = CHECK_LIST
        print "--" * 20
        print "start [step_check_doing] name : %s" % str(step_arg_li)
        print CHECK_LIST
        for i in list_d:
            if i == step_arg_li[0]:
                print "** " * 5
                print "STEP_LIST is %s , arg is %s" % (str(i), str(step_arg_li[1]))
                list_d[i](step_arg_li[1])

    def check_start_ue(self, args):
        print "check_start_ue"
    
    def check_recevied_log(self, args):
        print "check_recevied_log"
        pre_f = args[0] + ".log"
        print self.logMonitor.check_file(pre_f)

def test_tc_check():
    con = """
    <summary>client 使用TCP 发送send_data.log文件内容</summary>
    <preconditions>npl1465202670.db,nplServer1465202670.db,alone_integration.cfg,send_data.log</preconditions>
    <execution_type>1</execution_type>
    <steps>
        <step>
            <step_number>1</step_number>
            <actions>start with alone_integration.cfg npl1465202670.db so</actions>
            <expectedresults>ue 1465202670 start ok</expectedresults>
            <execution_type>1</execution_type>
        </step>
        <step>
            <step_number>2</step_number>
            <actions>send send_data.log</actions>
            <expectedresults>appserver received send_data.log</expectedresults>
            <execution_type>1</execution_type>
        </step>
    </steps>
    """
    x = tc_stru(con)
    tc_c = tc_check(x)
    tc_c.init_pre()
    tc_c.get_step_expectedresults()
    tc_c.step_check_doing_all()

if __name__ == "__main__":
    test_tc_check()
