# -*- coding:utf8 -*-
import time
from slimtest import slim_socket

class slim_client():
    def __init__(self):
        self.socket = None
    
    def start_client(self):
        """
        cmd = ["py_lib.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
        x = slim_socket(cmd)
        x.NexusLibMainEntry()
        x.SlimSocket()
        x.SlimBind()
        x.SlimConnect()

        """
        cmd = ["py_lib.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
        self.socket = slim_socket(cmd)
        self.socket.NexusLibMainEntry()
        self.socket.SlimSocket()
        self.socket.SlimBind()
        self.socket.SlimConnect()

    def send_data(self, data = "hi ,i am here .Unu wir statas vi!"):
        """
        data = "hi ,i am here .Unu wir statas vi!"
        x.SlimSend(data)
        while 1:
            time.sleep(1)
        """
        assert self.socket
        
        self.socket.SlimSend(data)
        self.socket.log(" send data is pass " * 20)

if __name__ == "__main__":
    a = slim_client()
    a.start_client()
    a.send_data()
