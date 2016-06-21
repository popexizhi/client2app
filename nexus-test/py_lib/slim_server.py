#-*- coding:utf8 -*-
#!/usr/bin/python

import time
from slimtest import slim_socket

class slim_server():
    def __init__(self):
        self.socket = None

    def start_server(self):
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
        cmd = ["slim_server.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
        server_lib = "/home/lijie/test/lib_nexus/app_lib/lib/libAPP_Server_SDK.so"
        self.socket = slim_socket(cmd, lib_path = server_lib)
        self.socket.NexusAPPMainEntry()
        self.socket.SlimSocket()
        self.socket.SlimBind(3000, 2102)
        self.socket.SlimListen()
        self.socket.SlimAccept()

    def run(self):
        while 1:
            res_data = self.socket.SlimReceive()
            self.socket.log("get data is %s" % res_data)

if __name__ == "__main__":
    s = slim_server()
    s.start_server()
    s.run()
