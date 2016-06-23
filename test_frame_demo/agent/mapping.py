# -*- coding:utf8 -*-
# map_list

environment_map = {
    # 依赖服务环境配置         
    "httper" :{
        "url": "http://192.168.1.25/testcase_use/",
        "file_list": "file_list/",
    },                
                
                
    "agent" :{
        "tc_path" : "testsuit/", #agent 端testcase下载存放位置
        "tc_bk" : "slim_uesfile/", #agent 端testcase中前置条件需要file的下载存储位置
        "log_path" : "/home/lijie/test/lib_nexus/app_lib/sf/", #agent端tc_check的log内容存储位置
    },
                
    }
