#!/bin/bash

NOC_PATH=`pwd`

export PYTHONPATH=$NOC_PATH

echo 'Starting ....'

cd $NOC_PATH && ./app_server -cfg="cfg/app_$1_alone.cfg" -db -server_provision -host="$1"
