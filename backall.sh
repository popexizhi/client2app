echo `mkdir /data/provision_test/$1`
echo `cp ue_provision_res_$1.html /data/provision_test/$1`
echo `mv log /data/provision_test/$1`
echo `cp -rf /corefile /data/provision_test/$1`
echo `cd /corefile && rm -rf *`
