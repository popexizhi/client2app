#-*- coding:utf8 -*-
import urllib, urllib2
import cookielib
import json, time

class httper():
    def __init__(self, http_ip = "192.168.1.55", space_s = 0):
        self.http_ip = http_ip
        self.space_http_s = space_s #每个请求的间隔时间，防止服务器请求太过频繁
    def login(self, username="lijie@senlime.com", passwd="password"):
        res=None
        return res

    def register_app_server(self, url_id, name, key, serial):
        "post id+key+serial /api/admin/register_app_server"
        self.add_licenses = "http://"+ self.http_ip +":18080/api/admin/register_app_server"
        data = json.dumps({"app_server_id":url_id, "customer_name":name, "license_key":key, "serial":serial})
        return self._send_data(self.add_licenses, data)

    def add_appserver_lic(self, name):
        self.add_licenses = "http://"+ self.http_ip +":18080/api/biz/licenses"
        data = json.dumps({"customer_name": name,"product_name":"app_server"})
        return self._send_data(self.add_licenses, data)
    
    def add_dev_lic(self, applications_name, email = "testdev@senlime.com"):
        self.add_dev_licenses = "http://"+ self.http_ip +":18080/api/admin/pin"
        data = json.dumps({"email": email,"applications":applications_name})
        
        return self._send_data(self.add_dev_licenses, data)

    def _send_data(self, url, data):
        print url
        print data
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'}) #添加发送头
        print "[httper] "+"*** " * 20
        print "url is %s; data is %s" % (url, data) 
        print "[httper] "+"*** " * 20
        f = urllib2.urlopen(req)
        get_data = f.read()
        f.close()
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
