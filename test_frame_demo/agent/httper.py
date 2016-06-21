#-*-coding:utf8-*-
import urllib2
from mapping import *

class httper():
    def __init__(self, url_base = environment_map["httper"]["url"]):
        self.url_b = url_base

    def get_xml(self, f_id):
        self.type_file = ".xml"
        assert type(f_id) == type("") or type(f_id) == type(1) 
        tc_rul = self.url_b + str(f_id) + self.type_file
        con_file = urllib2.urlopen(tc_rul).read() # next 做404.502的异常处理
        
        return con_file

    def get_bfile(self, f_name):
        tc_filelist = environment_map["httper"]["file_list"]
        tc_rul = self.url_b + tc_filelist + str(f_name)
        f = open(f_name, "wb") 
        con_file = urllib2.urlopen(tc_rul).read() # next 做404.502的异常处理
        f.write(con_file)
        f.close()
        
if __name__=="__main__":
    x = httper()
    #print x.get_xml("1466129033")
    f_name = "nplServer1465202670.db"
    x.get_bfile(f_name)
