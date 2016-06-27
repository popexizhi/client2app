# -*- coding:utf8 -*-
import threading  
import time 
import socket  
import struct  
import os , copy 

SAVEBUFF_LEN = 1000000 #file len
WAIT_TIME = 2 * 60 # 等待此时间无数据，存储剩余内容为文件

class rec_p(threading.Thread):
    def __init__(self, fd_name, interval = 1):
        threading.Thread.__init__(self)  
        self.thread_stop = False
        self.interval = interval  
        self.rec = ""
        self.fd_name = fd_name
        self.pre_f = 0
        self.lock = threading.Lock()
        self.log_path = "sf//"

    def run(self):
        self.change_f = 0
        while not self.thread_stop:
            if len(self.rec) > SAVEBUFF_LEN :
                self.savefile()
            if self.change_f + WAIT_TIME < 0 and len(self.rec) > 0 and len(self.rec) < SAVEBUFF_LEN:
                self.save_rec()
            else:
                time.sleep(self.interval)
                self.change_f = self.change_f - 1

        self.save_rec()

    def savefile(self):
        self.change_f = 1
        old = self.rec[0:SAVEBUFF_LEN]
        f = open(self.log_path + "res_%d_%s.log" % (self.fd_name, self.pre_f), "wb")
        f.write(old)
        f.close()
        self.pre_f = self.pre_f + 1
        
        self.lock.acquire() 
        self.rec = self.rec[SAVEBUFF_LEN:-1]
        self.lock.release()

    def stop(self):
        self.thread_stop = True
        

    def save_rec(self):
        f = open(self.log_path + "res_%d_%s.log" % (self.fd_name, self.pre_f), "wb")
        
        self.lock.acquire() 
        f.write(self.rec)
        self.rec = ""
        self.lock.release() 
        self.pre_f = self.pre_f + 1 
        f.close()



    def get_rec(self, new_rec):
        self.rec = self.rec + copy.deepcopy(new_rec)
        print "[rec_p] " * 5 + " len(self.rec) is %d" % len(self.rec)


if __name__ == "__main__":
    x = rec_p()
    f = open("testfile.log","rb")
    con = f.readlines()
    f.close()
    x.start()
    for i in con:
        x.get_rec(i)
    #x.stop()
    
