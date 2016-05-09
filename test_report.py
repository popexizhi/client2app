#-*- coding:utf8 -*-
import re
from os import walk
from HTMLTestRunnerx import HTMLTestRunner_ex #html 报告使用
from logMoner import logMon #L2 data use

class logMon_check():
    def __init__(self):
        self.ue_provision_finish = "ProvisionStatusIndication: status\\(.*Completed\\)"#"test client send finished"

    def get_l2_data(self, inputfile):
        """返回ue的log中最后一行的send data的number """
        res_pack = 0
        res_total_send_size = 0

        filepath = open(inputfile)
        con = filepath.readlines()
        filepath.close()
        
        search_l2 = re.compile(r'\*{6} (\d+) total')
        search_l2_total = re.compile(r'total_send_size=(\d+)')
        for i in con:
            pat_search = search_l2.search(i)
            if pat_search != None:
                res_pack = int(pat_search.group(1))    
                res_total_send_size = int(search_l2_total.search(i).group(1))
        
        return res_pack, res_total_send_size

    def mon_all_lines(self, inputfile):
        res = 0
        filepath = open(inputfile)
        con = filepath.readlines()
        filepath.close()

        check_log = self.ue_provision_finish
        for i in con:
            if re.search(check_log, i):
                print "%s is check pass" % inputfile
                return 1
        return 0
    
    def get_dir_files(self, dir_p):
        f = []
        res_file = []
        check_suf = "log.txt" #要求的后缀
        for (dirpath, dirnames, filenames) in walk(dir_p):
            f.extend(filenames)
            break
        for i in f:
            if re.search(check_suf, i):
                res_file.append(i)

        return res_file

    def res_process(self, dir_p, backup_dir):
        res = {}
        err_res = []
        pass_num = 0
        self.a=HTMLTestRunner_ex() #html use
        test_suit = "provision_ue"
        for i in self.get_dir_files(dir_p):
            if 1 == self.mon_all_lines(dir_p+"//"+i):
                res[i] = "pass"
                self.a.g_report_test(test_suit, i, res[i], "log has '"+self.ue_provision_finish +"'")
                pass_num = pass_num + 1
            else:
                res[i] = "fail"
                err_res.append(i)
                self.a.g_report_test(test_suit, i, res[i], "log doesn't have '"+self.ue_provision_finish + "'")


        totle = len(res)
        self.desc = "<tr><h4>100 provision test :</h4> </tr>"
        self.desc = self.desc + "<tr>总测试self.appserver 为 %d个 , dev 为%d 个<br /> 其中pass 完成provision的dev为 %d 个, 占%f</tr><br />" % (totle, totle, pass_num, pass_num/float(totle))
        self.desc = self.desc + '<tr>log 保存位置见  <a href="http://192.168.1.25/%s/log/">http://192.168.1.25/%s/log</a> </tr><br />'  % (backup_dir, backup_dir)
        self.desc = self.desc + '<tr>coredump 位置见 <a href="http://192.168.1.25/%s/corefile/">http://192.168.1.25/%s/corefile</a> </tr><br />' % (backup_dir, backup_dir)
        self.testname = backup_dir #报告名称使用
        return res, err_res

    def save_res(self):        
        self.a.set_report("100 provision_test & L2 data_test", self.desc)
        assert self.testname # test中定义
        self.a.g_savefile("ue_provision_res_%s.html" % self.testname)


    def res_l2(self, app_log = "app_server.log.txt"):
        """ L2 test 结果分析
        """
        testsuit = "L2 data test"
        x = logMon()
        res_l2 = x._search_list(app_log)
        #只测试L2的处理
        try:
            assert self.a
        except:
            self.a =HTMLTestRunner_ex() #html use
        #只测试L2的处理
        try:
            assert self.desc
        except:
            self.desc = ""
        self.desc = self.desc + "<tr><h4> L2 data test </h4> </tr>"

        for i in res_l2:
            print i     
            res = "pass"
            if (float(i[2])<=0):
                res = "fail"
                res_des = "%s文件未完成传输" % i[0]
            else:
                res_des = "%s文件传输速度%s" % (i[0], i[2])
                if (i[3]!=-1 and i[3]!= -2):
                    res_des = res_des + "标准差为%f" % i[3]


            self.desc = self.desc +"<tr>"+ "L2 传输测试" + res_des + "</tr>"
            self.a.g_report_test(testsuit, i[0] + "\t文件大小" + i[1] , res, res_des)
        try: #如果启用privision test，self.testname存在，否则要单独设置存储的文件名称
            assert self.testname 
        except:
            self.testname = str(time.time.now())


        self.save_res()
        return res_l2

if __name__ == "__main__":
    x = logMon_check()
    x.res_process("log", "test_II")
    #print x.get_l2_data("log//ue_client_1461233499.log.txt")       
    x.res_l2()
