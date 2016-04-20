# client2app
client to app test use

# use
#python provision_test.py 
-生成100个applicense

#python appserver_c.py 
-启动appserver，注册dev_lic

#python dev_c.py 
-dev_c监控appserver的log完成appserver provision后，添加dev lic,生成dev的配置文件后，启动dev

#python test_report.py
-test_report根据log生成html报告


#auto 
#python tester.py xxx
-xxx为开始lic的id, 可以直接执行use中的全部步骤

-
PS:
appserver_c.py与dev_c.py可以同时启动，无启动顺序要求
