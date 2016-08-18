#-*-coding:utf8-*-
import MySQLdb
class db_mod():
    def __init__(self, db_name = "nexus_eap" , ip = "192.168.1.44", user = "slim", pd = "password"):
        self.db = MySQLdb.connect(ip ,user, pd, db_name, port=3306, charset="utf8")
        self.cursor = self.db.cursor()       

    def __del__(self):
        self.db.close()

    def log(self, message):
        print "*" * 20
        print message

    def get_pin(self, num = 1016):
        sql = 'SELECT email, application_id, pin, pinhash from portal_host_pin where application_id = %d;' % num
        return self.select(sql)

    def select(self, sql):
        self.log(sql)
        res = self.cursor.execute(sql)
        # Fetch a single row using fetchone() method.
        data = self.cursor.fetchone()
        # disconnect from server
        return data
    def update_app_ip(self):
        """change eap db 中激活状态app 的ip 防止注册端口冲突临时使用 """
        host_ip = "192.168.1.25"
        update_sql = 'UPDATE  eap_app_server  set host_ip = "0.0.0.1" where app_server_status != "LOADING" and host_ip ="%s" ;' % host_ip
        #self.log(update_sql)
        self.update(update_sql)
    def change_user_appserver(self, user_mail, appserver_id):
        """change the devs of user_mail to  appserver_id 
           app_user_app_servers 修改
           user_id 与 app_server_id的对应关系后重新生成license即可。
           其中
            1.user_id为 eap_user的id "select id from eap_user where email=user_mail;"
            2.app_server_id 在appserver的sqlite库中的table_provision_status中server_id可以查询到
           return select app_server_id from app_user_app_servers where user_id = 步骤1;
        """
        updata_sql = 'update eap_user_app_servers set app_server_id = %d where user_id = (select id from eap_user where email="%s");' % (appserver_id, user_mail)
        res_sql = 'select app_server_id from eap_user_app_servers where user_id = (select id from eap_user where email="%s");' % user_mail
        self.update(updata_sql)
        res = self.select(res_sql)
        assert 1 == len(res) #业务逻辑要求dev只有一个appserver
        return res[0]

        
        return res
    def update(self, u_sql):
        self.log(u_sql)
        res = self.cursor.execute(u_sql)
        self.db.commit()
        return res

if __name__ == "__main__":
    x = db_mod()
    #print x.get_pin()
    print x.update_app_ip()
