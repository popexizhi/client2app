#-*-coding:utf8-*-
import httper
import re
from pexpect_dev import sh_dev
from mapping import *

STEP_LIST = {
                "step_ue_start": None, #step_ue_start,
                "stop ue": None, #step_stop,
                "send \d+ packages": None, #step_ue_send,
                }

class testcase():
    def __init__(self, tc_stru):
        self.tc_stru = tc_stru
        self.httper = httper.httper()
        STEP_LIST["step_ue_start"] = self.step_ue_start
        STEP_LIST["stop ue"] = self.step_stop
        STEP_LIST["send \d+ packages"] = self.step_ue_send

    def init_pre(self):
        self.pre_list = self.tc_stru.get_preconditions()
        print "testcase preconditions is %s " % str(self.pre_list)
        for i in self.pre_list:
            self.step_download(i)

    def get_step(self):
        self.step_list = self.tc_stru.get_step()
        print "** " * 10 
        print self.step_list
    
    def step_doing_all(self):
        assert self.step_list
        print "[step num is %d] start .." % len(self.step_list)
        print "**" * 50
        for i in self.step_list:
            self.step_doing(i)

    def step_doing(self, step_name):
        for i in STEP_LIST:
            res = re.findall(i, step_name)
            if len(res) > 0:
                print "** " * 20
                print "STEP_LIST is %s , step con is %s" % (str(i), str(res))
                STEP_LIST[i]()

    def step_download(self, filename):
        #self.get_file(filename) # 后期修改为self.httper下载
        self.httper.get_bfile(filename)

    def step_ue_start(self, host_id=1):
        self.sh_dev = sh_dev(host_id)
        self.sh_dev.dev_start()

    def step_ue_send(self, packet_num=10):
        assert self.sh_dev
        self.sh_dev.dev_send_data(packet_num)

    def step_stop(self):
        assert self.sh_dev
        self.sh_dev.dev_kill()



    def get_file(self, filename):
        bk = environment_map["agent"]["tc_bk"]
        f = open(bk + filename, "rb")
        con = f.readlines()
        f.close()

        f = open(filename, "wb")
        for i in con:
            f.write(i)

        f.close()
        


class tc_stru():
    """装载testcase的xml标签 next:使用xml驱动改写"""
    def __init__(self, con):
          self.tc_con = con

          self.LAB_preconditions = "<preconditions>.*</preconditions>"
          self.LAB_step = "<actions>.*</actions>" # next 使用懒惰统计

    def get_preconditions(self):
        res_preconditions = []
        for i in self.tc_con.split("\n"):
            x = re.findall(self.LAB_preconditions, i)
            if len(x) > 0:
               pre_con = re.split("[><]", x[0])[2]
               res_preconditions = pre_con.split(",")
               #print res_preconditions
               return res_preconditions

        return res_preconditions

    def get_step(self):
        res_step = ["step_ue_start",]
        for i in self.tc_con.split("\n"):
            x = re.findall(self.LAB_step, i)
            if len(x) > 0:
                step_con = re.split("[><]", x[0])[2]
                #print step_con
                res_step.append(step_con)
        
        return res_step

def test_tc_stru():
    con = """    
    <summary>clinet send 10 tcp packages</summary>
    <preconditions>npl1.db,ue_1.cfg</preconditions>
    <execution_type>1</execution_type>
    <steps>
        <step>
            <step_number>1</step_number>
            <actions>send 10 packages</actions>
            <expectedresults>send pass</expectedresults>
            <execution_type>1</execution_type>
        </step>
        <step>
            <step_number>2</step_number>
            <actions>stop ue</actions>
            <expectedresults>stop ue</expectedresults>
            <execution_type>1</execution_type>
        </step>
    </steps>    
    """
    x = tc_stru(con)
    #x.get_preconditions()

    tc = testcase(x)
    tc.init_pre()
    tc.get_step()

if __name__ == "__main__":
    test_tc_stru()
