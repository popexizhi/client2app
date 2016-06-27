# -*- coding:utf8 -*-
#
#

import threading
from rec_process import rec_p
from slimtest import slim_socket

class slim_rec_farmer(threading.Thread):
    def __init__(self, fd, socket):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.fd = fd
        self.socket = socket
        self.rec_p = rec_p(fd)  #save rec use

    def log(self, mes):
        self.socket.log(mes)
    
    def run(self):
        #start rec_p
        self.rec_p.start()

        #start save_receive and save rec into res
        self.save_receive()

    def save_receive(self):
        self.log("[run_receive] " * 5)
        rec_s = ""
        while not self.thread_stop:
            res = self.socket.SlimReceive(self.fd, rec_s)
            if 0 == res: #SocketClose
                #关闭res_process
                self.rec_p.stop()
                self.log("[save_receive stop] fd is %d " % self.fd)
                break
            else:
                #save rec_s
                self.rec_p.get_rec(rec_s)

    def stop(self):
        self.thread_stop = True 

