echo `mkdir /data/provision_test/$1`
echo `cp ue_provision_res_$1.html /data/provision_test/$1`
echo `mv log /data/provision_test/$1`
echo `cp -rf /corefile /data/provision_test/$1`
echo `cd /corefile && rm -rf *`
echo "http://192.168.1.25/$1/ue_provision_res_$1.html"

echo "%%%%%%%%%%%%%%%%%%%%%%%%send test result mail%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

echo "测试结果 http://192.168.1.25/$1/ue_provision_res_$1.html">>testsult.txt
echo "log备份地址 :  http://192.168.1.25/$1/log/">>testsult.txt
echo "corefile备份地址 :  http://192.168.1.25/$1/corefile/">>testsult.txt
echo "(本邮件是程序自动下发的，请勿回复！)">>testsult.txt
echo "">>testsult.txt



