#-*- encoding:utf8 -*-
#!/usr/bin/python

#from ctypes import *
import sys
from ctypes import *
import ctypes
import time, socket
import struct
#_sum = ctypes.CDLL('/home/lijie/test/py_so/libsum.so')
#_sum.add.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_char_p))
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

if __name__ =="__main__":
    print "*** " * 20 
    so = ctypes.CDLL("/home/lijie/test/lib_nexus/app_lib/lib/libAPP_Server_SDK.so") 
    so.NexusAPPMainEntry.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_char_p))
    print "*** " * 20
    print "len(sys.argv) "+ str( len(sys.argv))
    
    print "sys.argv "+str( sys.argv)
    
    num_numbers = len(sys.argv)
    array_type = ctypes.c_char_p * num_numbers
    print array_type
    #_sum.add(ctypes.c_int(num_numbers), array_type(*sys.argv))


    #L2 provision
    so.NexusAPPMainEntry(ctypes.c_int(num_numbers), array_type(*sys.argv))
    time.sleep(10)
    #server_fd = so.SlimSocket(ctypes.c_int(socket.AF_INET), ctypes.c_int(socket.SOCK_STREAM), 0) #client use
    server_fd = so.SlimSocket(socket.AF_INET, socket.SOCK_STREAM, ctypes.c_int(0))
    print "*** " * 50
    print "test socket create,server_fd=" + str(server_fd) + "\n"

    #SlimBind
    
    c_i_fd = ctypes.c_int(server_fd)
    #sockaddr_in = struct.pack("HH",socket.AF_INET, socket.ntohs(3000)) + socket.inet_aton("0.0.0.2")
    #sockaddr_in = struct.pack("b",9)+ struct.pack("HHi",socket.AF_INET, socket.ntohs(3000), socket.htonl(2102)) 
    sockaddr_in = struct.pack("HHi",socket.AF_INET, socket.ntohs(3000), socket.htonl(2102)) 
    
    print "*** " * 50
    print "sockaddr_in is "+ repr(sockaddr_in) + " [len(sockaddr_in) is " +str(len(sockaddr_in))
    res = so.SlimBind(c_i_fd, sockaddr_in , 16)#16 is long for sockaddr_in 
    print "slimBind_res is "+ str(res) 

    #SlimAccept
    listen_res = so.SlimListen(c_i_fd, ctypes.c_int(1))
    print "*** " * 50
    print "Slimlisten res is "+ str(listen_res)
    c_addr = outStructAddr()
    c_i_addr_len = 0
    print "*** " * 50
    #ctypes.POINTER(ctypes.c_char_p)
    #ctypes.c_int, ctypes.POINTER(ctypes.c_char_p)
    so.SlimAccept.argtypes= [ctypes.c_int, ctypes.POINTER(outStructAddr), ctypes.POINTER(ctypes.c_int)]
    newfd = so.SlimAccept(c_i_fd, ctypes.byref(c_addr), ctypes.byref(ctypes.c_int(c_i_addr_len)))
    print "SlimAccept newfd is "+ str(newfd) + "\t c_addr"+ repr(c_addr) + "\t len is "+ str(c_i_addr_len)
    print "c_addr is "+ str(c_addr)
    print repr(c_addr)
    print "c_addr.sin_len is "+ str(c_addr.sin_len)
    print repr(c_addr.sin_len)
    print "c_addr.sa_family is "+ str(c_addr.sa_family)
    print c_addr.sa_family
    print "c_addr.sin_port is "+ str(c_addr.sin_port)
    print c_addr.sin_port
    #print "c_addr.sin_addr_p.s_addr is "+ str(c_addr.sin_addr_p.s_addr)
    #print c_addr.sin_addr_p.s_addr
    
    so.SlimReceive.argtypes= [ctypes.c_int, ctypes.c_char_p , ctypes.c_int, ctypes.c_int]
    rcv_buf = ""
    while 1:
        rec_num = so.SlimReceive(newfd, ctypes.c_char_p(rcv_buf) , 1000, 0)
        print "$$$ " * 20
        print "rec_num is "+ str(rec_num)
        print rcv_buf
        rec_num = 0
        rcv_buf =""
        #time.sleep(1)
    
