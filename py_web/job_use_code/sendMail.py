#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib,sys 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_mail(sub, content, build_num, send_list):
    mailto_list = []
    #############   
    #要发给谁
    if ( "all" == send_list):
        mailto_list=["npl@senlime.com"] #"slim_test@126.com",
    else :
        mailto_list.append(send_list)#["lijie@senlime.com"] #"server@senlime.com",
    #####################
    #设置服务器，用户名、口令以及邮箱的后缀
    #mail_host="smtp.126.com"
    #mail_user="slim_test@126.com"
    #mail_pass="tkzhvxiwddkjzurk"#smtp.126 password
    #mail_postfix="126.com"
    mail_host="smtp.office365.com"
    mail_user="dev@senlime.com"
    mail_pass="S2m123,./"
    mail_postfix="office365.com"
    mail_port=587
    ######################
    '''''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user#+"<"+mail_user+"@"+mail_postfix+">"
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #msg = MIMEText(content,_charset='utf8')

    htm = MIMEText(content,_charset='utf-8')
    msg.attach(htm)

    #构造附件
    #att1 = MIMEText(open('/usr/share/nginx/html/testreport/testReport_'+build_num+'.html', 'r').read() ,'base64','utf-8')
    #att1["Content-Type"] = 'application/octet-stream'
    #att1["Content-Disposition"] = 'attachment; filename="testReport_'+build_num+'.html"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
    #msg.attach(att1)

    msg['Subject'] = sub 
    msg['From'] = me 
    msg['To'] = ";".join(mailto_list) 
    try: 
        s = smtplib.SMTP(mail_host,port=mail_port,timeout=20) 
        #s.connect(mail_host) 
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        
        s.login(mail_user,mail_pass) 
        s.sendmail(me, mailto_list, msg.as_string()) 
        s.close() 
        return True
    except Exception, e: 
        print str(e) 
        return  False
if __name__ == '__main__':
    filepath = sys.argv[3] #"testsult.txt"
    build_num = sys.argv[1]
    send_list = sys.argv[2]
    f=open(filepath)
    con = f.readlines()
    conx= ""
    f.close()
    for i in con:
        conx = conx + str(i)
    if send_mail(build_num, conx, build_num, send_list): 
        print '发送成功'
    else: 
        print '发送失败'
