#-*- coding:utf8 -*-
#!/usr/bin/python

import time
from slimtest import slim_socket
from g_db import g_db
from rec_process import rec_p
import threading

class slim_server():
    def __init__(self):
        self.socket = None
        self.g_db = g_db()
        self.rec_file_list = {} #rec_p dir
        self.lock = threading.Lock()

    def start_server(self, db_num = 1465202670):
        """
        cmd = ["slimtest.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
        server_lib = "/home/lijie/test/lib_nexus/app_lib/lib/libAPP_Server_SDK.so"
        x = slim_socket(cmd, server_lib)
        x.NexusAPPMainEntry()
        x.SlimSocket()
        x.SlimBind(3000, 2102)
        x.SlimListen()
        x.SlimAccept()       
        """
        cmd = ["slim_server.py", '-cfg=alone_with_provision.cfg', "-host=%d" % db_num]
        server_lib = "/home/lijie/test/lib_nexus/app_lib/lib/libAPP_Server_SDK.so"
        db_path = "nplServer%d.db" % db_num
        print "db_path is %s " % db_path
        host_id = self.g_db.get_hostid(db_path)
        self.socket = slim_socket(cmd, lib_path = server_lib)
        self.socket.NexusAPPMainEntry()
        self.socket.SlimSocket()
        assert host_id
        self.socket.SlimBind(3000, host_id_i = host_id)


    def run(self):
        #self.rec_file.start()
        self.list_fd = {}
        self.list_fd_res = {}
        self.save_res_list = {}
        self.save_res_run = {}
        while 1:
            self.socket.SlimListen(2)
            fd_ = self.socket.SlimAccept()
            print "**-##" * 20
            print "fd_ is %d" % fd_
            
            self.list_fd[fd_] = threading.Thread(target = self.run_receive, args=(fd_, ))

            #监控rec结果开始
            self.rec_file_list[fd_] = rec_p(fd_)
            self.rec_file_list[fd_].start()
            #接受开始
            self.list_fd_res[fd_] = "" 
            self.list_fd[fd_].start()            
            #转储开始
            self.save_res_run[fd_] = 1
            self.save_res_list[fd_] = threading.Thread(target = self.save_res, args=(fd_, ))
            self.save_res_list[fd_].start()
            

            print "list_fd[fd_] is " + str(self.list_fd[fd_])
            print "self.rec_file_list[fd_] is " + str(self.rec_file_list[fd_])
            print "self.save_res_list[fd_] is " + str(self.save_res_list[fd_])

    def run_receive(self, fd_):
        print "** **" * 20
        print "[run_receive] fd is %d start .." % fd_            
        while 1:
            print "[run_receive] " * 5
            res = self.socket.SlimReceive(fd_, self.list_fd_res[fd_])
            if 0 == res: #SockeClose
                #关闭save_res_list 和 self.rec_file_list[fd_]
                self.save_res_stop(fd_)
                self.rec_file_list[fd_].stop()
                break

    def save_res_stop(self, fd_):
        self.save_res_run[fd_] = 0

    def save_res(self, fd_):
        print "** **" * 20
        print "[save_res] fd is %d start .." % fd_

        while 1:
            #self.list_fd_res[fd_]
            print "===" * 20
            print "len(self.list_fd_res[fd_]) is %d" % len(self.list_fd_res[fd_])
            if len(self.list_fd_res[fd_]) > 0:
                self.lock.acquire() 
                print "*** " * 20
                print "get data is %s" % self.list_fd_res[fd_]
                self.rec_file_list[fd_].get_rec(self.list_fd_res[fd_])
                self.list_fd_res[fd_] = ""
                
                self.lock.release() 
            if 0 == self.save_res_run[fd_] :
                print "[save_res] stop " * 20
                break
                
            time.sleep(2)

if __name__ == "__main__":
    s = slim_server()
    s.start_server()
    s.run()
