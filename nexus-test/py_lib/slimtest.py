# python py_lib.py -cfg=alone.cfg -relay
# -*- encoding:utf8 -*-
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

    def SlimConnect(self):
        pass

     


if __name__ == "__main__":
    cmd = ["py_lib.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
    x = slim_socket(cmd)
    x.NexusLibMainEntry()
    x.SlimSocket()
    x.SlimBind()
    while 1:
        time.sleep(1)

