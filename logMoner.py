#-*- coding:utf8 -*-
#http://www.pythonclub.org/python-files/last-line
#http://code.activestate.com/recipes/578095/
import os, re
import time
class logMon():
    def __init__(self):
        self.app_log_provision_finish = "App Server Provision finished"
        self.readfilenum = 0
        

    def get_l2_data(self, inputfile):
        """返回ue的log中最后一行的send data的number """
        res = 0
        
        filepath = open(inputfile)
        con = filepath.readlines()
        filepath.close()
        
        search_l2 = re.compile(r'\*{6} (\d+) total')
        for i in con:
            pat_search = search_l2.search(i)
            if pat_search != None:
                res = int(pat_search.group(1))    
        
        return res
                

    def get_last_line(self, inputfile) :
        filesize = os.path.getsize(inputfile)
        blocksize = 1024
        dat_file = open(inputfile, 'rb')
        last_line = ""
        if filesize > blocksize :
            maxseekpoint = (filesize // blocksize)
            dat_file.seek((maxseekpoint-1)*blocksize)
        elif filesize :
            #maxseekpoint = blocksize % filesize
            dat_file.seek(0, 0)
        lines =  dat_file.readlines()
        if lines :
            last_line = lines[-1].strip()
        #print "last line : ", last_line
        dat_file.close()
        return last_line
   
    def mon_provision_last_line(self, applog = "app_server.log.txt"):
        while 1:
            con = self.get_last_line(applog)
            if re.search(self.app_log_provision_finish, con):
                print "appserver provision is ok ..."
                return 0 # appserver provision is ok
            else:
                time.sleep(1)

    def mon_provision(self, applog = "app_server.log.txt"):
        res = 1
        while 1:
            res = self.get_unread_line(applog)
            if 0 == res:
                print "appserver provision is ok ..."
                break
            print "Wait .. .. App Server Provision does not finished"
            time.sleep(1)

    def get_unread_line(self, inputfile):
        filepath = open(inputfile)
        con = filepath.readlines()
        filepath.close()
        lines = len(con)
        res = 1
        if lines > self.readfilenum:
            self.con = con[self.readfilenum: lines]
            for i in self.con:
                if re.search(self.app_log_provision_finish, i):
                    res = 0
                    break
        return res
        

if __name__ == "__main__":
    x = logMon()
    #x.mon_provision()
    print x.get_l2_data("log//ue_client_1461233499.log.txt")


