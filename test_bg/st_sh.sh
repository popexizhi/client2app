#!/usr/bin/env bash
# $1 db目录，
# $2 运行的内容
# $3 hostid


path=`pwd`
echo "path " ${path}
echo "db path  "$1
echo "run " $2
echo "cfg " $3
echo "db hostid "$4

#
echo "*******************************************"
cmd_str="${path}/$2 -cfg=${path}/$3 -host=$4"
cd $1 && nohup $cmd_str &
child_pid="$!"
echo "sub pid:" $child_pid
