#-*-coding:utf8-*-
#http://python-jenkins.readthedocs.io/en/latest/examples.html#example-6-working-with-jenkins-nodes
import jenkins
import time

server = jenkins.Jenkins('http://192.168.1.23:8080')
print server.jobs_count()

job_name = '22test'
#server.create_job(job_name, jenkins.EMPTY_CONFIG_XML)
jobs = server.get_jobs()
print server.build_job(job_name, {"testcase_id": int(time.time())})
#server.disable_job(job_name)
#server.copy_job(job_name, 'empty_copy')
#server.enable_job('empty_copy')
#server.reconfig_job('empty_copy', jenkins.RECONFIG_XML)
#server.delete_job(job_name)
#server.delete_job('empty_copy')
# build a parameterized job
# requires creating and configuring the api-test job to accept 'param1' & 'param2'
#server.build_job('api-test', {'param1': 'test value 1', 'param2': 'test value 2'})
#1. 执行build 前记录last_build_number,
#2. build_job
#3. 监控last_build_numer的执行结果
last_build_number = server.get_job_info(job_name)['lastCompletedBuild']['number']
build_info = server.get_job_info(job_name, last_build_number)
print "* " * 20

for i in  build_info:
    #print "%s : %s" % (i, build_info[i])
    print i
print "* " * 20 + "lastBuild"
print build_info["lastBuild"]
print "** " * 20 + "lastStableBuild"
print build_info["lastStableBuild"]
# get all jobs from the specific view
#jobs = server.get_jobs(view_name='View Name')
#print jobs
