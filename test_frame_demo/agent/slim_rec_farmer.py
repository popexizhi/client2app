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
        while not self.thread_stop:
            rec_num, res = self.socket.SlimReceive(self.fd)
            if 0 == rec_num: #SocketClose
                #关闭res_process
                self.rec_p.stop()
                self.log("[save_receive stop] fd is %d " % self.fd)
                break
            else:
                #save rec_s
                self.log("[slim_rec_farmer] res is %s" % res)
                self.rec_p.get_rec(res)
                

    def stop(self):
        self.thread_stop = True 

