# -*- coding:utf8 -*-
from appserver_c import *
from dev_c import *
from mapping import *
import sys, time
from shell_con import sh_control
from test_report import logMon_check
from provision_test import *
from app_lock import app_provision_res # app_provision use
import threading
def doing_test(app_num, dev_num):
    #app start
    x = appserver_c(db_name=app_mapping["db_name"], cfg =app_mapping["cfg"], eap_provision_server=EAP_Pro_mapping["url"])
    x.app_provision(num=str(time.time()), app_Mon =1, npls_thrift_port= app_mapping["thrift_port_list"][0]+int(app_num))
    server_id = x.get_appserver_id()
    dev_p = threading.Thread(target=provision_dev, args = (dev_num, server_id, ))
    dev_p.start()
    x.wait_dev_provision(dev_num)
    

def provision_dev(dev_num, server_id):
    for i in xrange(dev_num):
        log("start dev is %d" % i)
        x = dev_c()
        x.dev_provision(str(time.time()), server_id)
        log("stop dev is %d" % i)
        time.sleep(dev_mapping["space_provision_s"])
        
def log(message):
    f = open("tester.log","aw")
    f.write("[%s] %s\n" % (str(time.time()), message))
    f.close()

    print "**-- " * 50
    print message

if __name__ == "__main__":
    app_num = int(sys.argv[1])
    dev_num = int(sys.argv[2])
    log("Provision start [app_num:%d] [dev_num:%d]" % (app_num, dev_num))
    for i in xrange(app_num):
        log("start app server num is %d" % i)
        doing_test(i, dev_num)
        log("app server num{%d} is pass" % i)
