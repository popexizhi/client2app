# -*- encoding:utf8 -*-
import os, re
import time
class dirlog():
    def __init__(self, filedir="log"):
        self.dir_path = filedir

        self.res_lists = {}
        self.new_stat = []

    def now_status(self):
        for i in self.res_lists:
            res = self.res_lists[i].provision_check()
            self.new_stat.append([i, res])
        
        return len(self.new_stat)

    def logdirs(self):
        """
        1.检查dir中的全部log文件
        2.更新每个log的状态
        """
        logfile = self.get_logfiles()
        for i in logfile:
            t = logMon(i)
            self.res_lists[i] = t

    def get_logfiles(self):
        res = []
        for files in os.listdir(self.dir_path):
            if re.search("log.txt", files) >0:
                res.append(self.dir_path +"/" + files)
          
        return res

class logMon():
    def __init__(self, filepath = "ue_client_9.log.txt"):
        self.filepath = filepath
        self.readfilenum = 0

        #check log
        self.status = "OnEventDeviceStatusIndication: status"
        self.l1_pass = ["L1_Connected", "L1 PASS"]
        self.l2_pass = ["Completed", "L2 PASS"]

        self.checkhostid = "host_id=\d+"
        self.status_list = []

    def provision_check(self):
        """ 
        1.读取self.filepath未检查内容
        2.检查self.con中是否包含要检查的内容
        """
        host_id = -1
        if 1 == self.get_unread_line(self.filepath):
            res = self.check_status()
            if self.l2_pass[1] == res :
                host_id = self.check_host_id()
            
            print self.filepath + "\t: \t" + res + "\t host_id:\t" + self.host_id 
        
        return res, host_id    
    
    def check_status(self):
        """ 
        从self.con中检查 self.status
        """
        assert self.con
        res = "None"
        for i in self.con:
            if re.search(self.status, i) > 0:
                x = re.split('[\[ \]]', i)
                #print x[8] + "\t" + x[-1]
                self.status_list.append((x[8] ,x[-1]))
                if re.search(self.l1_pass[0], x[-1]) >0:
                    #print self.l1_pass
                    res = self.l1_pass[1]
                if re.search(self.l2_pass[0], x[-1]) >0:
                    #print self.l2_pass
                    res = self.l2_pass[1]

        #print self.status_list
        return res
    
    def check_host_id(self):
        """
        get host_id
        """
        self.host_id = ""
        assert self.con
        for i in self.con:
            res = re.findall(self.checkhostid, i) 
            if 1 == len(res):
               self.host_id = res[0]
            if len(res) > 0:
               #ue中的host_id 过多,next 做异常处理
               assert 1 == len(res) 
        return self.host_id

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
            if re.search(self.filepath, con):
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
                if re.search(self.filepath, i):
                    res = 0
                    break
        return res
        

if __name__ == "__main__":
    #x = logMon("log/ue_client_0.log.txt")
    #x.provision_check()
    y = dirlog("log")
    y.logdirs()
    print y.now_status()

