#include "test_common.h"
#include "noc_quic_appserver.h"

using namespace std;

IntParam log_level("system","logLevel",-1);
char L2_app_host_ip_str[64] ;
volatile int exit_flg;
int g_run_alone_mode = 0;
int g_appserver_index=1;
void set_coredump()
{  
  remove("core");
  struct rlimit r_limit, local_rlimit; 
  //int *p = 0; 
  r_limit.rlim_cur = 1024*1024*1000;  
  r_limit.rlim_max = 1024*1024*1000; 
  printf("Setting coredump file size unlimit\n");  
  setrlimit(RLIMIT_CORE,&r_limit);  
  int ret = getrlimit(RLIMIT_CORE,&local_rlimit); 
  printf("Currrent CORE limit: soft = %ld, hard= %ld ,ret=%d\n",     
  local_rlimit.rlim_cur,local_rlimit.rlim_max,ret);
}

//===========================
//UDP test functions

void client_udp_socket_test( int ue_id)
{
  DVLOG(0) << "******************UDP client_socket_test begin<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n" ;
  //==================================
  //socket 1
  int client_socket = SlimSocket(PF_INET,SOCK_DGRAM,0);
  struct sockaddr_in sin;
  memset(&sin, 0, sizeof(sin));
  sin.sin_family = AF_INET;

  sin.sin_addr.s_addr = htonl(ue_id);

  DVLOG(1) << "-------test client bind begin---,client_socket=" << client_socket ;
  sin.sin_port = ntohs(8000);
  DVLOG(1)<<"Start to bind UDP socket";
  if (SlimBind(client_socket, (struct sockaddr *)&sin, sizeof(sin)) != 0) {
    
  }
  //===========================
  //socket 2
  DVLOG(1)<<"Start to create UDP socket 2222";
  int client_socket2 = SlimSocket(PF_INET,SOCK_DGRAM,0);
  sin.sin_port = ntohs(8002);
  if (SlimBind(client_socket2, (struct sockaddr *)&sin, sizeof(sin)) != 0) {
    
  }
  //==========================
  //test_slim_upd
  TestSlimUdp udp3(ue_id, L2_app_host_ip_str);
  udp3.ShowLog();
  udp3.SendData();
  //===========================
  //sendto
  DVLOG(1) << "-------test client sendto server begin---" ;
  if (!inet_pton(AF_INET, (const char*)&L2_app_host_ip_str[0], &sin.sin_addr)) {
  }

  sin.sin_port = ntohs(4000);
  int test_packet = 1;
  int total_send_size = 0;
  int err = 0;
  char snd_buf[1500];
  int snd_len = 1000;
  //====================
  socklen_t from_len = sizeof(struct sockaddr_in);
  struct sockaddr_in from_addr;
  char rcv_buf[1600] ;
  int read_count = 0;
  char from_ip[20];
  //=======================
  while(!err && (test_packet < 500000) && (exit_flg == 0))
  {
    DVLOG(1) << "-------test client send begin ---,test_packet=" << test_packet<<", exit_flg="<<exit_flg;

    int total_send = 0;
    int count = 0;
    do
    {
      //UDP socket 1
      DVLOG(1)<<"Start to call UDP ClientSendTo() for socket 1";

      sprintf(snd_buf, "Hello UDP 111111 %d \n", test_packet);
     count = SlimSendTo(client_socket,snd_buf, snd_len - total_send,0, (struct sockaddr *)&sin, sizeof(sin) );
   
      if(count <= 0)
      {
        usleep(50);
      }
      else
      {      
        total_send_size += count;
        DVLOG(0) << "socket111-test client(" << ue_id << " )send count ---"  << count << " ******* " << test_packet << " total_send_size=" << total_send_size;      
        //==================
        read_count = SlimRecvFrom(client_socket,rcv_buf,1500,0, (struct sockaddr *)(&from_addr), &from_len);
        if (!inet_ntop(AF_INET, &from_addr.sin_addr, &from_ip[0], 16)) {
            DCHECK(0 && "IP address convert fail");
        }
        DVLOG(0) << "UDPclient(" << client_socket << " )rcv data: count="  << read_count <<", from="<<from_ip<<"."<< ntohs(from_addr.sin_port)<<", value= "<<rcv_buf;
        //================== 
        
      }
    }while(count <= 0  && (exit_flg == 0) );

    int count2 = 0;
    do
    {
      DVLOG(1)<<"Start to call UDP ClientSendTo() for socket 2";
      //===================
      //UDP socket 2
      sprintf(snd_buf, "Hello UDP 222222 %d", test_packet);
      count2 = SlimSendTo(client_socket2,snd_buf  ,snd_len - total_send,0, (struct sockaddr *)&sin, sizeof(sin) ) ;
      //=================
      
      if(count2 <= 0)
      {
        usleep(50);
      }
      else
      {      
        total_send_size += count;
        DVLOG(0) << "socket222-test client(" << ue_id << " )send count ---"  << count << " ******* " << test_packet << " total_send_size=" << total_send_size;       
        //==================
        read_count = SlimRecvFrom(client_socket2,rcv_buf,1500,0, (struct sockaddr *)(&from_addr), &from_len);
        if (!inet_ntop(AF_INET, &from_addr.sin_addr, &from_ip[0], 16)) {
            DCHECK(0 && "IP address convert fail");
        }
        DVLOG(0) << "UDPclient(" << client_socket << " )rcv data: count="  << read_count <<", from="<<from_ip<<"."<< ntohs(from_addr.sin_port)<<", value= "<<rcv_buf;
        //================== 
      }
    }while(count2<= 0  && (exit_flg == 0) );

    test_packet++;

  }

  DVLOG(0) << "test client UDP send finished" ;
  sleep(5);
  DVLOG(0) << "-------UDP test End--- test_packet=" <<test_packet ;
  DCHECK(0);
  exit_flg = 1;
  
}

//udp server port: 4000
void server_udp_socket_test(int ue_id)
{
  net::IPEndPoint peer_address;
  struct sockaddr_in sin;
  memset(&sin, 0, sizeof(sin));
  sin.sin_family = AF_INET;
  if (!inet_pton(AF_INET, (const char*)&L2_app_host_ip_str[0], &sin.sin_addr)) {
  }

  int server_socket = SlimSocket(PF_INET,SOCK_DGRAM,0);
  DVLOG(0) << "************** UDP test server create socket fd  ******************\n\n\n\n" << server_socket;
  sin.sin_port = ntohs(4000);
  if (SlimBind(server_socket, (struct sockaddr *)&sin, sizeof(sin)) != 0) {
    DVLOG(1) << "-------test server UDP socket fd " << server_socket << " bind error" ;
  }

  DVLOG(1) << "-------test server UDP socket fd " << server_socket << " bind ok" ;

  int rx_cnt = 1;
  int total_rcv_size = 0;   
  socklen_t from_len = sizeof(struct sockaddr_in);
  struct sockaddr_in from_addr;
  char rcv_buf[1600] ;
  int read_count = 0;
  char from_ip[20];
  
  while(exit_flg == 0)
  {
    read_count = SlimRecvFrom(server_socket,rcv_buf,1500,0, (struct sockaddr *)(&from_addr), &from_len);
    total_rcv_size += read_count; 

    if (!inet_ntop(AF_INET, &from_addr.sin_addr, &from_ip[0], 16)) {
      DCHECK(0 && "IP address convert fail");
    }
    
    DVLOG(0) << "UDPserver(" << server_socket << " )rcv data: count="  << read_count << " rx_cnt=" << rx_cnt << " ,total_rcv_size=" << total_rcv_size<<", from="<<from_ip<<"."<< ntohs(from_addr.sin_port)<<", value= "<<rcv_buf;

    rx_cnt++;
    //=======================
    //send back the data
    int send_count;
     do
     {
         send_count = SlimSendTo(server_socket,rcv_buf, read_count,0, (struct sockaddr *)&from_addr, from_len );
         if(send_count <= 0)
         {
             usleep(50);
         }
         else
         {
             DVLOG(0) << "UDP server(" << server_socket << " )send data: count="  << send_count <<", to="<<from_ip<<"."<< ntohs(from_addr.sin_port)<<", value= "<<rcv_buf;
         }
     }while(send_count <= 0);
  }
}

static base::Thread * pServerThreadTcp = nullptr;
static base::Thread * pServerThreadUdp = nullptr;

void app_server_socket_test(unsigned int  ue_id )
{
    DVLOG(0) << "++++++++++++create TCP server socket start +++++++++++++++++++++" ;
    DCHECK(pServerThreadTcp == nullptr);
    pServerThreadTcp = new base::Thread("tcp_server_socket_thread");
    pServerThreadTcp->Start();
    pServerThreadTcp->message_loop()->PostTask(FROM_HERE, base::Bind(&server_socket_test ,ue_id));
    
    DVLOG(0) << "++++++++++++create UDP server socket start +++++++++++++++++++++" ;
    DCHECK(pServerThreadUdp == nullptr);
    pServerThreadUdp = new base::Thread("udp_server_socket_thread");
    pServerThreadUdp->Start();
    pServerThreadUdp->message_loop()->PostTask(FROM_HERE, base::Bind(&server_udp_socket_test,ue_id));
}

//above functions are UDP socket test function

//==========================
//TCP socket test functions
void client_socket_test( int ue_id)
{
  DVLOG(1) << "********************************************xubo client_socket_test begin<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n\n" ;
  DEBUG_PAUSE_APP();
  int client_socket = SlimSocket(PF_INET,SOCK_STREAM,0);
  struct sockaddr_in sin;
  memset(&sin, 0, sizeof(sin));
  sin.sin_family = AF_INET;

  sin.sin_addr.s_addr = htonl(ue_id);

  DVLOG(1) << "-------test client bind begin---,client_socket=" << client_socket ;
  sin.sin_port = ntohs(9000);
  if (SlimBind(client_socket, (struct sockaddr *)&sin, sizeof(sin)) != 0) {
    
  }

  DVLOG(1) << "-------test client connect server begin---" ;
  if (!inet_pton(AF_INET, (const char*)&L2_app_host_ip_str[0], &sin.sin_addr)) {
  }

  DVLOG(1) << "-------test client bind begin---" ;
  sin.sin_port = ntohs(3000);
  
  if (SlimConnect(client_socket, (struct sockaddr *)&sin, sizeof(sin)) != 0) {
    
  }

  DVLOG(1) << "-------test server begin---" ;
  if (!inet_pton(AF_INET, "127.0.0.1", &sin.sin_addr)) {
  }

  int test_packet = 1 ;
  int total_send_size = 0;
  int err = 0;
  while(!err && (test_packet < 1000000) && (exit_flg == 0))
  {
    DVLOG(1) << "-------test client send begin ---,test_packet=" << test_packet ;
    char snd_buf[1500];
    int snd_len = sprintf(snd_buf,"client test data seq: %d" ,test_packet) ;
    snd_len = 1000;

    int total_send = 0;
    do
    {
      int count = SlimSend(client_socket,snd_buf + total_send ,snd_len - total_send,0) ;
      total_send_size += count;
      total_send += count;
      if(count == 0)
      {
        usleep(50);
      }
      else
      {      
        DVLOG(0) << "-------test client(" << ue_id << " )send count ---"  << count << " ******* " << test_packet << " total_send_size=" << total_send_size;       
      }
    }while(snd_len != total_send   && (exit_flg==0) );
/*
    DVLOG(1)<<"Client receive test";
    char rcv_buf[1500];
    int rcv_count = SlimReceive(client_socket, rcv_buf, 1500, 0);
    DVLOG(0)<<"TCP receive test count="<<rcv_count;
*/
    test_packet++;

    DEBUG_PAUSE_APP();
  }

  DVLOG(0) << "test client send finished" ;
  sleep(2);
  DVLOG(0) << "-------test End--- test_packet=" <<test_packet ;
  exit_flg = 1;

  
}


void server_receive_data_test(int newfd)
{
  int rx_cnt = 1;
  int total_rcv_size = 0;
  
  while(exit_flg == 0)
  {
    char rcv_buf[1500] ;
    int read_count = SlimReceive(newfd,rcv_buf,1000,0);
    if(read_count <= 0)
    {
        DVLOG(0)<<"server_receive_data_test, receive data error, close the fd="<<newfd;
        SlimClose(newfd);
        break;
    }
    total_rcv_size += read_count; 
    DVLOG(0) << "-------test server(" << newfd << " )rcv data: count="  << read_count << " rx_cnt=" << rx_cnt << " ,total_rcv_size=" << total_rcv_size;
    //read_count = SlimSend(newfd,rcv_buf,read_count,0);
   //DVLOG(0) << "-------test server send data: count="  << read_count << " rx_cnt=" << rx_cnt ;    
  //  DEBUG_PAUSE_APP();
    rx_cnt++;
  }

}


void server_socket_test(int ue_id)
{
  struct sockaddr_in sin;
  memset(&sin, 0, sizeof(sin));
  sin.sin_family = AF_INET;
  if (!inet_pton(AF_INET, (const char*)&L2_app_host_ip_str[0], &sin.sin_addr)) {
  }
 
  int server_socket = SlimSocket(PF_INET,SOCK_STREAM,0);

  DVLOG(1) << "********************* xubo test server create TCP socket fd  *****************************************\n\n\n\n" << server_socket;

  sin.sin_port = ntohs(3000);
  if (SlimBind(server_socket, (struct sockaddr *)&sin, sizeof(sin)) != 0) {
    DVLOG(1) << "-------test server socket fd " << server_socket << " bind error" ;
  }

  DVLOG(1) << "-------test server socket fd " << server_socket << " bind ok" ;

  int newfd = 0;

  while(1)
  {
    DVLOG(1) << "-------test server socket fd " << server_socket << " start listen" ;
  
    if (SlimListen(server_socket, 1) != 0) {
      DVLOG(1) << "-------test server socket fd " << server_socket << " listen error" ;
    }

    DVLOG(0) << "-------test server socket fd " << server_socket << " listen return" ;

    struct sockaddr __addr;

    socklen_t __addr_len ;

    newfd = SlimAccept( server_socket, &__addr, & __addr_len);
 
    DVLOG(0) << "-------test server socket fd " << server_socket << " accept newfd:" << newfd ;

    
    if(1)
    {
      base::Thread * pNewThread = new base::Thread("socket_rx_thread");
      pNewThread->Start();
      pNewThread->message_loop()->PostTask(FROM_HERE, base::Bind(&server_receive_data_test,newfd));
    }
  }
}

void L2ConnectionEvtNotify(unsigned int  ue_id ,CONNECTION_NOTIFY_TYPE evt,bool success , int errCode , void * cb_param)
{

  if(evt == APP_SOCKET_READY)
  {
    //创建 SOCKET 程序的测试 线程
   if(g_run_alone_mode)
   {
      //start TCP server socket
       base::Thread * pServerThreadTcp = new base::Thread("server_socket_thread");
       pServerThreadTcp->Start();
       pServerThreadTcp->message_loop()->PostTask(FROM_HERE, base::Bind(&server_socket_test ,ue_id));
       
       //start UDP server socket
       base::Thread * pServerThreadUdp = new base::Thread("server_socket_thread");
       pServerThreadUdp->Start();
       pServerThreadUdp->message_loop()->PostTask(FROM_HERE, base::Bind(&server_udp_socket_test ,ue_id));
   }

    if(1)
    {
      base::Thread * pClientThread = new base::Thread("client_socket_thread");
      pClientThread->Start();
      udp_socket_test = true; //popexizhi add use for udp test
      if(udp_socket_test == true)
      {
        pClientThread->message_loop()->PostTask(FROM_HERE, base::Bind(&client_udp_socket_test,ue_id));
      }
      else
      {
        pClientThread->message_loop()->PostTask(FROM_HERE, base::Bind(&client_socket_test,ue_id));
      }
    }
  }
}

void L1ConnectionEvtNotify(unsigned int  ue_id ,CONNECTION_NOTIFY_TYPE evt,bool success , int errCode , void * cb_param)
{
  if(success)
  {
    DVLOG(0) << "L1ConnectionEvtNotify ue_id " <<  ue_id << "  connection ok ,start L2 connect ";  
    CLIENT_L1_CONNECTION_PARAM *L1_param = (CLIENT_L1_CONNECTION_PARAM*)cb_param;
    if(L1_param->active_resume_flg == true) // active
    {
      Host_Info host_info;
      host_info.host_id = L1_param->L1HostId;
      host_info.L1_connection_id = 72058139515551871;
      host_info.L2_target_host_id = L1_param->L2TargetIdList;
      host_info.L1_crypt_key = L1_param->L1key;
      int nRet = DatabaseService::Instance()->AddHostInfo(host_info);
      if(nRet != 0)
      {
           DVLOG(0) << "add database data fail !!" ;
           DCHECK(0 && "add database data fail" );
           return;
      }
    }
    
    CLIENT_L2_CONNECTION_PARAM param;
    param.hostId = L1_param->L1HostId;
    param.targetHostId = L1_param->L2TargetIdList;
    param.L2key = "0x123456" ;
    param.L2Cb = L2ConnectionEvtNotify;
    param.L2Cb_param = 0;


    AUTH_L2_CLIENT_REQ *req = nullptr;

    qc_ue_GetEncryptedEapAuthPayload(L1_param->l2_params, &req);
    DVLOG(0) << "L2 Auth pincode = " << L1_param->l2_params.pincode;
    qc_ue_SendEapAuthReq(param.targetHostId ,req, sizeof(AUTH_L2_CLIENT_REQ) + req->verify_buf_len);
    delete req;

    
    qc_ue_start_L2_connect(&param);    
  }
  else
  {
    DVLOG(0) << "L1ConnectionEvtNotify ue_id " <<  ue_id << "  connection failed ,don't start L2 connect ";  
    DCHECK(0 && "L1ConnectionEvtNotify connection failed");
  }
}

IntParam init_database("system","init_database",0);

typedef struct 
{
    CLIENT_L1_CONNECTION_PARAM param;
    int *app_connected_result;
    int server_id;
}AppServerCbParam;

void AppServerL2ConnectionEvtNotify()
{
}

void AppServerL1ConnectionEvtNotify(unsigned int  ue_id ,CONNECTION_NOTIFY_TYPE evt,bool success , int errCode , void * cb_param)
{
  AppServerCbParam* result = (AppServerCbParam*) cb_param;
  if (success)
  {
      if (result->param.active_resume_flg == true) // active
      {
          AppServerHostInfo host_info;
          host_info.host_id = result->param.L1HostId;
          host_info.L1_connection_id = 72058139515551871;
          host_info.crypt_key = result->param.L1key;
          DVLOG(0) << "Host: " << result->param.L1HostId << "\nL1Key: " << result->param.L1key;
          int ret = AppServerDataService::Instance()->AddHostInfo(result->server_id, host_info);
          DCHECK(ret != -1);
      }
      *(result->app_connected_result) = 1;
  }
  else
  {
      *(result->app_connected_result) = 0;
  }

}

static void L2_data_tpt_test_end(const char * group, const char * name, void * old_value, void * new_value)
{
    DVLOG(0) << "L2_data_tpt_test_end";
    exit_flg = 1;
}
IntParam L2DataTestEnd("test", "L2DataTestEnd", 0, L2_data_tpt_test_end);

void ReadDeviceProvParams(const std::string& cfg_file, DeviceProvisionParam& param)
{
    memset(&param, 0, sizeof(DeviceProvisionParam));
    DVLOG(0) << "Reading Device Provision Params...";

    FileConfigureLoader loader;
    loader.LoadFile(cfg_file.c_str());

    strncpy(param.provision_uri, loader.GetString("dev_prov_provision_url").c_str(), MAX_URL_LEN);
    strncpy(param.email_addr, loader.GetString("dev_prov_email_addr").c_str(), MAX_EMAIL_LEN);
    strncpy(param.pin_hash, loader.GetString("dev_prov_pinhash").c_str(), MAX_PINHASH_LEN);
    strncpy(param.dev_serial, loader.GetString("dev_prov_dev_serial").c_str(), MAX_DEV_SERIAL_LEN);
    strncpy(param.dev_os_type, loader.GetString("dev_prov_dev_os_type").c_str(), MAX_DEV_OS_TYPE_LEN);
    strncpy(param.dev_os_ver, loader.GetString("dev_prov_dev_os_ver").c_str(), MAX_DEV_OS_VER_LEN);
    strncpy(param.dev_model, loader.GetString("dev_prov_dev_model").c_str(), MAX_DEV_MODEL_LEN);
    strncpy(param.dev_software_version, loader.GetString("dev_prov_dev_soft_ver").c_str(), MAX_DEV_SOFT_VER_LEN);
    strncpy(param.application_id, loader.GetString("dev_prov_application_id").c_str(), MAX_APP_ID_LEN);

    DVLOG(0) << "Device Provision Params Read.";
    getchar();
}

void ReadL2AuthParams(const std::string& cfg_file, AUTH_L2_CLIENT_PARAMS& param)
{
  memset(&param, 0, sizeof(AUTH_L2_CLIENT_PARAMS));
  DVLOG(0) << "Reading L2 Auth params...";

  FileConfigureLoader loader;
  loader.LoadFile(cfg_file.c_str());


  strncpy(param.device_info.serial, loader.GetString("dev_prov_dev_serial").c_str(), MAX_DEV_SERIAL_LEN);
  strncpy(param.device_info.os_type, loader.GetString("dev_prov_dev_os_type").c_str(), MAX_DEV_OS_TYPE_LEN);
  strncpy(param.device_info.os_version, loader.GetString("dev_prov_dev_os_ver").c_str(), MAX_DEV_OS_VER_LEN);
  strncpy(param.device_info.model, loader.GetString("dev_prov_dev_model").c_str(), MAX_DEV_MODEL_LEN);
  strncpy(param.device_info.software_version, loader.GetString("dev_prov_dev_soft_ver").c_str(), MAX_DEV_SOFT_VER_LEN);
  strncpy(param.email, loader.GetString("dev_prov_email_addr").c_str(), MAX_EMAIL_LEN);
  strncpy(param.pinhash, loader.GetString("dev_prov_pinhash").c_str(), MAX_PINHASH_LEN);
  strncpy(param.pincode, loader.GetString("dev_prov_pincode").c_str(), MAX_PINHASH_LEN);
}

void ReadAppProvParams(const std::string& cfg_file, AppServerProvisionParam& param)
{
    memset(&param, 0, sizeof(AppServerProvisionParam));
    DVLOG(0) << "Reading App Server Provision Params...";

    FileConfigureLoader loader;
    loader.LoadFile(cfg_file.c_str());

    strncpy(param.provision_uri, loader.GetString("app_prov_provision_url").c_str(), MAX_URL_LEN);
    strncpy(param.evt_query_url, loader.GetString("app_prov_evt_query_url").c_str(), MAX_URL_LEN);
    strncpy(param.dev_serial, loader.GetString("app_prov_dev_serial").c_str(), MAX_DEV_SERIAL_LEN);
    strncpy(param.dev_os_type, loader.GetString("app_prov_dev_os_type").c_str(), MAX_DEV_OS_TYPE_LEN);
    strncpy(param.dev_os_ver, loader.GetString("app_prov_dev_os_ver").c_str(), MAX_DEV_OS_VER_LEN);
    strncpy(param.dev_model, loader.GetString("app_prov_dev_model").c_str(), MAX_DEV_MODEL_LEN);
    strncpy(param.dev_software_version, loader.GetString("app_prov_dev_soft_ver").c_str(), MAX_DEV_SOFT_VER_LEN);
    assert(loader.GetUint32("app_prov_application_id", param.application_id) == true);

    DVLOG(0) << "App Server Provision Params Read";
    getchar();
}

void ServerProvisionCallback(std::string query_uri, int server_id, AppServerProvisionResult& result)
{
    BaseAppServerEvent* evt = nullptr;
    int res = 0;
    while ((res = QueryEventNotify(query_uri, server_id, evt, 300)) != ERR_OK)
    {
        if (res == ERR_TIMEOUT)
        {
            DVLOG(0) << "Provision Evt Query Timeout";
            continue;
        }
        else
        {
            DVLOG(0) << "Provision Failed";
            exit(-1);
        }
    }
    AppServerProvisionFinishEvent* derived_ptr = static_cast<AppServerProvisionFinishEvent*>(evt);
    strncpy(result.host_id, derived_ptr->host_id, MAX_HOST_ID_LEN);
    strncpy(result.host_key, derived_ptr->host_key, MAX_HOST_KEY_LEN);
    strncpy(result.gateway_addr, derived_ptr->gateway_addr, MAX_IP_LEN);
    DVLOG(0) << "host_id = " << result.host_id << "\nhost_key = " << result.host_key << "\ngw_ip = " << result.gateway_addr;
}

void InitAppServer(const std::string& pincode_query_url, const std::string& status_report_url, int server_id)
{
    QuicAppClientSystem::GetInstance()->SetAppServerId(server_id);
    QuicAppClientSystem::GetInstance()->SetPinCodeQueryUrl(pincode_query_url);
    QuicAppClientSystem::GetInstance()->SetStatusReportUrl(status_report_url);
}

void ShutdownApplication(int signum)
{
    exit(0);
}

void RunAppServer(base::CommandLine* line, std::string app_server_ip, std::string bgw_ip, int bgw_port,std::string pin_code_url)
{
    DCHECK(line->HasSwitch("cfg") && "No configuration file specified");
    std::string cfg_file = line->GetSwitchValueASCII("cfg");
    FileConfigureLoader loader;
    loader.LoadFile(cfg_file.c_str());

    AppServerCbParam app_param;
    memset(&app_param, 0, sizeof(AppServerCbParam));

    char pincode_query_url[MAX_URL_LEN] = {0};
    char status_report_url[MAX_URL_LEN] = {0};
    strncpy(pincode_query_url, loader.GetString("pincode_query_url").c_str(), MAX_URL_LEN);
    strncpy(status_report_url, loader.GetString("status_report_url").c_str(), MAX_URL_LEN);
    
    char secret_key[128] = { 0 };
    int conn_res = -1;
    int server_id = 0;
    strcpy(secret_key, "123456");

    DVLOG(1) << "App Server DB init...";
    std::string nplDbFile;
    nplDbFile = "nplServer" + std::to_string(g_appserver_index) + ".db";
    int nRet = -1;
    nRet = AppServerDataService::Instance()->InitDatabase((char*)nplDbFile.c_str());
    if (nRet != 0)
    {
        DVLOG(0) << "database init failed ";
        exit(0);
    }

    if (line->HasSwitch("db"))
    {
        AppServerDataService::Instance()->DeleteAllHostInfo();
    }

    //get all data 
    std::shared_ptr<vector<AppServerHostInfo>> ptrHostinfos = AppServerDataService::Instance()->GetAllHostInfo();
    DVLOG(0) << "query database: get host_infors count = " << ptrHostinfos->size();
    if (ptrHostinfos->size())
    {
        for (vector<AppServerHostInfo>::iterator it = ptrHostinfos->begin(); it != ptrHostinfos->end(); it++)
        {
            struct in_addr app_host_id;
            app_host_id.s_addr = htonl(it->host_id);
            strcpy(&L2_app_host_ip_str[0], inet_ntoa(app_host_id));
            DVLOG(0) << "App Server Host Id: " << L2_app_host_ip_str;

            unsigned int app_server_id = qc_app_server_create((const char*)&L2_app_host_ip_str[0], app_server_ip.c_str(), bgw_ip.c_str(), bgw_port);
            CLIENT_L1_CONNECTION_PARAM param;
            param.L1HostId = it->host_id;
            strcpy(secret_key, it->crypt_key.c_str());
            param.L1key = (const char*)&secret_key;
            g_app_server_id = app_server_id;
            param.active_resume_flg = false;
            param.L1Cb = AppServerL1ConnectionEvtNotify;

            server_id = AppServerDataService::Instance()->GetAppServerId();
            DVLOG(0) << "param.L1Host: " << param.L1HostId << "\nparam.L1Key: " << param.L1key;
            app_param.param = param;
            app_param.app_connected_result = &conn_res;
            app_param.server_id = server_id;

            param.L1Cb_param = &app_param;

            simu_relay_secret_key_init((unsigned char*)secret_key, strlen(secret_key));
            InitAppServer(pincode_query_url, status_report_url, server_id);

            qc_app_server_connect(app_server_id, param);

            DVLOG(0) << "app server client...";
            DEBUG_PAUSE();
        }
    }
    else
    {
        if (line->HasSwitch("server_provision"))
        {
            DVLOG(0) << "Start App Server Provision";
            AppServerProvisionParam sparams;
            ReadAppProvParams(cfg_file, sparams);

            AppServerProvisionResult result;
            if (ProvisionAppServer(sparams, server_id) == ERR_OK)
            {
                AppServerDataService::Instance()->SetAppServerId(server_id);
                DVLOG(0) << "App Server Added on EAP, please register on EAP...";
                getchar();
                ServerProvisionCallback(sparams.evt_query_url, server_id, result);
            }
            else
            {
                DVLOG(0) << "App Server Provision Failed";
                exit(-1);
            }
            struct in_addr app_host_id;
            app_host_id.s_addr = htonl(atoi(result.host_id));
            strcpy((char*)&L2_app_host_ip_str[0], inet_ntoa(app_host_id));
            strcpy(secret_key, result.host_key);
            DVLOG(0) << (char*)&L2_app_host_ip_str[0];

        }
        else
        {
            DVLOG(0) << " warning: not found host information and not use provision ,so use default test param";
            server_id = 1;
            AppServerDataService::Instance()->SetAppServerId(server_id);
        }

        unsigned int app_server_id = qc_app_server_create((const char*)&L2_app_host_ip_str[0], app_server_ip.c_str(), bgw_ip.c_str(), bgw_port);
        g_app_server_id = app_server_id;
        CLIENT_L1_CONNECTION_PARAM param;
        param.L1HostId = htonl(inet_addr((const char*)&L2_app_host_ip_str[0]));
        param.L1key = (const char*)&secret_key;
        param.active_resume_flg = true;
        param.L1Cb = AppServerL1ConnectionEvtNotify;

        DVLOG(0) << "param.L1Host: " << param.L1HostId << "\nparam.L1Key: " << param.L1key;
        app_param.param = param;
        app_param.app_connected_result = &conn_res;
        app_param.server_id = server_id;

        param.L1Cb_param = &app_param;

        strcpy(secret_key, param.L1key);
        simu_relay_secret_key_init((unsigned char*)secret_key, strlen(secret_key));

        InitAppServer(pincode_query_url, status_report_url, server_id);
        qc_app_server_connect(app_server_id, param);

        DVLOG(0) << "app server client...  run_alone_mode=" << g_run_alone_mode;
        DEBUG_PAUSE();
    }
    while (*(app_param.app_connected_result) == -1)
    {
        usleep(100);
    }
    if (*(app_param.app_connected_result) == 0)
    {
        DVLOG(0) << "app_server_connected_failed ...>>>>>>>>>>>>> ";
        exit(0);
    }

    if (line->HasSwitch("server_provision"))
    {
        DVLOG(0) << "App Server Provision finished";
        printf("Please Add User Pin...\n");
        getchar();
    }

    if (g_run_alone_mode)
    {
        DVLOG(0) << "AppServer DisabledUserPinCodeQuery";
        QuicAppClientSystem::GetInstance()->DisabledUserPinCodeQuery();
    }

}
