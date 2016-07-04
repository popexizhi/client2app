#-*- coding:utf8 -*-
#!/usr/bin/python

import time
from slimtest import slim_socket
from g_db import g_db
from rec_process import rec_p
import threading
from slim_rec_farmer import slim_rec_farmer

class slim_server():
    def __init__(self):
        self.socket = None
        self.g_db = g_db()


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
        self.cfd_list = {}
        while 1:
            self.socket.SlimListen(2)
            fd_ = self.socket.SlimAccept()
            print "**-##" * 20
            print "fd_ is %d" % fd_
            
            self.cfd_list[fd_] = slim_rec_farmer(fd_, self.socket)
            self.cfd_list[fd_].start()



if __name__ == "__main__":
    s = slim_server()
    s.start_server()
    s.run()
