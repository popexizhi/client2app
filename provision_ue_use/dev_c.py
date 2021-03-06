#-*-coding:utf8-*-
import sys, re
from httper import httper
from dbget import db_mod
from cfg_writer import filewriter
import thread, time
from shell_con import sh_control
from pexpect_dev import sh_dev

class test_dev_p():
    def __init__(self, dev_num = 10):
        self.eap_ip = "192.168.1.55"
        self.log_file = "dev_file.log"
        #操作间隔时间设置，防止操作太过频繁对服务的压力过大
        self.space_http_s = 0 #http请求
        self.space_provision_s = 0.1 #dev provision 的请求间隔

        
        self.eap_http = httper(self.eap_ip, self.space_http_s)
        self.sh_control = sh_control()
        self.sh_dev = sh_dev(self)

        self.dev_lic_list_num = dev_num
        self.dev_lic_list_start = int(time.time()) #使用当前时间作为申请的dev_lic起点

        self.res_list = {} #记录provision 结果使用 pexpect_dev使用
        #self.
    def log_f(self, message):
        f = open(self.log_file,"a")
        f.write(str(message) + str("\n"))
        f.close()

    def add_dev_lic(self, applications_name):
        #self._mon_app_log() #app provision修改后，不再使用此流程
        add_res = self.eap_http.add_devs(applications_name, self.dev_lic_list_num, self.dev_lic_list_start)
        return add_res
    
    def get_use_dev_lics(self, dev_pins):
        """
        从dev_pins的list中筛选self.dev_lic_list_num个self.dev_lic_list_start开始的值

        """
        assert dev_pins
        dev_use_list = []
        format_mail = "%d_\d" % self.dev_lic_list_start
        self.log_f( "xxx " * 20)
        self.log_f( format_mail)
        for i in dev_pins:
            if re.search(format_mail, i[0]):
                dev_use_list.append(i)

        return dev_use_list


    def get_dev_pin(self, num):
        x = db_mod()
        new_dev_pins = x.get_pin(num)
        assert new_dev_pins #db一定有返回

        new_dev_pins_use = self.get_use_dev_lics(new_dev_pins)
        self.log_f( "*** " * 20)
        self.log_f( "get pins from db is " + str(len(new_dev_pins_use)))
        j = 0
        for i in new_dev_pins_use:
            self.log_f( "*** " * 20)
            self.log_f( "[start dev] %d_%d" % (self.dev_lic_list_start, j) )
            cfg_w = filewriter("alone_dev.cfg")
            cfg_w.savenewfile(i, app = 0, names = [self.dev_lic_list_start, j])

            self.start_dev(j)

            time.sleep(self.space_provision_s)
            j = j + 1

    def start_dev(self, num_id):
        #启动client
        #thread.start_new_thread(self.sh_control.dev_provision,(self.dev_lic_list_start , num_id, ))
        self.res_list[num_id] = {}
        thread.start_new_thread(self.sh_dev.dev_check,(self.dev_lic_list_start , num_id, self.res_list[num_id]))
        

def dev_provision(app_id, num):
    a = test_dev_p(num)
    applications_name = [app_id]
    a.log_f( "add_dev_lic res is ...")
    dev_lic_http_res = a.add_dev_lic(applications_name)
    a.log_f( dev_lic_http_res)
    a.get_dev_pin(app_id) # num
    a.log_f( "dev_cfg is ok ....")

    return a.res_list

def start_dev(num):
    app_provision_wait_time = 0
    ts = 1
    for i in xrange(1):
        res = dev_provision(3, num)
        print "start dev....%d" % int(i + num)

    END = 0
    L2_PASS = "Completed"
    while END< (num-1):
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
        print "now END is %d, num-2 is %d" % (END, num-2)
        for j in end_list:
            if 0 == j[0]:
                print "%d is no L2" % j[1]
        time.sleep(5)
    s =  sh_control() 
    s.back_use_cp()
if __name__ == "__main__":
    num = int(sys.argv[1])
    ev_num = 50
    if num > ev_num:
        count = num / ev_num
        res = num % ev_num
        print "count %d \t res %d" % (count, res)
        for i in xrange(count):
            start_dev(ev_num)
            print "### " * 100
            print "now is %d ok" % ((i+1)*ev_num)
            time.sleep(5)
        start_dev(res)
        
        print "### " * 100
        print "now is %d ok , please wc -l db$ " % num
    else:
        start_dev(num)

