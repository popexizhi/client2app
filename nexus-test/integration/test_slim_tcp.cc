#include "test_slim_tcp.h"
#include "base/logging.h"
#include "slim_socket_interface.h"

using namespace std;

TestSlimTcp::TestSlimTcp(int ue_id, char * appserveraddr ,int sin_port=8003){
    ue_id_ = ue_id ;
    sin_port_ = sin_port ;
    InitSocket();
}

~TestSlimTcp::TestSlimTcp(){}

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





























