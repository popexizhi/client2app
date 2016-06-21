# python py_lib.py -cfg=alone.cfg -relay
# -*- coding:utf8 -*-
#!/usr/bin/python

import sys, os
from ctypes import *
import ctypes
import time, socket, struct

class slim_socket():
    def __init__(self, argv, lib_path = "/home/lijie/test/lib_nexus/lib/libNexus_Engine_SDK.so"):
        self.argv = argv
        self.lib_path_so = "export LD_LIBRARY_PATH=lib/$export LD_LIBRARY_PATH" 
        #os.system(self.lib_path_so)

        self.so = ctypes.CDLL(lib_path)
        self.log("len self.argv is %d" % len(self.argv))
        self.log("self.argv is %s" % str(self.argv))

    def log(self, message, meg_doc = ""):
        print "*** " * 20
        print "[slim_socket]\t%s\t%s " % (meg_doc , str(message))

    def NexusLibMainEntry(self):
        self.NexusLibMainEntry_WT = 10 #10 s
        num_numbers = len(self.argv)
        array_type = ctypes.c_char_p * num_numbers
        self.log("array_type is %s "% str(array_type))
        
        self.so.NexusLibMainEntry(ctypes.c_int(num_numbers), array_type(*self.argv))
        time.sleep(self.NexusLibMainEntry_WT)

    def SlimSocket(self):
        self.SlimSocket_WT = 5 # 1 s
        self.fd_ = self.so.SlimSocket(socket.AF_INET, socket.SOCK_STREAM, ctypes.c_int(0))
        time.sleep(self.SlimSocket_WT)
        self.log(self.fd_, "SlimSocket res fd_ is")

        assert self.fd_ > 0
        return self.fd_
    
    def SlimBind(self , port_i = 9000, host_id_i = 2104 ):
        self.SlimBind_WT = 1 # 1 s
        self.port_i = port_i
        self.host_id_i = host_id_i
        sockaddr_in = struct.pack("HHi",socket.AF_INET, socket.ntohs(self.port_i), socket.htonl(self.host_id_i))
        sockaddr_in_len = 16 #16 is long for sockaddr_in 
        self.c_addr_in_len = ctypes.c_int(sockaddr_in_len)

        self.log("sockaddr_in is %s; sockaddr_in len is %s" % (repr(sockaddr_in), len(sockaddr_in)))
        self.log("fd_ is " + str(self.fd_ ) )
        res = self.so.SlimBind(self.fd_, sockaddr_in, 16 )
        time.sleep(self.SlimBind_WT)
        self.log(res, " SlimBind res is ")
        assert res > -1

    def SlimConnect(self, s_port = 3000, s_host_id_i = 2102 ):
        self.SlimConnect_WT = 1 # 1s
        self.s_port_i = s_port
        self.s_host_id_i = s_host_id_i
        sockaddr_in = struct.pack("HHi",socket.AF_INET, socket.ntohs(self.s_port_i), socket.htonl(self.s_host_id_i))
        sockaddr_in_len = 16 #16 is long for sockaddr_in 
        self.s_addr_in_len = ctypes.c_int(sockaddr_in_len)        
        
        self.log("[SlimConnect] \t sockaddr_in is %s; sockaddr_in len is %s" % (repr(sockaddr_in), len(sockaddr_in)))
        assert self.fd_

        res = self.so.SlimConnect(self.fd_, sockaddr_in, self.s_addr_in_len )
        time.sleep(self.SlimConnect_WT)
        self.log(res, "SlimConnect res is")
        assert res > -1

    def SlimSend(self, send_str):
        assert self.fd_
        self.c_send_str_length_i = ctypes.c_int(len(send_str))
        self.c_char_p_send_str = ctypes.c_char_p(send_str)
        
        self.log("[SlimSend] start send ...")
        send_num = self.so.SlimSend(self.fd_, self.c_char_p_send_str, self.c_send_str_length_i, 0)
        self.log("send_num is %d" % send_num)
       
        res = ""
        if send_num < self.c_send_str_length_i:
            c_send_str_length_i = ctypes.c_int(len(send_str) - send_num)
            self.log("new send length is %s" % str(c_send_str_length_i))

            res = send_str[send_num:-1]
            self.log("new res is %s" % res)
            c_char_p_str = ctypes.c_char_p(res)
            send_e_len = self.so.SlimSend(self.fd_, c_char_p_str, c_send_str_length_i, 0)

            send_num = send_num + send_e_len
            

        self.log("[SlimSend] end send ...")
        return send_num

if __name__ == "__main__":
    cmd = ["py_lib.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
    x = slim_socket(cmd)
    x.NexusLibMainEntry()
    x.SlimSocket()
    x.SlimBind()
    x.SlimConnect()
    data = "hi ,i am here .Unu wir statas vi!"
    x.SlimSend(data)
    while 1:
        time.sleep(1)

