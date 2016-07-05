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

def provision(devnum = 1):
    """
    1.app provision
    2.dev provision
    """
    appnum = 1

    #1.app provision
    #1.1get cfg provision
    time_host = int(time.time())
    res_cfg_list = get_app_lic(appnum, std = time_host)
    print "appserver cfg list is %s " % str(res_cfg_list)    
    assert len(res_cfg_list) == appnum #创建的cfg文件一定是要provision的app的数量
    
    #1.2 app provision
    appid = appnum 
    app_Mon = app_provision_res(appid)
    start_app(time_host, app_Mon)
    
    #2.dev provision
    while 0 == app_Mon.get_provision_status():
        time.sleep(5)
        print "\t\t[waiting] .. appserver provision .."
    print "*** " * 50
    print "dev provision , DEV NUM is %d" % devnum
    start_dev(devnum, time_host)
         

if __name__ == "__main__":
    provision()

