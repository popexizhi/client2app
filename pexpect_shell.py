# -*- encoding:utf8 -*-
# pexpect use for stdout
import pexpect,time
import re
from httper import httper
from pex_log import pexLog

class sh_pex():
    def __init__(self):
        self.pexpect = None
        self.x_pex = None

    def get_url(self, num):
        #app_sta_shell = """./app_server -cfg="alone_with_provision.cfg" -db -server_provision"""
        #app_sta_shell = """./app_server -cfg="alone_%d_app.cfg" -db -server_provision"""
        app_sta_shell = './app_server -cfg="cfg/app_%d_alone.cfg" -db -server_provision -host="%d" ' % (num, num)
        get_char_1 = "App Server Provision Params Read"
        get_char_2 = "App Server Added on EAP, please register on EAP"
        send_c = "a"
        check_url = "Requesting URL https://192.168.1.42:443/api/admin/sync-appserver/\d+"
        x_pexpect = pexpect.spawn(app_sta_shell)
        x = pexLog("app_server.log.txt")
        self.log("wait %s" % get_char_1)
        x.expect(get_char_1, timeout = 5*60) #getchar before
        x_pexpect.sendline(send_c) #send_char

        self.log("wait %s" % get_char_2)
        x.expect(get_char_2, timeout = 5*60) #getchar before
        x_pexpect.sendline(send_c) #send_char
        #url check
        self.log("wait %s" % check_url)        
        x.expect(check_url, timeout = 5*60) #getchar before
        app_id = re.findall(r"\d+$",x.after[0])
        print app_id[0]
        #x.interact() # 把sh的连接交给用户控制
        self.pexpect = x #将shell控制权交给类变量
        self.x_pex = x_pexpect
        return app_id[0]
    
    def log(self, message):
        print "[log_pexpect] sta "+ "*** " * 20
        print message
        print "[log_pexpect] end "+ "*** " * 20

    def send_provision(self):
        """appserver provision,监控 appserver log的provision结果"""
        assert self.pexpect
        appserver_provision = "secretL1ConnectionHostID"
        print "wait .. .." + appserver_provision
        self.pexpect.expect(appserver_provision, timeout=5 * 60)
        print self.pexpect.after
       
    def l2_provision(self):
        """dev provision """
        assert self.pexpect
        dev_provision = "rcv data:" #通过L2 数据开始传入作为成功的条件
        self.pexpect.expect(dev_provision, timeout=5 * 60)
        print self.pexpect.after

if __name__=="__main__":
    a = sh_pex()
    print a.get_url(1467606399)
