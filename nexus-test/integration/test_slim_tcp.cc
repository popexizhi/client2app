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
      server_sin_.sin_port = ntohs(3000); //server port 3000
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
  socket_ = SlimSocket(PF_INET, SOCK_DGRAM, 0);

  std::string log="-------test client bind begin---,socket_=" + std::to_string(socket_);
  Log(log);
  if(SlimBind(socket_, (struct sockaddr *)&sin_, sizeof(sin_)) != 0) {
    res = false;
    return res;
  }

  Log("-------test client connect server begin---");
  if(SlimConnect(socket_, (struct sockaddr *)&server_sin_, sizeof(server_sin_)) != 0) {
    res = false;
    return res;
  }

  return res;
}

bool TestSlimTcp::RandomPackets(){
  //1.生成随机文件:包含包体大小和发送方
  //2.将步骤1的测试文件发送到server端
  //3.等待2的server确认信息后按步骤1开始执行测试
  bool res = true;
   
  //1.生成随机文件:包含包体大小和发送方
  std::string test_file_con = GetTestFileCon();


  return res;
}

void TestSlimTcp::Log(std::string log_con){
  DVLOG(0) <<"[popexizhi] [TestSlimTcp]"<<log_con;
}

std::string TestSlimTcp::GetTestFileCon(){ 
  //获得测试文件的内容
  //1.生成测试文件
  //2.读取测试文件内容
  std::string res_con;
  //1.生成测试文件
  std::string cmd = "python random_packets_testdata.py";
  int i = system(cmd.c_str());
  Log(cmd + " res is " + std::to_string(i));

  //2.读取测试数据文件内容
  res_con = GetTestDataFile();
  return res_con;
}

bool TestSlimTcp::GetTestDataFile(){
    //读取测试数据文件内容
    //当前目录下test_random_packets.td.csv
    char *file_name="test_random_packets.td.csv";
}























