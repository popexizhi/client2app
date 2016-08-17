#-*- coding:utf8 -*-
import sys
from db_Driver import sqlite_Driver
from pexpect_shell import sh_pex
from httper import httper
import thread
import time
class appserver_c():
    def __init__(self, db_name="nplServer1.db", cfg="alone_app.cfg", eap_provision_server="192.168.1.43:18080"):
        self.db = sqlite_Driver(db_name)
        self.cfg = cfg
        self.wait_time = 3 * 60 #appserver provision 超时时间
        self.httper = httper(eap_provision_server) 
        self.pex_app = sh_pex()

    def log(self, message):
        print "~" * 20
        print message

    def start_provision(self, cfg_path="alone_app.cfg"):
        """change cfg start appserver provision """
        args_list = ["-db", "-server_provision"]
        app_path = "app_server"
        self.pex_app.start_appserver(path=app_path ,cfg=cfg_path, args= args_list)

        return self.pex_app
    def get_url(self):
        wait_time = self.wait_time
        assert self.db
        server_id = self.db.get_server_id()
        res = "/api/eap/appservers/%d/activation"
        use_time = 0
        while None == server_id and use_time < wait_time:
            time.sleep(5)
            use_time = use_time + 5
            server_id = self.db.get_server_id()

        if None == server_id:
            server_id = "timeout err"
            #res = "timeout err"
            # wait timeout for server_id
        else:
            res = res % server_id

        self.log(res)
        return server_id    

    def app_provision(self, num, app_Mon):
        """
        1.change app cfg start appserver
        2.wait appdb server_id
        3.post id+key+serial /api/eap/appservers/<server_id>/activation
        4.wait log 打印 Please Add User Pin...
        """
        #1.change app cfg start appserver
        assert self.start_provision() != None
        #2.wait appdb server_id
        url_id = self.get_url()
        assert url_id #检查返回的id一定存在
    
        #3.post id+key+serial /api/eap/appservers/<server_id>/activation
        self.log("3.post id+key+serial /api/admin/register_app_server")
        res_add_app_key = self.httper.add_appserver_lic(num)
        assert 0 == res_add_app_key["result"] #要求添加结果一定为成功，否则退出后续流程
        res = self.httper.register_app_server(url_id, num, res_add_app_key["key"], res_add_app_key["serial"])
        self.log(res)
        time.sleep(50)
        app_Mon.set_provision_pass()
        while 1:
            print "appserver_wait ... --- "
            time.sleep(1)
        #4.wait log 打印 request url id
        a.l2_provision()

def start_app(std, app_Mon):
    for i in xrange(1):
        try:
            thread.start_new_thread(app_provision,(i + std , app_Mon, ))
            print "start app....%d" % int(i +std)
            time.sleep(5)
        except:
            print "start_app err " * 20
            break
            
    #    a = sh_control()
    #    a.app_provision(i+std)

if __name__ == "__main__":
    std = int(sys.argv[1])
    app_provision_res = app_provision_res()
    start_app(std, app_provision)
    #app_provision(2)

