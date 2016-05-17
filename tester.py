# -*- coding:utf8 -*-
from appserver_c import *
from dev_c import *
import sys, time
from shell_con import sh_control
from test_report import logMon_check
from provision_test import *

def doing_test(num):
    #app start
    wait_time = 5 #等待完成间隔
    start_app(num)
    time.sleep( wait_time )
    start_dev(num)
    time.sleep( wait_time * 2)


if __name__ == "__main__":
    num  = int(time.time())#int(sys.argv[1])
    use_num = 1 # 100
    #前置条件，注册app 的lic
    get_app_lic(use_num ,std = num)
    
    #测试过程
    x = sh_control()
    for i in xrange(use_num): 
        app_id = i*10 + num
        doing_test(app_id)        
        print "start kill dev %d " % app_id
        print "** " * 20
        x.kill_all()

    #结果处理
    rep_writer = logMon_check()
    testsuit_name = "test_%s" % str(num) #测试名称，报告和备份是使用
    rep_writer.res_process("log", testsuit_name)
    x.back_up(testsuit_name)
