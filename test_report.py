#-*- coding:utf8 -*-
import re
from os import walk
from HTMLTestRunnerx import HTMLTestRunner_ex #html 报告使用
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
        a=HTMLTestRunner_ex() #html use
        test_suit = "provision_ue"
        for i in self.get_dir_files(dir_p):
            if 1 == self.mon_all_lines(dir_p+"//"+i):
                res[i] = "pass"
                a.g_report_test(test_suit, i, res[i], "log has '"+self.ue_provision_finish +"'")
                pass_num = pass_num + 1
            else:
                res[i] = "fail"
                err_res.append(i)
                a.g_report_test(test_suit, i, res[i], "log doesn't have '"+self.ue_provision_finish + "'")


        totle = len(res)
        desc = "总测试 appserver 为 %d个 , dev 为%d 个<br /> 其中pass 完成provision的dev为 %d 个, 占%f<br />" % (totle, totle, pass_num, pass_num/float(totle))
        desc = desc + 'log 保存位置见  <a href="http://192.168.1.25/%s/log/">http://192.168.1.25/%s/log</a> <br />'  % (backup_dir, backup_dir)
        desc = desc + 'coredump 位置见 <a href="http://192.168.1.25/%s/corefile/">http://192.168.1.25/%s/corefile</a> <br />' % (backup_dir, backup_dir)
        a.set_report("%s : provision test" % backup_dir, desc )
        a.g_savefile("ue_provision_res_%s.html" % backup_dir)
        return res, err_res

    def res_l2(self, dir_p):
        res = {}
        for i in self.get_dir_files(dir_p):
            res[i] = self.get_l2_data(dir_p+"//"+i)
            #if self.get_l2_data(dir_p+"//"+i) >0 :

        return res
if __name__ == "__main__":
    x = logMon_check()
    x.res_process("log", "test_II")
    #print x.get_l2_data("log//ue_client_1461233499.log.txt")       
    #print x.res_l2("log")
