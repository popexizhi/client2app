#-*- coding:utf8 -*-
import re
from os import walk
from HTMLTestRunnerx import HTMLTestRunner_ex #html 报告使用
class logMon_check():
    def __init__(self):
        self.ue_provision_finish = "test client send finished"

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

    def res_process(self, dir_p):
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
        desc = desc + 'log 保存位置见  <a href="http://192.168.1.25/test_96/log/">http://192.168.1.25/test_96/log</a> <br />'
        desc = desc + 'coredump 位置见 <a href="http://192.168.1.25/test_96/corefile/">http://192.168.1.25/test_96/corefile</a> <br />'
        a.set_report("provision test", desc )
        a.g_savefile("ue_provision_res.html")
        return res, err_res


if __name__ == "__main__":
    x = logMon_check()
    x.res_process("log")
        
