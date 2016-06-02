#pragma once
#include <string>
#include <arpa/inet.h> /*struct sockaddr_in*/
#include <stdlib.h>  /*system*/

class TestSlimTcp {
  public:
    TestSlimTcp(int ue_id, char * appserveraddr, bool is_server=false,int sin_port=8000);
    ~TestSlimTcp();

    bool RandomPackets(); //测试包长随机波动

    bool InitSocket();

    void Log(std::string log_con); 
    std::string GetTestFileCon(); //获得测试文件的内容
  protected:

  private:
    int ue_id_ ;
    int sin_port_ ;
    int socket_ ;
    bool is_server_ ;
    struct sockaddr_in sin_;
    struct sockaddr_in server_sin_;    
};
