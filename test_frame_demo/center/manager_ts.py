#-*- coding:utf8 -*-
import re, time
import os
from jenkins_c import *

WAIT_TIME = 2 * 60 # 等待此时间无数据，存储剩余内容为文件 : 来源appserver的rec_process.py
class manager_tc():
    def __init__(self, ts = "1.xml"):
        self.ts = ts
        self.web_path = "/data/provision_test/testcase_use/"

    def get_tc_num(self):
        res_num = 0
        res_num = self.change_tc()
        return res_num

    def change_tc(self):
        f= open(self.ts,'r')
        con = f.readlines()
        f.close()
        
        tc_id = int(time.time())
        f=open(self.web_path + str(tc_id) + "_" + self.ts,"w")
        for i in con:
            f.write(i)

        f.close()
        
        return str(tc_id) + "_" + self.ts
if __name__ == "__main__":
    #tc_name_list = "TCPsendfile.xml"
    tc_name_list = "send_random_packate.xml,TCPsendfile.xml"
    tc_id_list = ""
    for i in tc_name_list.split(","):
        a = manager_tc(i)
        tc_id_list = tc_id_list +" "+ a.get_tc_num()
        print "tc_id is %s" % i
    
    j = jenkins_c()
    job_id = j.build_job(tc_id_list)
    print "job_id is %s" % str(job_id)
    print "%s build is %s" % (job_id, j.wait_job_pass(job_id))

    print "**-" * 10
    for i in xrange(WAIT_TIME):
        time.sleep(1)
        print "waiting rec log , 剩余时间: %d " % (WAIT_TIME - i )

    #使用appserver服务器的res_agent检查
    #next修改为ELK的agent检查
    job_id = j.build_job(tc_id_list, job_name = res_job_list[0]) 
    print "job_id is %s" % str(job_id)
    print "%s build is %s" % (job_id, j.wait_job_pass(job_id))    
