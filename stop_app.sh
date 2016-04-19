echo `ps aux|grep "app_server"|awk '{print $2}'|xargs kill -9`
echo `ps aux|grep "slim_engine_test"|awk '{print $2}'|xargs kill -9`
