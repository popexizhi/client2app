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
   ~TestSlimUdp();
   void ShowLog();

   //=============
   //
   bool InitSocket();
   bool SendData();
 protected:
    
 private:
    int ue_id_;
    int sin_port_ ;
    int client_socket_ ;
    struct sockaddr_in sin_;
    struct sockaddr_in server_sin_;
};

//extern void set_log();

