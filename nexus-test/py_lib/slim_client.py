# -*- coding:utf8 -*-
# 运行前添加如下命令 ，加载so库路径
#   export LD_LIBRARY_PATH=lib/$export LD_LIBRARY_PATH
# 
import time
from slimtest import slim_socket
from g_db import g_db
class slim_client():
    def __init__(self):
        self.socket = None
        self.g_db = g_db()
        
    def start_client(self, db_num = 1465202670):
        """
        cmd = ["py_lib.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
        x = slim_socket(cmd)
        x.NexusLibMainEntry()
        x.SlimSocket()
        x.SlimBind()
        x.SlimConnect()

        """
        cmd = ["py_lib.py", '-cfg=alone_with_provision.cfg', "-host=%d" % db_num]
        db_path = "npl%d.db" % db_num
        host_id = self.g_db.get_hostid(db_path) #从db中读取本地host_id
        target_host_id = self.g_db.get_target_hostid(db_path)#从db中读取server host_id

        self.socket = slim_socket(cmd)
        self.socket.NexusLibMainEntry()
        self.socket.SlimSocket()
        assert host_id
        self.socket.SlimBind(host_id_i = host_id)
        assert target_host_id
        self.socket.SlimConnect(s_host_id_i = target_host_id)

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
