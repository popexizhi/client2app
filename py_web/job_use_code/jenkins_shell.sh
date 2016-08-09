#!/bin/bash
echo "git push list is"${file_lists}
echo "commit list is "
echo ${commit_lists}
echo "branch is "${gitbranch}
echo "hi , git push "


echo "*******************************************************" 
echo ${file_lists}>files.log
vim -S get_file.vim files.log
cat files.log
echo "*******************************************************"
###################################################mail内容准备
#echo "测试邮件，请勿回复" >lizard_ana.log
echo "git@192.168.1.33:nexus/Nexus.git                  push branch is "${gitbranch}>>lizard_ana.log
echo "***************************************************************************************************">>lizard_ana.log
echo "**************************push commit id ：**************************">>lizard_ana.log
echo ${commit_lists} >>lizard_ana.log
echo "">>lizard_ana.log
echo "file modified list is">>lizard_ana.log
echo "**********************************************************************">>lizard_ana.log
cat files.log >>lizard_ana.log
echo "**********************************************************************">>lizard_ana.log
echo "lizard ana result ">>lizard_ana.log

cat files.log |xargs lizard -C10 -L50 >lizard_res.log
cat lizard_res.log
#lizard_res.log结果过滤（根据https://jira.senlime.com/browse/NGS-370 comment 记录要求）
vim -S lizard_res.vim lizard_res.log

cat lizard_res.log>>lizard_ana.log
echo "MAIL 准备内容如下:"
cat lizard_ana.log
#com3=`cat lizard_ana.log |grep -A4 " Warnings (cyclomatic_complexity > 10 or length > 50 or parameter_count > 100)" | grep -A3 'NLOC' | grep '===='`

#测试lizard分析结果中是非包含非法内容
cat lizard_ana.log |grep -A4 " Warnings (cyclomatic_complexity > 10 or length > 50 or parameter_count > 100)" | grep -A3 'NLOC' | grep '===='

if [ "$?" = "0" ]
then
    echo "lizard Warnings is null"
        echo "不需要邮件通知"
        else
            echo "发送测试结果mail ..." 
                echo `python sendMail.py "git push lizard Warnings mail"  all lizard_ana.log` #all@senlime.com
                    #echo `python sendMail.py 测试邮件请忽略 lijie@senlime.com lizard_ana.log` #all@senlime.com
                    fi
