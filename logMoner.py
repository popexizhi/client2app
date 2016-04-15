#http://www.pythonclub.org/python-files/last-line
#http://code.activestate.com/recipes/578095/
import os, re
import time
class logMon():
    def __init__(self):
        self.app_log_provision_finish = "App Server Provision finished"

    def get_last_line(self, inputfile) :
        filesize = os.path.getsize(inputfile)
        blocksize = 1024
        dat_file = open(inputfile, 'rb')
        last_line = ""
        if filesize > blocksize :
            maxseekpoint = (filesize // blocksize)
            dat_file.seek((maxseekpoint-1)*blocksize)
        elif filesize :
            #maxseekpoint = blocksize % filesize
            dat_file.seek(0, 0)
        lines =  dat_file.readlines()
        if lines :
            last_line = lines[-1].strip()
        #print "last line : ", last_line
        dat_file.close()
        return last_line
   
    def mon_provision(self, applog = "app_server.log.txt"):
        while 1:
            con = self.get_last_line(applog)
            if re.search(self.app_log_provision_finish, con):
                print "appserver provision is ok ..."
                return 0 # appserver provision is ok
            else:
                time.sleep(1)


if __name__ == "__main__":
    x = logMon()
    x.mon_provision()



