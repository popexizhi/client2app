#-*-coding:utf8-*-
import httper
import re
from pexpect_dev import sh_dev
from mapping import *
from slim_client import slim_client
STEP_LIST = {
                "step_ue_start": None, #step_ue_start,
                "start with (.*).cfg (.*).db so": None, #step_start_so with host=.* 
                "stop ue": None, #step_stop,
                "send (\d+) packages": None, #step_ue_send,
                "send (.*).log": None, #step_send_file,
                }
CHECK_LIST = {
                }
class testcase():
    def __init__(self, tc_stru):
        self.tc_stru = tc_stru
        self.httper = httper.httper()
        self.c_socket = slim_client()

        STEP_LIST["step_ue_start"] = self.step_ue_start
        STEP_LIST["start with (.*).cfg (.*).db so"] = self.step_start_so
        STEP_LIST["stop ue"] = self.step_stop
        STEP_LIST["send (\d+) packages"] = self.step_ue_send
        STEP_LIST["send (.*).log"] = self.step_send_file

    def init_pre(self):
        self.pre_list = self.tc_stru.get_preconditions()
        print "testcase preconditions is %s " % str(self.pre_list)
        for i in self.pre_list:
            self.step_download(i)

    def get_step(self):
        self.step_list = []
        for i in self.tc_stru.get_step():
            checkres, par = self.check_step(i)
            if "ERR_STEP_NO_INIT" == checkres:
                print "*** " * 20
                print "%s is ERR_STEP_NO_INIT" % i 
                break
            else:
                self.step_list.append([checkres, par, i]) #将结果作为队列存储
        print "** " * 10 
        for i in self.step_list:
            print i

        #return checkres

    def check_step(self, step_name, list_use = STEP_LIST ):
        """
        检查step_name是否在 STEP_LIST 存在:
        1.不存在返回ERR_STEP_NO_INIT, null
        2.存在返回STEP_LIST中步骤名称和参数
        """
        checkres = "ERR_STEP_NO_INIT"
        args = []
        for i in list_use:
            check_re = re.compile(i)
            res = check_re.findall(step_name)
            if len(res) > 0:
                #print "[check_step] step name is %s;\t args is %s ;\t step_name is %s" % (i, res, step_name)
                checkres = i
                args = res
                
        return checkres, args

    def step_doing_all(self, step_list = 1):
        if 2 == step_list :
            assert self.step_expectedresults_list
            list_d = self.step_expectedresults_list
        if 1 == step_list : 
            assert self.step_list
            list_d = self.step_list
        
        print "[step num is %d] start .." % len(list_d)
        print "**" * 50
        for i in list_d:
            self.step_doing(i, step_list)

    def step_doing(self, step_arg_li, step_list = 1):
        if 1 == step_list:
            list_d = STEP_LIST
        if 2 == step_list:
            list_d = CHECK_LIST
        for i in list_d:
            res = re.findall(i, step_arg_li[0])
            if len(res) > 0:
                print "** " * 5
                print "STEP_LIST is %s , step con is %s, arg is %s" % (str(i), str(res), str(step_arg_li[1]))
                list_d[i](step_arg_li[1])

    def step_start_so(self, args_tup):
        #use hostid start so
        # "start with (.*).cfg (.*).db so": None, #step_start_so with host=.* 
        cfg, npl_hostid = args_tup[0]
        self.cfg = cfg + ".cfg"
        x = re.compile("npl(\d*)")
        hostid = x.findall(npl_hostid)[0]
        print "[next] step_start_so \t cfg = %s, hostid = %s" % (self.cfg , str(hostid))
        self.c_socket.start_client(cfg = str(self.cfg) , db_num = int(hostid))
        self.socket = self.c_socket 

    def step_send_file(self, filenames):
        """ 
        "send (.*).log": None, #step_send_file,
        
        1.open file,get content
        2.send content for line
        """
        assert filenames
        print "[next] step_send_file"
        filename = filenames[0] + ".log"
        f = open(filename, "rb")
        content = f.readlines()
        f.close()
        print "content is %s" % content
        # send data
        assert self.socket 
        for i in content:
            print "[step_send_file] " * 2 + "send: %s" % i
            self.socket.send_data(i)


    def step_download(self, filename):
        #self.get_file(filename) # 后期修改为self.httper下载
        self.httper.get_bfile(filename)

    def step_ue_start(self, host_id=1):
        self.sh_dev = sh_dev(host_id)
        self.sh_dev.dev_start() 



    def step_ue_send(self, packet_num=10):
        assert self.sh_dev
        self.sh_dev.dev_send_data(packet_num)

    def step_stop(self, noarg):
        assert self.sh_dev
        self.sh_dev.dev_kill()



    def get_file(self, filename):
        bk = environment_map["agent"]["tc_bk"]
        f = open(bk + filename, "rb")
        con = f.readlines()
        f.close()

        f = open(filename, "wb")
        for i in con:
            f.write(i)

        f.close()
        


class tc_stru():
    """装载testcase的xml标签 next:使用xml驱动改写"""
    def __init__(self, con):
          self.tc_con = con

          self.LAB_preconditions = "<preconditions>.*</preconditions>"
          self.LAB_step = "<actions>.*</actions>" # next 使用懒惰统计
          self.LAB_step_expectedresults = "<expectedresults>.*</expectedresults>" # next 使用懒惰统计,增加对应的step验证

    def get_preconditions(self):
        res_preconditions = []
        for i in self.tc_con.split("\n"):
            x = re.findall(self.LAB_preconditions, i)
            if len(x) > 0:
               pre_con = re.split("[><]", x[0])[2]
               res_preconditions = pre_con.split(",")
               #print res_preconditions
               return res_preconditions

        return res_preconditions

    def get_step(self):
        #res_step = ["step_ue_start",]
        res_step = []
        for i in self.tc_con.split("\n"):
            x = re.findall(self.LAB_step, i)
            if len(x) > 0:
                step_con = re.split("[><]", x[0])[2]
                print step_con
                res_step.append(step_con)
        
        return res_step

    def get_step_expectedresults(self):
        res_expectedresults = []
        for i in self.tc_con.split("\n"):
            x = re.findall(self.LAB_step_expectedresults, i)
            if len(x) > 0:
                step_con = re.split("[><]", x[0])[2]
                print step_con
                res_expectedresults.append(step_con)
        
        return res_expectedresults

def test_tc_stru():
    con = """    
    <summary>clinet send 10 tcp packages</summary>
    <preconditions>npl1465202670.db,nplServer1465202670.db,alone_integration.cfg</preconditions>
    <execution_type>1</execution_type>
    <steps>
        <step>
            <step_number>3</step_number>
            <actions>start with alone_integration.cfg npl1465202670.db so</actions>
            <expectedresults>start ok</expectedresults>
            <execution_type>1</execution_type>
        </step>    
        <step>
            <step_number>1</step_number>
            <actions>send 10 packages</actions>
            <expectedresults>send pass</expectedresults>
            <execution_type>1</execution_type>
        </step>
        <step>
            <step_number>2</step_number>
            <actions>send send_data.log</actions>
            <expectedresults>stop ue</expectedresults>
            <execution_type>1</execution_type>
        </step>
    </steps>    
    """
    x = tc_stru(con)
    #x.get_preconditions()
    #x.get_step_expectedresults()

    tc = testcase(x)
    tc.init_pre()
    tc.get_step()
    tc.step_doing_all()

if __name__ == "__main__":
    test_tc_stru()
