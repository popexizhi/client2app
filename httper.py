#-*- coding:utf8 -*-
import urllib, urllib2
import cookielib
import json

class httper():
    def __init__(self, http_ip = "192.168.1.43"):
        self.add_licenses = "http://"+ http_ip +":18080/api/biz/licenses"
        
    def add_appserver_lic(self, name):
        data = json.dumps({"customer_name": name,"product_name":"app_server"})
        req = urllib2.Request(self.add_licenses, data, {'Content-Type': 'application/json'}) #添加发送头

        f = urllib2.urlopen(req)
        get_data = f.read()
        f.close()
        return json.loads(get_data)

if __name__ == "__main__":
    a = httper()
    print a.add_appserver_lic("xd")
