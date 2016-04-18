#-*- coding:utf8 -*-
import sys
from shell_con import sh_control
import thread
import time
def app_provision(num):
    a = sh_control()
    a.app_provision(i+std)


if __name__ == "__main__":
    std = int(sys.argv[1])
    for i in xrange(1):
    #    thread.start_new_thread(app_provision,(i + std , ))
    #    print "start ....%d" % int(i +std)
    #    time.sleep(1)

        a = sh_control()
        a.app_provision(i+std)
        
