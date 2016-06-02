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
#include "slim_socket_interface.h"
#include "test_noc_ue_interface.h"
#include "intergration/test_c.h" //popexizhi add
#include "intergration/test_slim_udp.h" //popexizhi add
#include "intergration/test_slim_tcp.h" //popexizhi add

extern char L2_app_host_ip_str[64] ;

extern IntParam log_level;
extern IntParam init_database;
extern volatile int exit_flg;
extern int g_run_alone_mode;
extern bool udp_socket_test;

extern void set_coredump();
extern void client_socket_test(int ue_id);
extern void server_receive_data_test(int newfd);
extern void server_socket_test(int ue_id);
extern void mem_log_init();
extern void init_test_run_thread();
extern void L2ConnectionEvtNotify(unsigned int  ue_id, CONNECTION_NOTIFY_TYPE evt, bool success, int errCode, void * cb_param);
extern void L1ConnectionEvtNotify(unsigned int  ue_id, CONNECTION_NOTIFY_TYPE evt, bool success, int errCode, void * cb_param);
extern void AppServerL1ConnectionEvtNotify(unsigned int  ue_id, CONNECTION_NOTIFY_TYPE evt, bool success, int errCode, void * cb_param);
extern void ReadDeviceProvParams(const std::string& cfg_file, DeviceProvisionParam& param);
extern void ReadAppProvParams(const std::string& cfg_file, AppServerProvisionParam& param);
extern void ReadL2AuthParams(const std::string& cfg_file, AUTH_L2_CLIENT_PARAMS& param);
extern void RunAppServer(base::CommandLine* line, std::string app_server_ip, std::string bgw_ip, int port_offset,std::string pin_code_url);
//udp test functions
extern void server_udp_socket_test(int ue_id);
extern void client_udp_socket_test(int ue_id);
extern void socket_test_udp(unsigned int  ue_id);
extern void app_server_socket_test(unsigned int  ue_id );
extern void ShutdownApplication(int signum);
