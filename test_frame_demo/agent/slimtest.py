# python py_lib.py -cfg=alone.cfg -relay
# -*- coding:utf8 -*-
#!/usr/bin/python

import sys, os, copy
from ctypes import *
import ctypes
import time, socket, struct

class in_addr(Structure):
 _fields_= [
  ('s_addr', ctypes.c_uint),]

class outStructAddr(Structure):
 _fields_= [
    ('sin_len', ctypes.c_char),
    ('sa_family', ctypes.c_ushort),
    ('sin_port', ctypes.c_ushort),
    ('sin_addr_p', ctypes.POINTER(in_addr)),
    ('sin_zero', ctypes.c_char*8),
    ]

class slim_socket():
    def __init__(self, argv, lib_path = "/home/lijie/test/lib_nexus/lib/libNexus_Engine_SDK.so"):
        self.argv = argv
        self.lib_path_so = "export LD_LIBRARY_PATH=lib/$export LD_LIBRARY_PATH" 
        #os.system(self.lib_path_so)
        
        self.so = ctypes.CDLL(lib_path)
        self.log("lib_path is %s" % lib_path)
        self.log("len self.argv is %d" % len(self.argv))
        self.log("self.argv is %s" % str(self.argv))
    
    def log(self, message, meg_doc = ""):
        sp = "*** " * 20
        mes ="[slim_socket]\t%s\t%s " % (meg_doc , str(message))
        print sp
        print mes
        f = open("slimlog.log", "a")
        f.write(sp + "\n")
        f.write(mes + "\n")
        f.close()

    def NexusLibMainEntry(self):
        """client use"""
        self.NexusLibMainEntry_WT = 10 #10 s
        num_numbers = len(self.argv)
        array_type = ctypes.c_char_p * num_numbers
        self.log("array_type is %s "% str(array_type))
        
        self.so.NexusLibMainEntry(ctypes.c_int(num_numbers), array_type(*self.argv))
        time.sleep(self.NexusLibMainEntry_WT)

    def NexusAPPMainEntry(self):
        """sever use """
        self.NexusAPPMainEntry_WT = 10 #10s
        num_numbers = len(self.argv)
        array_type = ctypes.c_char_p * num_numbers
        self.log("array_type is %s "% str(array_type))

        #provision
        #self.so.NexusAPPMainEntry.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_char_p))
        self.so.NexusAPPMainEntry(ctypes.c_int(num_numbers), array_type(*self.argv))        
        time.sleep(self.NexusAPPMainEntry_WT)

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
    
    def SlimListen(self, listen_num = 1):
        """serever use  """
        self.SlimListen_WT = 1 # 1s
        assert self.fd_
        res = self.so.SlimListen(self.fd_, ctypes.c_int(listen_num))
        time.sleep(self.SlimListen_WT)
        self.log("listen res is %d" % res)
        assert res > -1
    
    def SlimAccept(self):
        """server accept """
        self.SlimAccept_WT = 1 # 1s
        assert self.fd_
    
        c_addr = outStructAddr()
        c_i_addr_len = 0
        self.so.SlimAccept.argtypes= [ctypes.c_int, ctypes.POINTER(outStructAddr), ctypes.POINTER(ctypes.c_int)]
        self.newfd = self.so.SlimAccept(self.fd_, ctypes.byref(c_addr), ctypes.byref(ctypes.c_int(c_i_addr_len)))        
        
        log_use = "SlimAccept newfd is "+ str(self.newfd) + "\t c_addr"+ repr(c_addr) + "\t len is "+ str(c_i_addr_len)
        self.log(log_use)
        self.log("c_addr is ")
        self.log(c_addr)
        self.log("c_addr.sin_len is ")
        self.log(c_addr.sin_len)
        self.log("c_addr.sa_family is ")
        self.log(c_addr.sa_family)
        self.log("c_addr.sin_port is ")
        self.log(c_addr.sin_port)
        time.sleep(self.SlimAccept_WT)

        return self.newfd

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
        if send_num < len(send_str):
            c_send_str_length_i = ctypes.c_int(len(send_str) - send_num)
            self.log("new send length is %s" % str(c_send_str_length_i))

            res = send_str[send_num:-1]
            self.log("new res is %s" % res)
            c_char_p_str = ctypes.c_char_p(res)
            send_e_len = self.so.SlimSend(self.fd_, c_char_p_str, c_send_str_length_i, 0)

            send_num = send_num + send_e_len
            

        self.log("[SlimSend] end send ...")
        return send_num
    
    def SlimClose(self, nfd):
        """ close fd """
        assert nfd
        self.log("[SlimClose] fd is %d" % nfd)
        res = self.so.SlimClose(nfd)
        self.log("[SlimClose] res is %s" % str(res))
        return res

    def SlimReceive(self, nfd):
        """ get receive """
        self.log("[SlimReceive]")
        fd_ = nfd
        self.so.SlimReceive.argtypes= [ctypes.c_int, ctypes.c_char_p , ctypes.c_int, ctypes.c_int]

        
        rcv_buf = c_char_p(" "*1000)
        self.log("[SlimReceive]")
        rec_num = self.so.SlimReceive(fd_, rcv_buf , 1000, 0) # next这里固定读取1000 ,没有做全都读取的处理
        self.log("[SlimReceive]")
        self.log("rcv_buf is %s" % rcv_buf.value)
        self.log("rec_num is %d" % rec_num)
        #被动关闭处理
        if 0 == rec_num:
            self.SlimClose(fd_)
            self.log("[SlimSocket %d is closed ]" % fd_)
            return rec_num, ""
        res = copy.deepcopy(rcv_buf.value)
         
        #res_da = copy.deepcopy(res[0:rec_num])
        self.log("res is %s" % res)
        return rec_num, res


def test_client():
    cmd = ["slimtest.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
    x = slim_socket(cmd)
    x.NexusLibMainEntry()
    x.SlimSocket()
    x.SlimBind()
    x.SlimConnect()
    data = "hi ,i am here .Unu wir statas vi!"
    x.SlimSend(data)
    while 1:
        time.sleep(1)

def test_server():
    cmd = ["slimtest.py", '-cfg=alone_with_provision.cfg', "-host=1465202670"]
    server_lib = "/home/lijie/test/lib_nexus/app_lib/lib/libAPP_Server_SDK.so"
    x = slim_socket(cmd, server_lib)
    x.NexusAPPMainEntry()
    x.SlimSocket()
    x.SlimBind(3000, 2102)
    x.SlimListen()
    x.SlimAccept()
    while 1:
        res_data = x.SlimReceive()
        x.log("get data len is %d" % len(res_data) )
        x.log("con is %s" % str(res_data))

if __name__ == "__main__":
    #test_client()
    test_server()
