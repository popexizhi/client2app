# -*- coding:utf8 -*-
from appserver_c import *
from dev_c import *
import sys, time
from shell_con import sh_control
from test_report import logMon_check
from provision_test import *
from app_lock import app_provision_res # app_provision use
def doing_test(num):
    #app start
    wait_time = 5 #等待完成间隔
    app_Mon = app_provision_res(num)
    start_app(num, app_Mon)
    time.sleep( wait_time )
    res = start_dev(num, app_Mon)
    if -1 == res:
        return res


if __name__ == "__main__":
    num  = int(time.time())#int(sys.argv[1])
    use_num = 101 # 100
    #前置条件，注册app 的lic
    get_app_lic(use_num ,std = num)
    
    #测试过程
    x = sh_control()
    for i in xrange(use_num): 
        app_id = i + num
        res = doing_test(app_id)        
        if -1 == res:
            print "err for app provision" * 20
            break
        print "start kill dev %d " % app_id
        x.kill_dev()
        print "** " * 200
        time.sleep(5)
    #结果处理
    rep_writer = logMon_check()
    testsuit_name = "test_%s" % str(num) #测试名称，报告和备份是使用
    rep_writer.res_process("log", testsuit_name)
    rep_writer.save_res() #保存L1测试报告
    x.back_up(testsuit_name)
