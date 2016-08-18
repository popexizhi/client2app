#-*- coding:utf8 -*-
import urllib, urllib2
import cookielib
import json, time

class httper():
    def __init__(self, http_ip = "192.168.1.55", space_s = 0):
        self.http_ip = http_ip
        self.space_http_s = space_s #每个请求的间隔时间，防止服务器请求太过频繁
        self.token = None

    def log(self, message):
        print "*" * 20
        print "[httper] %s" % message

    def login(self, username="lijie@senlime.com", passwd="password"):
        """post username+passwd api/eap/auth ,return token"""
        self.add_licenses = "http://"+ self.http_ip +"/api/eap/auth"
        data = json.dumps({"email":username, "password":passwd})
        res = self._send_data(self.add_licenses, data)
        assert 0 == res["result"]
        self.token = res["data"]["token"]
        return res
    def add_user(self, user_mail):
        """post api/eap/users """
        if None == self.token:
            self.login() 
        assert self.token #无token无法add
        res = {}
        self.add_user = "http://"+ self.http_ip +"/api/eap/users"
        value = {"name":user_mail,"email":user_mail,"mobile":"","policy_set":1,"app_group":[1]}
        data = json.dumps(value)
        res = self._send_data(self.add_user, data, self.token)
        return res

    def register_app_server(self, url_id, name, key, serial):
        """post id+key+serial /api/eap/appservers/<server_id>/activation"""
        if None == self.token:
            self.login() 
        assert self.token #无token无法add
        url_register = "/api/eap/appservers/%d/activation" % url_id
        self.add_licenses = "http://"+ self.http_ip + url_register
        value = {"app_server_id":url_id,"license":{"customer_name":name, "license_key":key, "serial":serial},"activation_type":"single","cluster_info":{"cluster_type":"join","custer_id":"","cluster_name":"","cluster_desc":""},"single_info":{"name":url_id,"description":url_id},"dbconfig":{"type":"mysql","hostname":"","port":"3306","username":"","password":""}}

        data = json.dumps(value)
        return self._send_data(self.add_licenses, data, self.token)

    def add_appserver_lic(self, name):
        self.add_licenses = "http://"+ self.http_ip +"/api/biz/licenses"
        data = json.dumps({"customer_name": name,"product_name":"app_server"})
        return self._send_data(self.add_licenses, data)
    
    def add_dev_lic(self, user_id, applications_name = "com.senlime.nexus.app.browser"):
        """/api/eap/users/2/accesskey?application_id=com.senlime.nexus.app.browser """
        if None == self.token:
            self.login() 
        assert self.token #无token无法add
        add_dev_api = "/api/eap/users/%s/accesskey?application_id=%s" % (str(user_id), str(applications_name))
        self.add_dev_licenses = "http://"+ self.http_ip + add_dev_api 
        data = json.dumps({"user_id":user_id,"application_id":applications_name})
        
        return self._send_data(self.add_dev_licenses, data, self.token)

    def _send_data(self, url, data, token=None):
        self.log("url is %s" % url)
        self.log("post data is %s" % str(data))
        if None == token:
            header = {'Content-Type': 'application/json'}
        else:
            header = {'Content-Type': 'application/json', 'Authorization': token}
        self.log("header is %s" % str(header))
        req = urllib2.Request(url, data, header) #添加发送头
        
        f = urllib2.urlopen(req)
        get_data = f.read()
        f.close()
        self.log(get_data)
        return json.loads(get_data)

    def add_devs(self, application_ids =[3], dev_num = 100, dev_start = 0):
        """
        1.add dev_lic 申请 mail根据dev($dev_start_j)@test.com
        2.增加dev_num个申请，每个申请间隔为self.space_http_s
        return 全部的申请结果list
        """
        res_lists = []
        for j in xrange(dev_num):
            print "*** " * 5 + str(j) + "*** " * 10
            dev_lic_add_res = self.add_dev_lic(application_ids, email = "dev%d_%d@test.com" % (dev_start, j))
            print dev_lic_add_res
            res_lists.append([j, dev_lic_add_res["result"]])
            
            time.sleep(self.space_http_s)

        return res_lists

if __name__ == "__main__":
    a = httper()
    a.add_devs()
