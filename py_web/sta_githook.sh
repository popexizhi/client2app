#!/bin/bash

cmd_flask="python flask_t.py"
#kill old 
echo 'kill server....'
ps axu|grep "python flask_t.py"|grep -v grep |cut -c 9-16|xargs kill -9


#start flask_t.py
echo 'Starting server....'
nohup python flask_t.py>gitlab_hook.log &

sleep 1
#
ps axu|grep "python flask_t.py"
