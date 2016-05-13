# -*- encoding:utf8 -*-
# pexpect use for stdout
import pexpect,time
import re
class sh_pex():
    def __init__(self):
        pass
    def get_url(self):
        app_sta_shell = """./app_server -cfg="alone_with_provision.cfg" -db -server_provision"""
        get_char_1 = "App Server Provision Params Read"
        get_char_2 = "App Server Added on EAP, please register on EAP"
        send_c = "a"
        check_url = "Requesting URL https://192.168.1.43:443/api/admin/sync-appserver/\d+"
        x = pexpect.spawn(app_sta_shell)
        x.expect(get_char_1) #getchar before
        x.sendline(send_c) #send_char
        x.expect(get_char_2) #getchar before
        x.sendline(send_c) #send_char
        #url check
        x.expect(check_url) #getchar before
#        print "*** " * 20
#        print x.after
#        print "*** " * 20
        app_id = re.findall(r"\d+$",x.after)
        print app_id[0]
        x.interact() # 把sh的连接交给用户控制
        return app_id[0]

if __name__=="__main__":
    a = sh_pex()
    print a.get_url()
