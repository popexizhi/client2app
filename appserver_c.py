#-*- coding:utf8 -*-
import sys
from shell_con import sh_control
from pexpect_shell import sh_pex 
from httper import httper
import thread
import time
def app_provision(num):
    """
    1.start appserver
    2.wait log 打印 request url id
    3.post id+key+serial /api/admin/register_app_server
    4.wait log 打印 Please Add User Pin...
    """
    a = sh_pex()
    #1.start appserver
    #2.wait log 打印 request url id
    url_id = a.get_url()
    assert url_id #检查返回的id一定存在
    print "get url_id is "
    print url_id

    #3.post id+key+serial /api/admin/register_app_server
    print "** " * 20
    print "3.post id+key+serial /api/admin/register_app_server"
    http_x = httper()
    res_add_app_key = http_x.add_appserver_lic(num)
    assert 0 == res_add_app_key["result"] #要求添加结果一定为成功，否则退出后续流程
    print http_x.register_app_server(url_id, num, res_add_app_key["key"], res_add_app_key["serial"])
    print "log is " + "$$ " * 20
    a.send_provision()
    #4.wait log 打印 request url id


def start_app(std):
    for i in xrange(10):
        thread.start_new_thread(app_provision,(i + std , ))
        print "start app....%d" % int(i +std)
        time.sleep(5)

    #    a = sh_control()
    #    a.app_provision(i+std)

if __name__ == "__main__":
    std = int(sys.argv[1])
    start_app(std)
    #app_provision(2)

