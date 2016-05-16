# -*- encoding:utf8 -*-
# pexpect use for stdout
import pexpect,time
import re
from httper import httper
class sh_pex():
    def __init__(self):
        self.pexpect = None
        
    def get_url(self):
        app_sta_shell = """./app_server -cfg="alone_with_provision.cfg" -db -server_provision"""
        get_char_1 = "App Server Provision Params Read"
        get_char_2 = "App Server Added on EAP, please register on EAP"
        send_c = "a"
        check_url = "Requesting URL https://192.168.1.43:443/api/admin/sync-appserver/\d+"
        x = pexpect.spawn(app_sta_shell)
        x.expect(get_char_1) #getchar before
        x.sendline(send_c) #send_char
        x.expect(get_char_2) #getchar before
        x.sendline(send_c) #send_char
        #url check
        x.expect(check_url) #getchar before
#        print "*** " * 20
#        print x.after
#        print "*** " * 20
        app_id = re.findall(r"\d+$",x.after)
        print app_id[0]
        #x.interact() # 把sh的连接交给用户控制
        self.pexpect = x #将shell控制权交给类变量
        return app_id[0]
    
    def send_provision(self):
        """appserver provision,监控 appserver log的provision结果"""
        assert self.pexpect
        appserver_provision = "App Server Provision finished"
        self.pexpect.expect(appserver_provision)
        print self.pexpect.after
        


if __name__=="__main__":
    a = sh_pex()
    print a.get_url()
