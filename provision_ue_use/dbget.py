#-*-coding:utf8-*-
import MySQLdb
class db_mod():
    def __init__(self, db_name = "nexus_eap" , ip = "192.168.1.55", user = "root", pd = "password"):
        self.db = MySQLdb.connect(ip ,user, pd, db_name, port=3306, charset="utf8")
        self.cursor = self.db.cursor()        

    def get_pin(self, num = 1016):
        sql = 'SELECT email, application_id, pin, pinhash from portal_host_pin where application_id = %d;' % num
        return self.select(sql)

    def select(self, sql):        
        res = self.cursor.execute(sql)
        # Fetch a single row using fetchone() method.
        #data = self.cursor.fetchone()
        data = self.cursor.fetchall()
        # disconnect from server
        self.db.close()
        return data

if __name__ == "__main__":
    x = db_mod()
    res = x.get_pin(3)
    import re
    list_new = []
    format_mail = "\d\d\d"
    for i in res:
        if re.search(format_mail, i[0]):
            print i
            list_new.append(i)
    print len(res)
    print len(list_new)
