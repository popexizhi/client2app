#pragma once
#include <string>
#include <arpa/inet.h>

class TestSlimTcp {
  public:
    TestSlimTcp(int ue_id, char * appserveraddr, bool is_server=false,int sin_port=8003);
    ~TestSlimTcp();

    bool RandomPackets();//测试包长随机波动

    bool InitSocket();
  
  protected:

  private:
    int ue_id_ ;
    int sin_port_ ;
    bool is_server_ ;
    struct sockaddr_in sin_;
    struct sockaddr_in server_sin_;    
};
