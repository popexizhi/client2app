#include "test_slim_tcp.h"
#include "base/logging.h"
#include "slim_socket_interface.h"

using namespace std;

TestSlimTcp::TestSlimTcp(int ue_id, char * appserveraddr, bool is_server, int sin_port){
  ue_id_ = ue_id ;
  sin_port_ = sin_port ;
  is_server_ = is_server;
  
  if(!inet_pton(AF_INET, appserveraddr, &server_sin_.sin_addr)){
    ; 
  }
  else{
      server_sin_.sin_family = AF_INET;
      server_sin_.sin_port = ntohs(4000); //
  }


  memset(&sin_, 0, sizeof(sin_));
  sin_.sin_family = AF_INET;
  sin_.sin_addr.s_addr = htonl(ue_id_);
  sin_.sin_port = ntohs(sin_port_) ;


  InitSocket();
}

TestSlimTcp::~TestSlimTcp(){}

bool TestSlimTcp::InitSocket(){
  bool res = true;
  return res;
}

bool TestSlimTcp::RandomPackets(){
  bool res = true;
  //1.生成随机文件:包含包体大小和发送方
  //2.将步骤1的测试文件发送到server端
  //3.等待2的server确认信息后按步骤1开始执行测试
  return res;
}





























