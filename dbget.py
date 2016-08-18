#-*-coding:utf8-*-
import MySQLdb
class db_mod():
    def __init__(self, db_name = "nexus_eap" , ip = "192.168.1.44", user = "slim", pd = "password"):
        self.db = MySQLdb.connect(ip ,user, pd, db_name, port=3306, charset="utf8")
        self.cursor = self.db.cursor()        
    def log(self, message):
        print "*" * 20
        print message

    def get_pin(self, num = 1016):
        sql = 'SELECT email, application_id, pin, pinhash from portal_host_pin where application_id = %d;' % num
        return self.select(sql)

    def select(self, sql):        
        res = self.cursor.execute(sql)
        # Fetch a single row using fetchone() method.
        data = self.cursor.fetchone()
        # disconnect from server
        self.db.close()
        return data
    def update_app_ip(self):
        """change eap db 中激活状态app 的ip 防止注册端口冲突临时使用 """
        host_ip = "192.168.1.25"
        update_sql = 'UPDATE  eap_app_server  set host_ip = "0.0.0.1" where app_server_status != "LOADING" and host_ip ="%s" ;' % host_ip
        #self.log(update_sql)
        self.update(update_sql)

    def update(self, u_sql):
        self.log(u_sql)
        res = self.cursor.execute(u_sql)
        self.db.commit()
        self.db.close()
        return res

if __name__ == "__main__":
    x = db_mod()
    #print x.get_pin()
    print x.update_app_ip()
