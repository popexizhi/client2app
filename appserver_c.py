#-*- coding:utf8 -*-
import sys
from shell_con import sh_control
import thread
import time
def app_provision(num):
    a = sh_control()
    a.app_provision(num)

def start_app(std):
    for i in xrange(10):
        thread.start_new_thread(app_provision,(i + std , ))
        print "start app....%d" % int(i +std)
        time.sleep(1)

    #    a = sh_control()
    #    a.app_provision(i+std)

if __name__ == "__main__":
    std = int(sys.argv[1])
    start_app(std)
