#-*- coding:utf8 -*-
import sys
from shell_con import sh_control



if __name__ == "__main__":
    for i in xrange(1):
    #    thread.start_new_thread(app_provision,(i+1011, ))
    #    print "start ....%d" % i+1011
    #    time.sleep(1)
        std = int(sys.argv[1])
        a = sh_control()
        a.app_provision(i+std)
        
