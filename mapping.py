#-*- coding:utf8 -*-

#----------------------EAP_Provision-----------------
EAP_Pro_mapping = {
    "url" : "192.168.1.43:18080", #eap,provision,appstore的地址
    "eap_api": {
        "appserver_activation" : "/api/eap/appservers/%d/activation", #app server provision的post请求接口
    },
    "DB":{
        "EAP":{
            "db_name":"nexus_eap",
            "ip" : "192.168.1.44",
            "user" : "slim",
            "passwd": "password",
        },
    },
} 

# ---------------------appserver---------------------
APPSERVERDB = {"Actived":"Actived", "Waiting_active": "Waiting_active" }# app db中provision状态定义
app_mapping = {
    "db_name": "nplServer1.db", #appserver使用的db name
    "cfg" : "alone_app.cfg",    #app使用的cfg 路径和名称
    "app_path" : "provision_code/app_server",  #app的路径和名称
    "thrift_port_list" : [11000, 12000], # 此位置每次使用根据eap_db.eap_app_server的host_ip + host_port 使用情况
    "ip" : "192.168.1.84", #当前运行appserver的ip
}
# ---------------------dev ------------------------
dev_mapping = {
    "db_name": "npl1.db",       #dev使用的db name
    "cfg" : "alone_dev.cfg",    #dev使用cfg 路径和名称
    "dev_path" : "provision_code/slim_engine_test",  #app的路径和名称
    "space_http_s": 0,          #dev provision时http请求的间隔时间
    "space_provision_s": 5,          #dev provision的间隔时间
    "space_provision_wait_time": 60, #dev provision过程中pex UI的最长等待时间，单位为s
}
