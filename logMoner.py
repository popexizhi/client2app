#-*- coding:utf8 -*-
#http://www.pythonclub.org/python-files/last-line
#http://code.activestate.com/recipes/578095/
import os, re
import time
from datetime import datetime
from dbget_insert import db_mod #存储到mysql中

class logMon():
    def __init__(self):
        self.app_log_provision_finish = "App Server Provision finished"
        self.readfilenum = 0
        self.search_list = {"sta": " start get", "end": " end get"} #开始结束标记
        self.search_list["kind"] = r"filename:.*;filelength:\d+" #类型描述特征
        self.search_list["kind_get"] = r":.*;" #类型描述特征中识别方式,当前识别出两个分组
        self.search_list["usetime"] = r"\[.*?\]" #时间描述方式,懒惰方式匹配
          
    def _get_datatime(self, str_i):
        """date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        #[2016/05/03/18/10/51/281:195]
        """
        
        str_i = re.sub("\[|:|\]", "", str_i)
        date_object = datetime.strptime(str_i, "%Y/%m/%d/%H/%M/%S/%f")
        return date_object

    def _search_list(self, inputfile):
        """通过self.search_list做模式识别
        识别过程为:
        0.处理inputfile添加包含全部kind的line到res_list中 _get_res_list(fileneam)
        1.kind start 识别kind是否有此类型没有时添加 _rearch_kind(kind)
        2.kind start 中 usetime_sta 识别为start time
        3.kind end 中usetime_end 识别为end time
        4.做res_list添加[kind , start time, end time, filename, filelength, usetime, average_speed]
        5.计算标准差std_list
        """
        #0.处理inputfile添加包含全部kind的line到res_list中
        self._get_res_list(inputfile)
        try:
            assert self.res_list #执行后一定存在此列表
        except:
            print "no l2 data" #app_server.log.txt中无目标的L2data,退出处理过程
            return -10

        
        #1.self.res_list 识别kind并添加self.kind_list  _rearch_kind()
        self._rearch_kind()
        print "kind_list len is " + str( len(self.kind_list))
        print "res_list len is " + str( len(self.res_list))
        print "res_list_end len is " + str( len(self.res_list_end))

        #3.kind end 中usetime_end 识别为end time
        self._rearch_end_time()

        #4.做res_list添加[kind , start time, end time, filename, filelength, usetime, average_speed]
        self._save_res_list()

        #5.计算标准差std_list
        return self.std_list()
    def std_list(self):
        """
        计算标准差std_list
        """
        assert self._res_list
        #save self._res_list
        save_db = db_mod()
        std_res_list = []
        for i in self._res_list:
            print i
            filename = i.split(",")[0]
            filelength = i.split(",")[1]
            use_time = re.sub("'","",i.split(",")[4])
            std = save_db._std_use_time(filename, filelength, use_time)
            print std
            std_res_list.append([filename, filelength, use_time, std])
        self.statistics_update()
                
        save_db._close()

        return std_res_list

    def statistics_update(self):
        """ 将self._res_list内容在statistics中更新
        """
        print "*" * 20 + "statistics_update"
        save_db = db_mod()
        for i in self._res_list:
            filename = i.split(",")[0]
            filelength = i.split(",")[1]
            save_db._statistics(filename+","+filelength)
            

        print "*" * 20 + "statistics_update end"    
    def _save_res_list(self):
        """
        4.做res_list添加[kind , start time, end time, filename, filelength, usetime, average_speed]
        """
        assert self.kind_list
        self._res_list = []
        for x in self.kind_list:
            filename, filelength = x.split(";")
            sta_time, end_time = self.kind_list[x]
            filename = re.sub("filename:", "", filename)
            filelength = int(re.sub("filelength:", "", filelength) )
            use_time_s = end_time - sta_time
            average_speed = filelength / use_time_s.total_seconds()
            #print filename, filelength, sta_time, end_time, use_time_s, average_speed
            data = "'%s',%d,'%s','%s','%s',%f" % (filename, filelength, str(sta_time), str(end_time), str(use_time_s.total_seconds()), average_speed)
            self._res_list.append(data)
        
        #save self._res_list
        save_db = db_mod()

        for data in self._res_list:
            print data
            print save_db.insert(data)

        save_db._close()

    def update_statistics(self):
        save_db = db_mod()
        for i in self._res_list:
            filename_length = """%s, %s""" % (i.split(",")[0], i.split(",")[1])
            save_db._statistics(filename_length)
            
    def _rearch_kind(self):
        """1.self.res_list 识别kind并添加self.kind_list
           2.kind start 中 usetime_sta 识别为start time
        """
        assert self.res_list
        self.kind_list = {}
        for i in self.res_list:
            kind = re.findall(self.search_list["kind"], i)
            print kind
            assert 1 == len(kind) #如果存在多分组请再处理，这里没有考虑
            start_time = re.findall(self.search_list["usetime"], i)
            start_time_data_time = self._get_datatime(start_time[1])
            #print start_time, start_time_data_time
            assert 5 == len(start_time) #使用第二分组内容为时间，如果修改self.search_list["usetime"]，请修改此为止
            self.kind_list[kind[0]] = (start_time_data_time, 0)
       
    def _rearch_end_time(self):
        """ 3.kind end 中usetime_end 识别为end time """
        assert self.kind_list
        for i in self.res_list_end:
            kind = re.findall(self.search_list["kind"], i)
            print kind
            assert 1 == len(kind) #如果存在多分组请再处理，这里没有考虑
            assert self.kind_list[kind[0]] #如果不存在此文件将end结果视为非法步骤
            end_time = re.findall(self.search_list["usetime"], i) 
            end_time_data_time = self._get_datatime(end_time[1])
            #print end_time[1], end_time_data_time
            assert 5 == len(end_time) #使用第二分组内容为时间，如果修改self.search_list["usetime"]，请修改此为止
            start_time = self.kind_list[kind[0]][0]
            self.kind_list[kind[0]] = (start_time, end_time_data_time)
            print self.kind_list[kind[0]][1] - self.kind_list[kind[0]][0]
            

    def _get_res_list(self, inputfile):
        """处理inputfile添加包含全部kind的line到res_list中 """
        #前置条件
        assert self.search_list["kind"]
        assert self.search_list["sta"]
        
        filepath = open(inputfile)
        self.res_list = []
        self.res_list_end = []
        search_list = self.search_list["kind"] +".*"+ self.search_list["sta"]
        search_list_end = self.search_list["kind"] +".*"+ self.search_list["end"]
        num = 0
        while True:
            i = filepath.readline()
            num = num + 1
            if not i: break
            if re.search(search_list, i):
                self.res_list.append(i)
            if re.search(search_list_end, i):
                self.res_list_end.append(i)
            #print num
        filepath.close()


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
    x.mon_provision()
    print x._search_list("app_server.log.txt")
    #x.update_statistics()


