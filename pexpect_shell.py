# -*- encoding:utf8 -*-
# pexpect use for stdout
import pexpect,time
import re
from httper import httper

class sh_pex():
    def __init__(self):
        self.pexpect = None
    
    def start_appserver(self, path="app_server", cfg="alone_app.cfg", args = ["-db", "-server_provision"]):
        """start appserver """
        self.app = path
        self.cfg = cfg
        self.args_app = args
        args_list = self.get_args(self.args_app)
        command_app = './%s -cfg="%s" %s' % (self.app, self.cfg, str(args_list))
        self.log(command_app)
        
        self.pexpect = pexpect.spawn(command_app)
        return self.pexpect
    def get_args(self, args_list):
        assert args_list
        res = ""
        for i in args_list:
            res = res + " %s" % i

        return res
    
    def start_dev(self, path="slim_engine_test", cfg="alone_dev.cfg", args= ["-db", "-provision"]):
        """
            start dev 
        """
        self.dev = path
        self.cfg_dev = cfg
        self.args_dev = args
        args_list = self.get_args(self.args_dev)
        command_dev = './%s -cfg="%s" %s' % (self.dev, self.cfg_dev, str(args_list))
        self.log(command_dev)
        self.pexpect = pexpect.spawn(command_dev)
        #self.pexpect.expect("dpaadfjksjfkjd", timeout = 900000) #getchar before
        #self.pexpect.expect("dpaadfjksjfkjd", timeout = 900000) #getchar before
        return self.pexpect
    
    def wait_dev_provision(self, timeout = 90000, dev_log_flag = "OnEventDeviceStatusAnswer: status_query_id:10, status(18:Completed)"):
        assert self.pexpect
        self.pexpect.expect(dev_log_flag, timeout) #getchar before
        return self.pexpect
        

    def get_url(self, num):
        #app_sta_shell = """./app_server -cfg="alone_with_provision.cfg" -db -server_provision"""
        #app_sta_shell = """./app_server -cfg="alone_%d_app.cfg" -db -server_provision"""
        app_sta_shell = './app_server -cfg="cfg/app_%d_alone.cfg" -db -server_provision -host="%d" ' % (num, num)
        get_char_1 = "App Server Provision Params Read"
        get_char_2 = "App Server Added on EAP, please register on EAP"
        send_c = "a"
        check_url = "Requesting URL https://192.168.1.42:443/api/admin/sync-appserver/\d+"
        x = pexpect.spawn(app_sta_shell)
        self.log("wait %s" % get_char_1)
        x.expect(get_char_1) #getchar before
        x.sendline(send_c) #send_char

        self.log("wait %s" % get_char_2)
        x.expect(get_char_2) #getchar before
        x.sendline(send_c) #send_char
        #url check
        self.log("wait %s" % check_url)        
        x.expect(check_url) #getchar before
#        print "*** " * 20
#        print x.after
#        print "*** " * 20
        app_id = re.findall(r"\d+$",x.after)
        print app_id[0]
        #x.interact() # 把sh的连接交给用户控制
        self.pexpect = x #将shell控制权交给类变量
        return app_id[0]
    
    def log(self, message):
        print "[log_pexpect] sta "+ "*** " * 20
        print message
        print "[log_pexpect] end "+ "*** " * 20

    def send_provision(self):
        """appserver provision,监控 appserver log的provision结果"""
        assert self.pexpect
        #appserver_provision = "App Server Provision finished"
        appserver_provision = "secretL1ConnectionHostID host="
        print "wait .. .." + appserver_provision
        self.pexpect.expect(appserver_provision, timeout=5 * 60)
        print self.pexpect.after
       
    def l2_provision(self):
        """dev provision """
        assert self.pexpect
        dev_provision = "rcv data:" #通过L2 数据开始传入作为成功的条件
        self.pexpect.expect(dev_provision)
        print self.pexpect.after

if __name__=="__main__":
    a = sh_pex()
    print a.get_url(1467606399)
