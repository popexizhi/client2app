#-*- coding:utf8 -*-
import sys
from db_Driver import sqlite_Driver
from pexpect_shell import sh_pex
from httper import httper
from shell_con import sh_control
from cfg_writer import filewriter
from dbget import db_mod
from mapping import *
import thread
import time
class appserver_c():
    def __init__(self, db_name=app_mapping["db_name"], cfg=app_mapping["cfg"], eap_provision_server=EAP_Pro_mapping["url"]):
        self.db = sqlite_Driver(db_name)
        self.cfg = cfg
        self.wait_time = 3 * 60 #appserver provision 超时时间
        self.httper = httper(eap_provision_server) 
        self.pex_app = sh_pex()
        self.filewriter = None
        self.sh_con = sh_control()

    def log(self, message):
        print "~" * 20
        print message

    def start_provision(self, cfg_path=app_mapping["cfg"], port=10021):
        """change cfg start appserver provision """
        self.filewriter = filewriter(cfg_path)
        self.cfg_path = self.filewriter.change_thrift_port(port)
        assert self.cfg_path
        args_list = ["-db", "-server_provision"]
        app_path = app_mapping["app_path"] #"app_server"
        self.pex_app.start_appserver(path=app_path ,cfg=self.cfg_path, args= args_list)

        return self.pex_app
    def get_url(self):
        wait_time = self.wait_time
        assert self.db
        server_id = self.db.get_server_id()
        res = EAP_Pro_mapping["eap_api"]["appserver_activation"]
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
    def wait_provision(self):
        assert self.db
        wait_time = self.wait_time
        provision_stat = self.db.get_prov_status()
        use_time = 0 
        while provision_stat != APPSERVERDB["Actived"] and use_time < wait_time:
            time.sleep(5)
            use_time = use_time + 5
            provision_stat = self.db.get_prov_status()
       
        return provision_stat
    def setup(self):
        """前置条件准备
        1.update eap db中的provision成功的ip
        2.rm 本地db
        """
        self.db_eap = db_mod(db_name = EAP_Pro_mapping["DB"]["EAP"]["db_name"] , ip = EAP_Pro_mapping["DB"]["EAP"]["ip"], user = EAP_Pro_mapping["DB"]["EAP"]["user"], pd = EAP_Pro_mapping["DB"]["EAP"]["passwd"])
        self.db_eap.update_app_ip(app_mapping["ip"])
        self.sh_con.remove_all_db()

    def app_provision(self, num, app_Mon, npls_thrift_port = 10022):
        """
        1.change app cfg start appserver
        2.wait appdb server_id
        3.post id+key+serial /api/eap/appservers/<server_id>/activation
        """
        #0.前置条件准备
        self.setup()
        #1.change app cfg start appserver
        assert self.start_provision(port = npls_thrift_port) != None
        #2.wait appdb server_id
        url_id = self.get_url()
        assert url_id #检查返回的id一定存在
        self.appserver_id = url_id #provision成功后appserver_id值

        #3.post id+key+serial /api/eap/appservers/<server_id>/activation
        self.log("3.post id+key+serial /api/admin/register_app_server")
        res_add_app_key = self.httper.add_appserver_lic(num)
        assert 0 == res_add_app_key["result"] #要求添加结果一定为成功，否则退出后续流程
        res = self.httper.register_app_server(url_id, num, res_add_app_key["key"], res_add_app_key["serial"])
        self.log(res)
        assert 0 == res["result"]
        
        app_start = self.wait_provision()
        self.log("appserver provision is %s" % app_start)
        assert APPSERVERDB["Actived"]  == app_start
        
        #save db
        host_id = self.db.get_app_host_id()
        self.log("appserver hostid is %s" % str(host_id))
        self.sh_con.back_up_app_db(host_id)
    def get_appserver_id(self):
        """
        appserver provision成功后才包含此内容
        """
        assert self.appserver_id
        return self.appserver_id

    def wait_dev_provision(self, num):
        """
        wait dev provision pass
        """
        assert self.pex_app
        self.pex_app.wait_app_client_num(dev_mapping["space_provision_wait_time"]*num, num)

if __name__ == "__main__":
    
    std = int(sys.argv[1])
    
    for i in xrange(std):
        x = appserver_c(db_name=app_mapping["db_name"], cfg =app_mapping["cfg"], eap_provision_server=EAP_Pro_mapping["url"])
        x.app_provision(num=str(time.time()), app_Mon =1, npls_thrift_port= app_mapping["thrift_port_list"][0]+i)

