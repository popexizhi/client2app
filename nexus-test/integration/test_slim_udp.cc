#include "test_slim_udp.h"
#include "base/logging.h"
#include "slim_socket_interface.h"
#include "noc_quic_appserver.h"

TestSlimUdp::TestSlimUdp(int ue_id, char * appserveraddr, int sin_port){
  ue_id_ = ue_id ; 
  sin_port_ = sin_port;
  if(!inet_pton(AF_INET, appserveraddr, &server_sin_.sin_addr)){
    ; 
  }
  else{
      server_sin_.sin_family = AF_INET;
      server_sin_.sin_port = ntohs(4000); //[popexizhi] ?why
  }
  InitSocket();
}

TestSlimUdp::~TestSlimUdp() {}

bool TestSlimUdp::InitSocket(){
  bool res = true;
  client_socket_ = SlimSocket(PF_INET, SOCK_DGRAM, 0);

  memset(&sin_, 0, sizeof(sin_));
  sin_.sin_family = AF_INET;
  sin_.sin_addr.s_addr = htonl(ue_id_);
  sin_.sin_port = ntohs(sin_port_) ;

  
  DVLOG(0)<<"[popexizhi] start udp socket, \t ue_id is "<< ue_id_ <<"\t sin_port is "<< sin_port_ ;
  if (SlimBind(client_socket_, (struct sockaddr *)&sin_, sizeof(sin_)) != 0){
    res = false ;
    DVLOG(0)<<"[popexizhi] SlimBind udp socket is not 0 , \t ue_id is "<< ue_id_ <<"\t sin_port is "<< sin_port_ ;
  }
  return res;
}

bool TestSlimUdp::SendData(){
    //=========================
    //sendto
    bool res = true;
    DVLOG(0) << "[popexizhi]----------test client sendto server begin-------" ;
//    if(!inet_pton(AF_INET, (const char*)&L2_app_host_ip_str[0], &server_sin_.sin_addr)){
//        res = false ;
//        return res;
//    }
    //send use ========================

    int test_packet = 1;
    int total_send_size = 0;
    int err = 0;
    char snd_buf[1500];
    int snd_len = 1000;
    //res use ==========================
    char rcv_buf[1600];
    int read_count = 0;
    
    int exit_flg = 0;

    while(!err && (test_packet < 50000) && (0 == exit_flg)){
        DVLOG(0) << "[popexizhi] -------test client send begin ---,test_packet=" << test_packet<<", exit_flg="<<exit_flg;
        //UDP socket 
        DVLOG(0)<<"[popexizhi] Start to call UDP ClientSendTo() for socket " << client_socket_;
        //send
        sprintf(snd_buf, "Hello UDP %d %d \n", client_socket_, test_packet);
        int count = Send(snd_buf, snd_len);
        total_send_size += count;
        DVLOG(0) << "[popexizhi]socket client(" << ue_id_ << " )send count ---"  << count << " ** " << test_packet << " total_send_size=" << total_send_size;      
        //recv
        read_count = Recv(rcv_buf);


        test_packet++;
    }
    DVLOG(0) << "[popexizhi] test client UDP is finished" ;
    return res;
}
int TestSlimUdp::Recv(char * rcv_buf){
        socklen_t form_len = sizeof(struct sockaddr_in);
        struct sockaddr_in from_addr;
        char from_ip[20];

        int read_count = SlimRecvFrom(client_socket_,rcv_buf,1500,0, (struct sockaddr *)(&from_addr), &form_len);
        if (!inet_ntop(AF_INET, &from_addr.sin_addr, &from_ip[0], 16)) {
            DCHECK(0 && "IP address convert fail");
        }
        DVLOG(0) << "UDPclient(" << client_socket_ << " )rcv data: count="  << read_count <<", from="<<from_ip<<"."<< ntohs(from_addr.sin_port)<<", value= "<<rcv_buf;

        return read_count;

}
int TestSlimUdp::Send(char * snd_buf, int snd_len){
    int count = 0 ;
    do{
        count = SlimSendTo(client_socket_,snd_buf, snd_len, 0, (struct sockaddr *)&server_sin_, sizeof(server_sin_) );
        if (count <= 0){
            usleep(50);
        }
    }while(count <= 0);
    return count;
}

void TestSlimUdp::ShowLog() {
   DVLOG(0)<<"[popexizhi] TestSlimUdp::ShowLog......";
}
