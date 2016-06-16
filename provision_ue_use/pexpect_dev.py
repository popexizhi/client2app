# -*- encoding:utf8 -*-
# pexpect use for stdout
import pexpect,time
import re, copy
from httper import httper

class sh_dev():
    def __init__(self, objlog ):
        self.pexpect = None
        self.objlog = objlog

    def dev_check(self, start_num, num, res):
        """
        start dev ./slim_engine_test -cfg="cfg/dev_$1$2_alone.cfg" -db -provision -host="$1$2"
        check log is 
        OnEventDeviceStatusIndication: status(1:OTAP_Authenticating)
        OnEventDeviceStatusIndication: status(2:L1_Connecting)
        OnEventDeviceStatusIndication: status(3:L1_Connected)
        OnEventDeviceStatusIndication: status(5:EAP_Authenticating)
        OnEventDeviceStatusIndication: status(6:L2_Connecting)
        OnEventDeviceStatusIndication: status(8:Completed)
        """
        dev_sta_shell = './slim_engine_test -cfg="cfg/dev_%d%d_alone.cfg" -db -provision -host="%d%d" ' % (start_num, num, start_num , num)
        status_check = "OnEventDeviceStatusIndication"
        L1_PASS = "OnEventDeviceStatusIndication: status\(3:L1_Connected\)"
        L2_PASS = "OnEventDeviceStatusIndication: status\(8:Completed\)"
        HOST_ID = "SocketManagerRegister start, host_id=\d+"
        status_list = [L1_PASS, HOST_ID, L2_PASS]
        sh_dev = pexpect.spawn(dev_sta_shell)
        print dev_sta_shell
        print status_check
        for i in status_list:
            print " ** " * 10
            print "\n check num is %s" % i
            sh_dev.expect(i)
            
            print "** " * 30
            print sh_dev.after
            res[i] = copy.deepcopy(sh_dev.after)
            print "$$$ " * 20
        
        sh_dev.kill(0)
        

    def get_url(self, num):
        app_sta_shell = './app_server -cfg="cfg/app_%d_alone.cfg" -db -server_provision -host="%d" ' % (num, num)
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
        app_id = re.findall(r"\d+$",x.after)
        print app_id[0]
        #x.interact() # 把sh的连接交给用户控制
        self.pexpect = x #将shell控制权交给类变量
        return app_id[0]
    
    def send_provision(self):
        """appserver provision,监控 appserver log的provision结果"""
        assert self.pexpect
        appserver_provision = "App Server Provision finished"
        print "wait .. .." + appserver_provision
        self.pexpect.expect(appserver_provision)
        print self.pexpect.after
       
    def l2_provision(self):
        """dev provision """
        assert self.pexpect
        dev_provision = "rcv data:" #通过L2 数据开始传入作为成功的条件
        self.pexpect.expect(dev_provision)
        print self.pexpect.after

if __name__=="__main__":
    a = sh_pex()
    #print a.get_url()
    print a.dev_check()
