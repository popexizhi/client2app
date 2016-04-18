#-*-coding:utf8-*-
import sys
from httper import httper
from logMoner import logMon
from dbget import db_mod
from cfg_writer import filewriter
from shell_con import sh_control

class test_dev_p():
    def __init__(self):
        self.eap_ip = "192.168.1.43"
        self.eap_http = httper(self.eap_ip)
   
    def add_dev_lic(self, applications_name):
        #self._mon_app_log()
        add_res = self.eap_http.add_dev_lic(applications_name)
        return add_res["result"]

    def _mon_app_log(self):
        """通过监控appserver log判断是否可以开始dev lic add """
        x = logMon()
        return x.mon_provision()
    
    def get_dev_pin(self, num):
        x = db_mod()
        new_dev_pin = x.get_pin(num)
        assert new_dev_pin #db一定有返回
        cfg_w = filewriter("alone_dev.cfg")
        cfg_w.savenewfile(new_dev_pin, app = 0)
         

if __name__ == "__main__":
    num = int(sys.argv[1])
    a = test_dev_p()
    applications_name = [num]
    print "add_dev_lic res is ..."
    print a.add_dev_lic(applications_name)
    a.get_dev_pin(num)
    print "dev_cfg is ok ...."

    #启动client
    c = sh_control()
    c.dev_provision(num)
