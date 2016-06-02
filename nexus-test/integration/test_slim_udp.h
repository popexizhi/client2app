#pragma once
#include "base/at_exit.h"
#include "base/logging.h"
#include "base/files/file_path.h"
#include "base/command_line.h"
#include <queue>
#include <string>
#include "base/stl_util.h"
//#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <cstdlib>
#include <iostream>
#include <stdint.h>
#include <time.h>
#include <signal.h>
#include "quic_module_interface.h"
#include "noc_epoll_module.h"
#include "base/strings/string_number_conversions.h"
#include "base/threading/thread.h"
#include "noc_module_interface.h"
#include "base/bind.h"
#include "base/logging.h"
#include "base/memory/ref_counted.h"
#include "base/message_loop/message_loop.h"
#include "base/pending_task.h"
#include "base/run_loop.h"
#include "base/thread_task_runner_handle.h"
#include "base/threading/thread.h"
#include <stdlib.h>
#include <pwd.h>
#include <sys/resource.h>
#include <sys/types.h>
//#include "app_socket_port.h"
#include "noc_ue_port.h"
#include "param_util.h"
#include "noc_param.h"
#include "noc_test_case_timer.h"
#include <time.h>
#include <sys/time.h>
#include "noc_logging.h"
#include "noc_quic_ue_socket_system.h"
#include "DatabaseService.h"
#include "AppServerDataService.h"
#include <vector>
#include <iostream>
#include "npl_c_http_client_interface.h"
#include "npl_s_http_client_interface.h"
#include "noc_testcase_util.h"
#include "test_noc_ue_interface.h"

class TestSlimUdp {
 public:
   TestSlimUdp(int ue_id, char * appserveraddr ,int sin_port=8003);
   TestSlimUdp(int ue_id, char * appserveraddr ,bool is_server, int sin_port=4000);
   ~TestSlimUdp();
   void Sh owLog();

   //=============
   //
   bool InitSocket();
   int Send(char * snd_buf, int snd_len);
   int Send(std::string snd_sbuf);
   int Recv(char * rcv_buf);

   bool SendData(); //默认测试发送50000包
   bool RecvData(); //默认测试接受5000包
   bool SendFile(std::string file_path); //发送指定路径的文件
   bool SendDir(std::string dir_path);  //发送指定路径的文件夹内容
   void RecvDir(std::string dir_path="getfile//");  //接受文件存放到指定路径
   bool CheckFile(std::string *snd_sbuf); //检查rcv_str_中文件名称，并回复结果
 protected:
    
 private:
    int ue_id_;
    int sin_port_ ;
    int socket_ ;
    bool is_server_ ;
    struct sockaddr_in sin_;
    struct sockaddr_in server_sin_;

    std::string rcv_str_;
    //fileHead 传输使用
    //send : f_name_USE_ + file_path + f_spl_USE_ + f_length_USE_ + std::to_string(file_length) + f_spl_USE_ ;
    //rec pass : f_name_USE_ + file_path + f_spl_USE_ + f_length_USE_ + std::to_string(file_length) + f_spl_USE_ + f_PASS_USE_ + f_spl_USE_;
    std::string f_length_USE_; // = "filelength:";
    std::string f_name_USE_ ;// = "filename:";
    std::string f_spl_USE_ ;//= ";";   
    std::string f_PASS_USE_ ; //= "pass";
    std::string f_FAIL_USE_ ; //= "fail";
    
    //在rcv_str_中检查FileHead使用
    bool FileHeadPass(std::string *snd_sbuf);
    void GetFileHead(std::string *file_path, std::string *file_length, std::string *file_head);

    //发送文件内容
    bool FileBodySend(FILE *fp, int file_length);
    //接受文件内容
    bool FileBodyRecv(std::string file_head, std::string dir_path);
};

//extern void set_log();

