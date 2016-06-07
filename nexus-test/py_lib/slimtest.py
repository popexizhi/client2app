# python py_lib.py -cfg=alone.cfg -relay
# -*- encoding:utf8 -*-
#!/usr/bin/python

import sys
from ctypes import *
import ctypes
import time

class slim_socket():
    def __init__(self, argv, lib_path = "/home/lijie/test/lib_nexus/libNexus_Engine_SDK.so"):
        self.argv = argv
        
        self.so = ctypes.CDLL(lib_path)
        self.log("len self.argv is %d" % len(self.argv))
        self.log(" self.argv is %s" % str(self.argv))

    def log(self, message):
        print "*** " * 20
        print "[slim_socket]\t " + str(message)

    def nexusLibMainEntry(self):
        pass

if __name__ == "__main__":
    cmd = ["py_lib.py", "-cfg=alone.cfg", "-relay"]
    x = slim_socket(cmd)

