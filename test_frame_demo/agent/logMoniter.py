#-*- coding:utf8 -*-
import re, os, sys
import time
PASS = "pass"
FALSE = "null"
ERR = "" #?查找结果不完整需要返回吗?
class logMonitor():
    def __init__(self, path = "./"):
        self.rec_path = path

    def check_file(self, pre_filename):
        self.pre = pre_filename
        f = open(self.pre, "rb")
        self.con = f.readlines()
        f.close()

        return self._diff_con(self.con)
        
    def _diff_con(self, format_con_list):
        r = FALSE
        print format_con_list 
        format_re = re.compile(format_con_list[0])
        for i in os.listdir(self.rec_path):
            if re.findall("^res_", i):
                #print "rec file name is %s" % i
                f = open(self.rec_path + i, "rb")
                con = f.readlines()
                f.close()
                for j in con:
                    #print "\t con is %s" % j
                    res = format_re.findall(j)
                    #print res
                    if len(res) > 0:
                        print "rec file name is %s" % i
                        #[next] 比较全部的文件内容，返回是否一致
                        r = PASS
        return r
if __name__ == "__main__":
    x = logMonitor()
    print x.check_file("send_data.log")
