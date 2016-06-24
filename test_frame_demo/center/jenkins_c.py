#-*-coding:utf8-*-
import jenkins
import time

JE_IP = 'http://192.168.1.23:8080'
job_list = ['22test']
res_job_list = ['99test']
class jenkins_c():
    def __init__(self):
        self.jc = jenkins.Jenkins(JE_IP)
        

    def build_job(self, tc_id, job_name = job_list[0]):
        """
        #1. 执行build 前记录last_build_number,
        #2. build_job
        """
        job_id = None
        job_id = self.jc.get_job_info(job_name)['lastBuild']['number']

        self.jc.build_job(job_name, {"testcase_id": tc_id})

        return str(job_id + 1)

    def wait_job_pass(self, job_id, job_name = job_list[0], timeout = 60 * 2):
        """
        #监控job_id timeout 内是否成功
        其中 get_job_info 返回如下:
{u'building': False, u'queueId': 23, u'displayName': u'#11', u'description': None, u'changeSet': {u'items': [], u'kind': None}, u'artifacts': [], u'timestamp': 1466069379662, u'fingerprint': [], u'number': 11, u'actions': [{u'parameters': [{u'name': u'testcase_id', u'value': u'1466069371'}]}, {u'causes': [{u'userName': u'anonymous', u'userId': None, u'shortDescription': u'Started by user anonymous'}]}], u'id': u'11', u'keepLog': False, u'url': u'http://192.168.1.23:8080/job/22test/11/', u'culprits': [], u'result': u'SUCCESS', u'executor': None, u'duration': 83, u'builtOn': u'192.168.1.22', u'fullDisplayName': u'22test #11', u'estimatedDuration': 71}
        """
        res = "TIMEOUT"
        sta = int(time.time())
        for i in xrange(timeout):
            build_info = self.jc.get_job_info(job_name, job_id) #['lastCompletedBuild']['number'] #lastCompletedBuild

            build_info_last_id = build_info['lastCompletedBuild']['number']
            print "\t now build_info_last_id is %d " % build_info['lastCompletedBuild']['number']
            if (str(build_info_last_id) == str(job_id) and (str("False") == str(build_info['lastCompletedBuild']["building"]))):
                res = build_info['lastCompletedBuild']["result"]
                return res
            time.sleep(1)
        return res
        
if __name__ == "__main__":
    a = jenkins_c()
    job_id = a.build_job(int(time.time()))
    print "job_id is %s" % job_id
    print "result is %s" % a.wait_job_pass(job_id)
