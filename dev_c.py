#-*-coding:utf8-*-
import sys
from httper import httper
from logMoner import logMon
from dbget import db_mod
from cfg_writer import filewriter
from shell_con import sh_control
import thread, time

class test_dev_p():
    def __init__(self, eap_ip = "192.168.1.43"):
        self.eap_ip = eap_ip
        self.eap_http = httper(self.eap_ip)
   
    def add_dev_lic(self, applications_name):
        #self._mon_app_log() #app provision修改后，不再使用此流程
        add_res = self.eap_http.add_dev_lic(applications_name)
        return add_res["result"]

    def _mon_app_log(self):
        """通过监控appserver log判断是否可以开始dev lic add """
        x = logMon()
        return x.mon_provision()
    
    def get_dev_pin(self, num):
        x = db_mod(db_name = "nexus_eapII" , ip = "192.168.1.44", user = "admin", pd = "password")
        new_dev_pin = x.get_pin(num)
        assert new_dev_pin #db一定有返回
        cfg_w = filewriter("alone_dev.cfg")
        cfg_w.savenewfile(new_dev_pin, app = 0)
         

def dev_provision(num):
    a = test_dev_p(eap_ip = "192.168.1.42")
    applications_name = [num]
    print "add_dev_lic res is ..."
    print a.add_dev_lic(applications_name)
    a.get_dev_pin(num)
    print "dev_cfg is ok ...."

    #启动client
    c = sh_control()
    c.dev_provision(num)
def start_dev(num, app_Mon):
    sh = sh_control()
    app_provision_wait_time = 0
    ts = 1
    while 1 :
        if 1 == app_Mon.get_provision_status():
            print "%s app provision is ok ..." % str(num)                
            sh.back_up_app(num)
            break
        else:
            print "wait %s app provision ; app_provision_wait_time is %f" % (str(num), app_provision_wait_time)
            time.sleep(ts)
            app_provision_wait_time = app_provision_wait_time + ts
            if app_provision_wait_time > 30 :
                return -1 # app_provision_wait_time超时无法完成后续工作

    for i in xrange(1):
        thread.start_new_thread(dev_provision,(i + num, ))
        print "start dev....%d" % int(i + num)
        time.sleep(1)

if __name__ == "__main__":
    num = int(sys.argv[1])
    start_dev(num)
