#-*- coding:utf8 -*-
from httper import httper
from cfg_writer import filewriter
import sys

class test_p():
    def __init__(self, std = 3000):
        self.eap_ip = "192.168.1.43"
        self.eap_http = httper(self.eap_ip)
        self.std = std # appserver申请时的id补偿

    def add_appserver_lic(self, tot = 10):
        self.app_servers = []
        for i in xrange(tot):
            add_res = self.eap_http.add_appserver_lic(i+self.std)
            if 0 == add_res["result"]:
                self.app_servers.append(add_res)
            else:
                print "ERR add_appserver_lic %s" % str(add_res)
        self.__show_applist()
    
    def get_new_appserver_cfgs(self):
        j = 0
        for i in self.app_servers :
            x = filewriter()    
            x.savenewfile([str(j + self.std) , i["key"], i["serial"], str(j + self.std)])
            j = j + 1

    def __show_applist(self):
        for i in self.app_servers : 
            print i 

if __name__ == "__main__":
    test_num = 500
    if len(sys.argv) > 1 :
        std = sys.argv[1]
        a = test_p(std)
    else:
        a = test_p()
    a.add_appserver_lic(test_num)
    a.get_new_appserver_cfgs()
