# -*- coding:utf8 -*-
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print content
    return jsonify({"uuid":uuid})

class json_git():
    def __init__(self, str_json):
        self.str_json = str_json

    def get_files(self):
        assert self.str_json
        json_s = self.str_json
        print str(json_s)
        file_list = []
        commit_id_list = []
        num = json_s['total_commits_count']
        print "num is %s" % str(num)
        for x in json_s['commits']:#json['commits'] = [] num 个
            # 处理'added','modified'
            print "*" * 50
            print x['added']
            print x['id']
            file_list = file_list + x['added']
            file_list = file_list + x['modified']
            commit_id_list.append(x['id'])
            print x['modified']
            
        return file_list, commit_id_list
    
    def get_branch(self):
        assert self.str_json
        return self.str_json["ref"]
if __name__ == '__main__':
    app.run(host= '192.168.1.99', port=8888,debug=True)
