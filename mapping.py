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
    "app_path" : "app_server",  #app的路径和名称
    "thrift_port_list" : [11000, 12000], # 此位置每次使用根据eap_db.eap_app_server的host_ip + host_port 使用情况
}
