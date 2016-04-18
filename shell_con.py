#-*- coding:utf8 -*-
import subprocess
import re, time, sys
import thread
class sh_control():
    def __init__(self):
        pass

    def app_provision(self, num):
        #self.appserver_cmd = './app_server -cfg="cfg/app_%d_alone.cfg" -db -server_provision -host="%d" ' % (num, num)
        self.appserver_cmd = './app_server.sh %d' % num
        self._com(self.appserver_cmd)

    def dev_provision(self, num):
        #self.dev_cmd = './slim_engine_test -cfg="cfg/dev_%d_alone.cfg" -db -provision -host="dev%d"  ' % (num, num)
        self.dev_cmd = './slim_engine_test.sh %d' % num
        self._com(self.dev_cmd)

    def _com(self, cmd):
        getchar = "a"
        print cmd
        self.app_log_b = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE, stdin = subprocess.PIPE)
        # Send the data and get the output
        stdout, stderr = self.app_log_b.communicate(getchar)
    
if __name__=="__main__" :
    for i in xrange(1):
    #    thread.start_new_thread(app_provision,(i+1011, ))
    #    print "start ....%d" % i+1011
    #    time.sleep(1)
        std = int(sys.argv[1])
        a = sh_control()
        a.app_provision(i+std)
        a.dev_provision(i+std)
    
