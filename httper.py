#-*- coding:utf8 -*-
import urllib, urllib2
import cookielib
import json

class httper():
    def __init__(self, http_ip = "192.168.1.43"):
        self.http_ip = http_ip
    
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
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'}) #添加发送头

        f = urllib2.urlopen(req)
        get_data = f.read()
        f.close()
        return json.loads(get_data)

if __name__ == "__main__":
    a = httper()
    name = "xd"
    res = a.add_appserver_lic(name)
    print res
    assert res["result"] == 0 # 判断返回为成功
    print a.register_app_server(32, name, res["key"], res["serial"])
    #print a.add_dev_lic([2])

