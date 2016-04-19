# -*- coding:utf8 -*-
from appserver_c import *
from dev_c import *
import sys, time
from shell_con import sh_control
from test_report import logMon_check
from provision_test import *

def doing_test(num):
    #app start
    start_app(num)
    time.sleep(40)
    start_dev(num)
    time.sleep(60 * 2)


if __name__ == "__main__":
    num  = int(sys.argv[1])
    #注册app 的lic
    get_app_lic(num = 100,std = num)

    x = sh_control()
    for i in xrange(5):
        app_id = i*20 + num
        doing_test(app_id)        
        print "start kill all %d + 10" % app_id
        print "** " * 20
        x.kill_all()
    rep_writer = logMon_check()
    rep_writer.res_process("log")
