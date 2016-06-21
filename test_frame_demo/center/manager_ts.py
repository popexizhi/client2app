#-*- coding:utf8 -*-
import re, time
import os
import jenkins_c
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
    a = manager_tc("TCPsendfile.xml")
    tc_id = a.get_tc_num()
    print "tc_id is %s" % tc_id
    
    j = jenkins_c.jenkins_c()
    job_id = j.build_job(tc_id)
    print "job_id is %s" % str(job_id)
    print "%s build is %s" % (job_id, j.wait_job_pass(job_id))
