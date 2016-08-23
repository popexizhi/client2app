#-*-coding:utf8-*-
import sys, re
from httper import httper
from dbget import db_mod
from cfg_writer import filewriter
import thread, time
from shell_con import sh_control
from pexpect_shell import sh_pex

class dev_c():
    def __init__(self, dev_num = 10, eap_ip = "192.168.1.43:18080", dev_mod = "alone_dev.cfg"):
        self.eap_ip = eap_ip
        self.log_file = "dev_file.log"
        #操作间隔时间设置，防止操作太过频繁对服务的压力过大
        self.space_http_s = 0 #http请求
        self.space_provision_s = 0.1 #dev provision 的请求间隔

        
        self.httper = httper(self.eap_ip, self.space_provision_s)
        self.db = db_mod()
        self.cfg = filewriter(dev_mod)
        self.sh_control = sh_control()
        self.pex_dev = sh_pex()

        self.dev_lic_list_num = dev_num
        self.dev_lic_list_start = int(time.time()) #使用当前时间作为申请的dev_lic起点

        self.res_list = {} #记录provision 结果使用 pexpect_dev使用
        #self.
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
        assert user_id
        return self.httper.add_dev_lic(user_id)

    def add_user(self, user_email, server_id):
        """
        1.通过post 请求添加 user_email
        2.修改步骤1用户为指定的appserver
        """
        # 1
        assert self.httper
        res = self.httper.add_user(user_email)
        assert 0 == res["result"] #如果添加不成功无法进行后续修改操作
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

    def start_dev(self, cfg_dev):
        """
            1.start dev
            2.wait dev provision is ok
        """
        assert self.pex_dev
        #1
        self.pex_dev.start_dev(cfg = cfg_dev)
        #2
        dev_log_flag = "OnEventDeviceStatusIndication: status\(18:Completed\)"
        self.pex_dev.wait_dev_provision(5000, dev_log_flag )

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
        assert self.add_user(user_name, server_id) #如果添加不成功无法后续操作

        # 3
        assert 0 == self.add_dev_lic(user_name)["result"] 

        # 4,5
        cfg_path = self.change_dev_cfg(user_name)

        #[6]

        #7
        pex_dev = self.start_dev(cfg_path)

        return pex_dev 

def start_dev(num, app_id):
    app_provision_wait_time = 0
    ts = 1
    for i in xrange(1):
        res = dev_provision(app_id, num)
        print "start dev....%d" % int(i + num)

    END = 0
    L2_PASS = "Completed"
    while END< num:
        print "res " * 20
        END = 0
        end_list = []
        for i in res:
            end_list.append([0,i])
            print "cfg:%s res is :" % i
            for key in res[i]:
                print res[i][key]
                if re.search(L2_PASS, res[i][key]):
                    END = END + 1
                    end_list[i][0] = 1
                #else:
                #    print res[i][key]
        print "now END is %d, num is %d" % (END, num)
        for j in end_list:
            if 0 == j[0]:
                print "%d is no L2" % j[1]
        time.sleep(5)
    s =  sh_control() 
    s.back_use_cp()
if __name__ == "__main__":
    num = int(sys.argv[1])
    ev_num = 50
    app_id = 3
    if num > ev_num:
        count = num / ev_num
        res = num % ev_num
        print "count %d \t res %d" % (count, res)
        for i in xrange(count):
            start_dev(ev_num, app_id)
            print "### " * 100
            print "now is %d ok" % ((i+1)*ev_num)
            time.sleep(5)
        start_dev(res, app_id)
        
        print "### " * 100
        print "now is %d ok , please wc -l db$ " % num
    else:
        start_dev(num, app_id)

