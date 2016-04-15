import subprocess
import re, time, sys
import thread
class appserver():
    def __init__(self):
        pass

    def app_provision(self, num):
        cmd = './app_server -cfg="cfg/%d_alone.cfg" -db -server_provision' % num
        getchar = "a"
        print cmd
        self.app_log_b = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE, stdin = subprocess.PIPE)
        # Send the data and get the output
        stdout, stderr = self.app_log_b.communicate(getchar)
    
    
for i in xrange(1):
#    thread.start_new_thread(app_provision,(i+1011, ))
#    print "start ....%d" % i+1011
#    time.sleep(1)
    std = int(sys.argv[1])
    a = appserver()
    a.app_provision(i+std)
