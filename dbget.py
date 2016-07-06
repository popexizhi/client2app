#-*-coding:utf8-*-
import MySQLdb
class db_mod():
    def __init__(self, db_name = "nexus_eap" , ip = "192.168.1.44", user = "slim", pd = "password"):
        self.db = MySQLdb.connect(ip ,user, pd, db_name, port=3306, charset="utf8")
        self.cursor = self.db.cursor()        

    def get_pin(self, num = 1016):
        sql = 'SELECT email, application_id, pin, pinhash from portal_host_pin where application_id = %d;' % num
        res = self.select(sql)
        self.log("select res is %s (SQL is %s)" % (str(res), str(sql))) 
        return res

    def select(self, sql):        
        res = self.cursor.execute(sql)
        # Fetch a single row using fetchone() method.
        #data = self.cursor.fetchone()
        data = self.cursor.fetchall()
        # disconnect from server
        self.db.close()
        return data
    def log(self, message):
        print "*** " * 20
        print "[db_mod] %s" % message

if __name__ == "__main__":
    x = db_mod()
    print x.get_pin()
