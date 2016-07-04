#include "test_slim_udp.h"
#include "base/logging.h"
#include "slim_socket_interface.h"
#include "noc_quic_appserver.h"
#include <sys/types.h>
#include <dirent.h>
#include <sys/stat.h>

using namespace std;

TestSlimUdp::TestSlimUdp(int ue_id, char * appserveraddr, int sin_port){
  //类变量初始化
  f_length_USE_ = "filelength:";
  f_name_USE_ = "filename:";
  f_spl_USE_ = ";";   
  f_PASS_USE_ = "pass";
  f_FAIL_USE_ = "fail";

  ue_id_ = ue_id ; 
  sin_port_ = sin_port;
  is_server_ = false;
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

TestSlimUdp::TestSlimUdp(int ue_id, char * appserveraddr, bool is_server, int sin_port){
  //类变量初始化
  f_length_USE_ = "filelength:";
  f_name_USE_ = "filename:";
  f_spl_USE_ = ";";   
  f_PASS_USE_ = "pass";
  f_FAIL_USE_ = "fail";


  ue_id_ = ue_id ; 
  sin_port_ = sin_port;
  is_server_ = true;
  sin_.sin_family = AF_INET;
  if(!inet_pton(AF_INET, appserveraddr, &sin_.sin_addr)){
    ; 
  }
  sin_.sin_port = ntohs(sin_port_) ;

  InitSocket();
}

TestSlimUdp::~TestSlimUdp() {}

bool TestSlimUdp::InitSocket(){
  bool res = true;
  socket_ = SlimSocket(PF_INET, SOCK_DGRAM, 0);
  DVLOG(0) << "[popexizhi]************** UDP test create socket fd ***" << socket_ << "\t is server :" << is_server_;

  DVLOG(0) << "[popexizhi] start udp socket, \t ue_id is "<< ue_id_ <<"\t sin_port is "<< sin_port_ ;
  if (SlimBind(socket_, (struct sockaddr *)&sin_, sizeof(sin_)) != 0){
    res = false ;
    DVLOG(0)<<"[popexizhi] SlimBind udp socket is not 0 , \t ue_id is "<< ue_id_ <<"\t sin_port is "<< sin_port_ ;
  }
  return res;
}
bool TestSlimUdp::RecvData(){
    bool res = true;
    DVLOG(0) << "[popexizhi]----------test server socket fd-------" ;
    //send use ========================
    int total_rcv_size = 0;   
    char rcv_buf[1600] ;
    int read_count = 0;
    int exit_flg = 0;
  
    while( 0 == exit_flg)
    {
        read_count = Recv(rcv_buf);
        total_rcv_size += read_count;  
        Send(rcv_buf, read_count);
    }
    return res;
}
bool TestSlimUdp::SendData(){
    //=========================
    //sendto
    bool res = true;
    DVLOG(0) << "[popexizhi]----------test client sendto server begin-------" ;
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
        DVLOG(0)<<"[popexizhi] Start to call UDP ClientSendTo() for socket " << socket_;
        //send
        sprintf(snd_buf, "Hello UDP %d %d \n", socket_, test_packet);
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
    char from_ip[16];

    int read_count = SlimRecvFrom(socket_, rcv_buf, 1500, 0, (struct sockaddr *)(&from_addr), &form_len);
    if (!inet_ntop(AF_INET, &from_addr.sin_addr, &from_ip[0], 16)) {
        DCHECK(0 && "IP address convert fail");
    }
    else{
       //设置接收端地址
       server_sin_.sin_family = AF_INET;
       server_sin_.sin_port = from_addr.sin_port; //
       server_sin_.sin_addr = from_addr.sin_addr;
    }
    DVLOG(0) << "[popexizhi] UDPclient(" << socket_ << " )rcv data: count="  << read_count <<", from="<< from_ip <<"."<< ntohs(from_addr.sin_port)<<", value= "<<rcv_buf;

    return read_count;

}
int TestSlimUdp::Send(char * snd_buf, int snd_len){
    int count = 0 ;
    do{
        count = SlimSendTo(socket_, snd_buf, snd_len, 0, (struct sockaddr *)&server_sin_, sizeof(server_sin_) );
        if (count <= 0){
            usleep(50);
        }
    }while(count <= 0);
    return count;
}

int TestSlimUdp::Send(std::string snd_sbuf){
    char *cstr = new char[snd_sbuf.length() + 1] ;
    strcpy(cstr, snd_sbuf.c_str());
    return Send(cstr, snd_sbuf.length()); 
}

void TestSlimUdp::ShowLog() {
   DVLOG(0)<<"[popexizhi] TestSlimUdp::ShowLog......";
}

bool TestSlimUdp::SendFile(std::string file_path){
    // 发送指定路径的文件
    bool res = true;
    DVLOG(0)<<"[popexizhi] file_path: \t"<<file_path ;
    FILE *fp = fopen(file_path.c_str(), "r");
    if (NULL == fp) {
        DVLOG(0) <<"[popexizhi err]************************** Open file is ERR";
        res = false;
        return res;
    }
    long file_length = 0;
    fseek(fp, 0, SEEK_END);
    file_length = ftell(fp);

    int SENDBUF = 1000; //发送缓冲区大小
    int count = 0;
    count = file_length/SENDBUF; //发送次数
    
    fseek(fp, 0, SEEK_SET);

    //send 文件头[filename,filelength]
    std::string fileHead = "";//"filename:" + file_path + ";filelength:" + std::to_string(file_length)+";";
    fileHead = f_name_USE_ + file_path + f_spl_USE_ + f_length_USE_ + std::to_string(file_length) + f_spl_USE_ ;

    DVLOG(0) << "[popexizhi]fileHead is "<<fileHead;
    //const char *cstr = fileHead.c_str();
    char *cstr = new char[fileHead.length() + 1] ;
    strcpy(cstr, fileHead.c_str());
    if (!Send(cstr, fileHead.length())){
        DVLOG(0) <<"[popexizhi err]************************** Send file head is ERR";
        res = false;
        return res;
    }
    //接受文件头发送结果
    char rcv_buf[1600];
    int read_count = 0;
    while(1){
        read_count = Recv(rcv_buf);
        rcv_str_ = rcv_str_ + rcv_buf;
        DVLOG(0) << "[popexizhi] -----------------rcv_str :" << rcv_str_ ;
        //Send(rcv_buf, read_count);
        std::string snd_sbuf;
        if (CheckFile(&snd_sbuf)) {
            //获取返回结果
            int rcv_f_end = rcv_str_.find(f_spl_USE_, 1);
            std::string rcv_f ;
            rcv_f = rcv_str_.substr(0, rcv_f_end);
            DVLOG(0) << "[popexizhi] -----------------rcv_str_ " << rcv_str_ ;
            DVLOG(0) << "[popexizhi] -----------------rcv_f " << rcv_f ;
            if (f_PASS_USE_ == rcv_f){
                DVLOG(0) << "[popexizhi] fileHead is pass";
                FileBodySend(fp, file_length);
            }
            else{
                DVLOG(0) << "[popexizhi] fileHead is false";    
            }
        }
    }
    fclose(fp);
    delete [] cstr;
    return res;
}
bool TestSlimUdp::FileBodySend(FILE *fp, int file_length){
    //发送文件体内容
    int SENDBUF = 1000; //发送缓冲区大小
    int count = 0;
    count = file_length/SENDBUF; //发送次数

    DVLOG(0) <<"[popexizhi] file body is start send, count is "<< count;
    for(long i = 0; i < count + 1; i++){
        char snd_buf[1500] = {0}; 
        int snd_len = SENDBUF;
        if (count == i) {
                snd_len = file_length % SENDBUF;
        }
        fread(snd_buf, snd_len, 1, fp);
        DVLOG(0) <<"[popexizhi] send count is " << i << "\t; count is "<< count;
        Send(snd_buf, snd_len);
    } 
    
    DVLOG(0) << "[popexizhi] file body is end send";
    return true;
}

bool TestSlimUdp::SendDir(std::string dir_path){
    //发送指定路径的文件夹内容
    bool res = true;

    return res;
}

void TestSlimUdp::RecvDir(std::string dir_path){
    //接受文件保存到指定的文件夹
    DVLOG(0) << "[popexizhi]----------test server socket fd RecvDir-------" << dir_path ;
    //send use ========================
    int total_rcv_size = 0;   
    char rcv_buf[1600] ;
    int read_count = 0;
    int exit_flg = 0;
    rcv_str_ = "";
    while( 0 == exit_flg)
    {
        read_count = Recv(rcv_buf);
        rcv_str_ = rcv_str_ + rcv_buf;
        total_rcv_size += read_count; 
        DVLOG(0) << "[popexizhi] -----------------rcv_str " << rcv_str_ ;
        //Send(rcv_buf, read_count);
        std::string snd_sbuf="";
        if (FileHeadPass(&snd_sbuf)) {
            Send(snd_sbuf);
            FileBodyRecv(snd_sbuf, dir_path);
        }
    }
}
bool TestSlimUdp::FileBodyRecv(std::string file_head, std::string dir_path){
    //接受数据
    std::string file_path;
    std::string file_slength;
    GetFileHead(&file_path, &file_slength, &file_head);
    DVLOG(0) << "[popexizhi] --------file_slength is "<< file_slength;
    int file_ilength = std::stoi(file_slength);
    
    file_path = dir_path + file_path;   
    DVLOG(0) << "[popexizhi] --------file_path is "<< file_path;
    //FILE *fp_new=NULL;
    //存储文件
    int total_rcv_size = 0;   
    char rcv_buf[1600] ;
    int read_count = 0;
    int exit_flg = 0;
    std::string file_body="";
    while( 0 == exit_flg)
    {   
        read_count = Recv(rcv_buf);
        file_body = file_body + rcv_buf;
        total_rcv_size += read_count;
        DVLOG(0) << "[popexizhi] --------total_rcv_size is "<< total_rcv_size <<"\t file_ilength "<< file_ilength <<"-----rcv_buf :" << rcv_buf ;
        if(total_rcv_size >= file_ilength){
            exit_flg = 1;
            DVLOG(0) << "[popexizhi]  file get is end --------total_rcv_size is "<< total_rcv_size <<" file_ilength "<< file_ilength;
        }
    }
    FILE *fp_new=NULL;
    DVLOG(0) << "[popexizhi] start save file " <<file_path;
    fp_new = fopen(file_path.c_str(), "w");
    fwrite(file_body.c_str(),file_ilength, 1, fp_new);
    fclose(fp_new);
    DVLOG(0) << "[popexizhi] end save file " <<file_path;
    return true;
}
void TestSlimUdp::GetFileHead(std::string *file_path, std::string *file_length, std::string *file_head){
    int file_path_sta = file_head->find(f_name_USE_) + f_name_USE_.length() ;
    int file_path_end = file_head->find_first_of(f_spl_USE_) + 1;
    *file_path = file_head->substr(file_path_sta , file_path_end - file_path_sta - f_spl_USE_.length());
    DVLOG(0) << "[popexizhi] file_path_end - file_path_sta - f_spl_USE_.length()" << file_path_end - file_path_sta - f_spl_USE_.length() ;
    DVLOG(0) << "[popexizhi] f_spl_USE_.length()" << f_spl_USE_.length() ;
    DVLOG(0) << "[popexizhi] file_path_end " << file_path_end ;
    DVLOG(0) << "[popexizhi] file_path_sta " << file_path_sta ; 
    //截取file_head, 剔除f_spl_USE_ 从file_path_end + f_spl_USE_.length() 开始
    *file_head = file_head->substr(file_path_end + f_spl_USE_.length(), file_head->length() - file_path_end - f_spl_USE_.length());
    DVLOG(0) << "[popexizhi] file_head is "<< *file_head << "\t file_path "<< *file_path <<"\t\t file_head->length() "<< file_head->length();

    int file_length_sta = file_head->find(f_length_USE_) + f_length_USE_.length() ;
    int file_length_end = file_head->find_first_of(f_spl_USE_) + 1;
    DVLOG(0) <<"[popexizhi] file_head->find(f_length_USE_) "<<file_head->find(f_length_USE_) << "\tf_length_USE_.length() "<<f_length_USE_.length();
    DVLOG(0) <<"[popexizhi] f_length_USE_ "<<f_length_USE_;
    DVLOG(0) <<"[popexizhi] file_length_sta "<<file_length_sta << "file_length_end "<< file_length_end;
    *file_length = file_head->substr(file_length_sta , file_length_end - file_length_sta - 1);
    //截取file_head, 保留f_spl_USE_ 从file_length_end开始
    *file_head = file_head->substr(file_length_end , file_head->length() - file_length_end);

    DVLOG(0) << "[popexizhi] file_head is "<< *file_head << "\t file_length "<< *file_length;
}

bool TestSlimUdp::CheckFile(std::string *snd_sbuf){
    //检查rcv_str_中文件名称，
    //return true，则
    //1. snd_sbuf 中内容为f_name_USE_ + file_path + f_spl_USE_ + f_length_USE_ + std::to_string(file_length) + f_spl_USE_ ;
    //2. rcv_str_ 为不包含检查内容的部分
    
    bool res = false;
    if ( rcv_str_.find(f_length_USE_) == std::string::npos){
        return res;
    }
    else{
        std::string file_path="";
        std::string file_slength="";
        GetFileHead(&file_path, &file_slength, &rcv_str_);

        *snd_sbuf = f_name_USE_ + file_path + f_spl_USE_ + f_length_USE_ + file_slength + f_spl_USE_;
        DVLOG(0) << "[popexizhi]TestSlimUdp::CheckFile is "<< *snd_sbuf;
        res = true;
    }
    return res;
}
bool TestSlimUdp::FileHeadPass(std::string *snd_sbuf){
    if(CheckFile(snd_sbuf)){
        *snd_sbuf = *snd_sbuf + f_PASS_USE_ + f_spl_USE_;
        DVLOG(0) << "[popexizhi]CheckFile is "<< *snd_sbuf;
        return true;
    }
    else{
        return false;
    }


}
