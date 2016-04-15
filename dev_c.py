#-*-coding:utf8-*-
import sys
from httper import httper
from logMoner import logMon
from dbget import db_mod

class test_dev_p():
    def __init__(self):
        self.eap_ip = "192.168.1.43"
        self.eap_http = httper(self.eap_ip)
   
    def add_dev_lic(self, applications_name):
        self._mon_app_log()
        add_res = self.eap_http.add_dev_lic(applications_name)
        return add_res["result"]

    def _mon_app_log(self):
        """通过监控appserver log判断是否可以开始dev lic add """
        x = logMon()
        return x.mon_provision()
    
    def get_dev_pin(self, num):
        x = db_mod()
        return x.get_pin(num)


if __name__=="__main__":
    num = int(sys.argv[1])
    a = test_dev_p()
    applications_name = [num]
    a.add_dev_lic(applications_name)
    print a.get_dev_pin(num)
