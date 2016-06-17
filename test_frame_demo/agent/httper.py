#-*-coding:utf8-*-
import urllib2

class httper():
    def __init__(self, url_base = "http://192.168.1.25/testcase_use/"):
        self.url_b = url_base

    def get_xml(self, f_id):
        self.type_file = ".xml"
        assert type(f_id) == type("") or type(f_id) == type(1) 
        tc_rul = self.url_b + str(f_id) + self.type_file
        con_file = urllib2.urlopen(tc_rul).read() # next 做404.502的异常处理
        
        return con_file

if __name__=="__main__":
    x = httper()
    print x.get_xml("1466129033")
