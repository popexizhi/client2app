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
    provision_res_list = {}
    x = appserver_c(db_name=app_mapping["db_name"], cfg =app_mapping["cfg"], eap_provision_server=EAP_Pro_mapping["url"])
    app_res = x.try_app_provision(num=str(time.time()), app_Mon =1, npls_thrift_port= app_mapping["thrift_port_list"][0]+int(app_num))
    provision_res_list["app"] = app_res
    provision_res_list["dev"] = {}
    server_id = x.get_appserver_id()
    dev_p = threading.Thread(target=provision_dev, args = (dev_num, server_id, provision_res_list["dev"], ))
    dev_p.start()
    x.wait_dev_provision(dev_num)

    return provision_res_list
    

def provision_dev(dev_num, server_id, dev_list={}):
    for i in xrange(dev_num):
        log("start dev is %d" % i)
        #time.sleep(30)
        x = dev_c()
        dev_res = x.try_dev_provision(str(time.time()), server_id)
        dev_list["dev_%d" % i] = dev_res
        log("stop dev is %d" % i)
        time.sleep(dev_mapping["space_provision_s"])
    log("server_id:%s provision dev result is %s" % (str(server_id), str(dev_list)))
def log(message):
    f = open("tester.log","aw")
    f.write("[%s] %s\n" % (str(time.time()), message))
    f.close()

    print "**-- " * 50
    print message

def app_dev_provision(app_num, dev_num):
    log("Provision start [app_num:%d] [dev_num:%d]" % (app_num, dev_num))
    app_dev = {}
    for i in xrange(app_num):
        log("start app server num is %d" % i)
        res = doing_test(i, dev_num)
        app_dev[i] = res
        log("app server num{%d} is pass" % i)
    log("Provision TEST is pass:: [app_num:%d] [dev_num:%d]" % (app_num, dev_num))
    return app_dev
    
if __name__ == "__main__":
    app_num = int(sys.argv[1])
    dev_num = int(sys.argv[2])
    res = app_dev_provision(app_num, dev_num)

    log("STOP ALL . THE RESULT IS %s" % str(res))
