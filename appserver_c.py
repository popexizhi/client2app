#-*- coding:utf8 -*-
import sys
from db_Driver import sqlite_Driver
from httper import httper
import thread
import time
class appserver_c():
    def __init__(self, db_name="nplServer1.db", cfg="alone_app.cfg"):
        self.db = sqlite_Driver(db_name)
        self.cfg = cfg
        self.wait_time = 3 * 60 #appserver provision 超时时间

    def log(self, message):
        print "~" * 20
        print message

    def start_provision(self):
        """change cfg start appserver provision """
        pass
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
            res = "timeout err"
            # wait timeout for server_id
        else:
            res = res % server_id

        self.log(res)
        return res        
    
def app_provision(num, app_Mon):
    """
    1.change app cfg start appserver
    2.wait appdb server_id
    3.post id+key+serial /api/eap/appservers/<server_id>/activation
    4.wait log 打印 Please Add User Pin...
    """
    appserver = appserver_c()
    #1.change app cfg start appserver
    appserver.start_provision()
    #2.wait appdb server_id
    url_id = a.get_url(num)
    assert url_id #检查返回的id一定存在
    print "** " * 20
    print "get url_id is "
    print url_id

    #3.post id+key+serial /api/eap/appservers/<server_id>/activation
    print "** " * 20
    print "3.post id+key+serial /api/admin/register_app_server"
    http_x = httper("192.168.1.42")
    res_add_app_key = http_x.add_appserver_lic(num)
    assert 0 == res_add_app_key["result"] #要求添加结果一定为成功，否则退出后续流程
    print http_x.register_app_server(url_id, num, res_add_app_key["key"], res_add_app_key["serial"])
    print "log is " + "$$ " * 20
    a.send_provision()
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

