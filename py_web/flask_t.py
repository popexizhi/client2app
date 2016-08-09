from flask import Flask, request, jsonify
from job_c import jenkins_c
import threading
import time
import json
from githook_web import json_git

app = Flask(__name__)

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print content
    job_doing(content)
    return jsonify({"uuid":uuid})


def job_doing(push_json):
    assert push_json
    th1 = threading.Thread(target=checkout, args=(push_json,))      
    th1.start()

def checkout(push_json):
    #get commite_flies
    j_git = json_git(push_json)
    file_lists, commit_lists = j_git.get_files()
    branch_name = j_git.get_branch()
    print "file_lists is %s" % str(file_lists)
    print "commit_lists is %s" % str(commit_lists)
    print "branch_name is %s" % str(branch_name)
    #for jenkins
    a = jenkins_c()
    job_id = a.build_job(str(file_lists), str(commit_lists), str(branch_name))
    print "job_id is %s" % job_id
    print "result is %s" % a.wait_job_pass(job_id)


if __name__ == '__main__':
    app.run(host= '192.168.1.99', port=8888,debug=True)
