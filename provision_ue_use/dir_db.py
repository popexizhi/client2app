# -*- coding:utf8 -*-
import re, os
import sqlite3
def os_dir():
    x = []
    x_dir = {}
    for i in os.listdir("db_use"):
        if re.findall("db", i):
            x.append(i) 
            x_dir[i] = "0"
        else:
            print i
    sql = "SELECT local_host_id from target_host_info ;"
    u = {}
    err = {}
    for i in x:
        #print "** " * 5
        #print i
        conn = sqlite3.connect("db_use\\"+i)
        try:
            cursor = conn.execute(sql)
            for j in cursor:
                #print "%s host_id : %s" % (i, j[0])
                u[i] = j[0]
                cp_cmd = "cp db_use\\%s db_hostid\\npl%s.db" % (i, j[0]) 
                print cp_cmd
                os.system(cp_cmd)
                
        except:
            err[i] = "Null"
                
        conn.close()
        
    #print u
    for i in err:
        #print i
        pass
    print len(err)
    print len(u)
    print len(x)

    for i in u:
        del x_dir[i]
    print "** " * 20
    print x_dir
os_dir()        
