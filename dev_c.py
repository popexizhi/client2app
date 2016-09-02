#-*-coding:utf8-*-
import sys, re
from httper import httper
from dbget import db_mod
from cfg_writer import filewriter
import thread, time
from shell_con import sh_control
from pexpect_shell import sh_pex
from db_Driver import sqlite_Driver
from mapping import *
import err

class dev_c():
    def __init__(self, dev_num = 10, eap_ip = EAP_Pro_mapping["url"], dev_mod = dev_mapping["cfg"]):
        self.eap_ip = eap_ip
        self.log_file = "dev_file.log"
        #操作间隔时间设置，防止操作太过频繁对服务的压力过大
        self.space_http_s = dev_mapping["space_http_s"] #http请求
        self.space_provision_s = dev_mapping["space_provision_s"] #dev provision 的请求间隔

        
        self.httper = httper(self.eap_ip, self.space_provision_s)
        #self.db = db_mod()
        self.db = db_mod(db_name = EAP_Pro_mapping["DB"]["EAP"]["db_name"] , ip = EAP_Pro_mapping["DB"]["EAP"]["ip"], user =     EAP_Pro_mapping["DB"]["EAP"]["user"], pd = EAP_Pro_mapping["DB"]["EAP"]["passwd"])
        self.cfg = filewriter(dev_mod)
        self.sh_control = sh_control()
        self.pex_dev = sh_pex()

        self.dev_lic_list_num = dev_num
        self.dev_lic_list_start = int(time.time()) #使用当前时间作为申请的dev_lic起点

        self.res_list = {} #记录provision 结果使用 pexpect_dev使用
        self.sqldb_path = dev_mapping["db_name"]
    def log_f(self, message):
        f = open(self.log_file,"a")
        f.write(str(message) + str("\n"))
        f.close()
    def log(self, message):
        print "*" * 20
        print message

    def add_dev_lic(self, user_email):
        """ 
        1. 从db中获得user_email的user_id
        2.通过此user_id 使用post增加对应的dev lic
        """
        assert self.httper
        assert self.db
        #1
        user_id = self.db.get_dev_user_id(user_email)
        #2
        if None == user_id:
            raise err.ProvisionError("EAP db no has user_id for %s" % str(user_email))
        return self.httper.add_dev_lic(user_id)

    def add_user(self, user_email, server_id):
        """
        1.通过post 请求添加 user_email
        2.修改步骤1用户为指定的appserver
        """
        # 1
        assert self.httper
        res = self.httper.add_user(user_email)
        if 0 != res["result"]: #如果添加不成功无法进行后续修改操作
            raise err.ProvisionError("add_user for user_email:%s res is %s" % (str(user_email), str(res)))
        # 2
        assert self.db
        res_server_id = self.db.change_user_appserver(user_email, server_id)
        return server_id == res_server_id #如果修改成功返回为True, 否则为失败


    def get_use_dev_lics(self, dev_pins):
        """
        从dev_pins的list中筛选self.dev_lic_list_num个self.dev_lic_list_start开始的值

        """
        assert dev_pins
        dev_use_list = []
        format_mail = "%d_\d" % self.dev_lic_list_start
        self.log_f( "xxx " * 20)
        self.log_f("[format_mail] %s" % format_mail)
        self.log_f("[dev_pins] %s" % str(dev_pins))
        #for i in dev_pins:
        #    print "i is " + str(i)
        if re.search(format_mail, dev_pins[0]):
           dev_use_list.append(dev_pins)
        else:
           print "dev_pin is %s,\n dev_pin is not include %s" % (str(dev_pin), str(format_mail))
           assert 0 == 1 #err  

        return dev_use_list


    def change_dev_cfg(self, user_email):
        """
        1.从eap_db 中获得dev可用pincode
        2.修改dev cfg
        return dev配置文件名称
        """
        #1
        assert self.db
        #pincode = self.db.get_dev_pin(user_email)[0]
        #self.log("get dev pin code is %s" % pincode)
        #time.sleep(30)
        pincode = self.db.get_dev_pin(user_email)[0]
        self.log("get dev pin code is %s" % pincode)
        #2
        assert self.cfg
        dev_file = self.cfg.change_dev_pincode(user_email, pincode)
        return dev_file

    def start_dev(self, cfg_dev, path = dev_mapping["dev_path"]):
        """
            1.start dev
            2.wait dev provision is ok
        """
        assert self.pex_dev
        
        #1
        self.pex_dev.start_dev(path = path, cfg = cfg_dev)
        #2
        dev_log_flag = "OnEventDeviceStatusIndication: status\(18:Completed\)"
        self.pex_dev.wait_dev_provision(5000, dev_log_flag )

    def save_dev_db(self, dev_db_name = "npl1.db", server_id = 29):
        """
        1.从db库中获得dev host_id
        2.保存db到 server_id//nplhost_id.db
        """
        #1.
        assert self.sqldb_path
        sqldb = sqlite_Driver(self.sqldb_path)
        dev_host, appserver_host = sqldb.get_dev_host_id()
        self.log("dev_host_id is %s; appserver_host is %s" % (str(dev_host), str(appserver_host)))
        assert dev_host
        assert appserver_host
        #2.
        assert self.sh_control
        
        self.sh_control.back_up_dev_db(appserver_host, dev_host)
        

    def dev_provision(self, user_name = int(time.time()), server_id = 29):
        """
        dev provision 流程如下:
        1./api/eap/users post 添加新用户
        2.修改nexus_eap库中eap_user_app_servers 保持1中的user为预期的appserver
        3./api/eap/users/%user_id/accesskey?application_id=com.senlime.nexus.app.browser 生成新的dev license
        4.从nexus_eap.eap_access_key中获得3添加的license
        5.修改dev的cfg文件
        [6.启动对应的appserver] 
        7.开始dev的provision start_dev()
        8.监控dev本地db和log 等待provision 成功
        9.保存dev db
        """
        # 1, 2
        if False == self.add_user(user_name, server_id): #如果添加不成功无法后续操作
            raise err.ProvisionError("change user:%s for server_id:%s is False" % (str(user_name), str(server_id)))

        # 3
        res_add_dev_lic = self.add_dev_lic(user_name)
        if 0 != res_add_dev_lic["result"] :
            raise err.ProvisionError("eap add_dev_lic for user_name res is %s" % (str(user_name), str(res_add_dev_lic)))

        # 4,5
        cfg_path = self.change_dev_cfg(user_name)

        #[6]

        #7, 8
        pex_dev = self.start_dev(cfg_path)

        #9
        res = self.save_dev_db("npl1.db", server_id)
        #return res

    def try_dev_provision(self, user_name = int(time.time()), server_id = 29):
        """
        try dev_provision
        """
        try:
            res = self.dev_provision(user_name, server_id)
        except err.ProvisionError as e:
            res = "[ERR.ProvisionError] %s" % str(e)
            self.log(res)
        return res

if __name__ == "__main__":
    num = int(sys.argv[1])
    #x = dev_c()
    server_id = 50
    for i in xrange(num):
        print "*" * 20
        x = dev_c()
        x.dev_provision(str(time.time()), server_id)
        print "*" * 20
        time.sleep(dev_mapping["space_provision_s"])

