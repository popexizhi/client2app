#-*-coding:utf8-*-
import re

class filewriter():
    def __init__(self, filename = "alone_app.cfg"):
        self.cfgfile = filename
        self.cfg_data = []
        self.chang_cfg_list_app = ["app_prov_customer_name", "app_prov_license_key", "app_prov_license_serial", "app_prov_application_id"]
        self.chang_cfg_list_app_x = ["app_prov_application_id"]
        self.chang_cfg_list_dev = ["dev_prov_email_addr", "dev_prov_application_id", "dev_prov_pincode", "dev_prov_pinhash"]
        self.__readfile()

    def log(self, message):
        print "*"*20
        print message

    def change_thrift_port(self, new_port):
        self.thrift_port = ["npls_thrift_port"]
        self._change_cfg(self.thrift_port[0], str(new_port))
        res = self.__save_newfile("app_%s" % str(new_port))
        
        return res
    def change_dev_pincode(self, user_email , new_pincode):
        self.pincode_list = ["dev_prov_email_addr", "dev_prov_pincode"]
        self._change_cfg(self.pincode_list[0], user_email)
        self._change_cfg(self.pincode_list[1], new_pincode)
        res = self.__save_newfile("dev_%s_%s" % (str(user_email), str(new_pincode)))

        return res


    def __readfile(self):
        f = open(self.cfgfile)
        cfg_data = f.readlines()
        f.close()
        for i in cfg_data:
            self.cfg_data.append(i)
             

    def savenewfile(self, newcfgs = ["app3", "1", "2", "3"], app = 1 , names = [0, 0]):
        chang_cfg_list = self.chang_cfg_list_app if 1 == app else self.chang_cfg_list_dev
        
        t = 0
        for i in chang_cfg_list:
            self._change_cfg(str(i), str(newcfgs[t]))
            t = t + 1
        file_name_pre = (("app_%s" % newcfgs[0]) if 1 == app else ("dev_%d%d" % (names[0], names[1]) ))
        self.__save_newfile(file_name_pre)
        
    def savenewfilex(self, newcfgs = ["app3"], app = 1 ):
        chang_cfg_list = self.chang_cfg_list_app_x if 1 == app else self.chang_cfg_list_dev
        t = 0
        for i in chang_cfg_list:
            self._change_cfg(str(i), str(newcfgs[t]))
            t = t + 1
        file_name_pre = (("app_%s" % newcfgs[0]) if 1 == app else ("dev_%s" % newcfgs[1]))
        return self.__save_newfile(file_name_pre)


    def _change_cfg(self, cfg_lab, newcfg):
        u_re = "#?%s ? =.*\n" % str(cfg_lab) #注释和空格处理
        link = re.compile(u_re)
        new_link = cfg_lab + " = " + newcfg + "\n"
        j = 0
        for i in self.cfg_data:
            if re.match("#?%s" % str(cfg_lab), i): #注释的处理
                x = re.sub(link, new_link, i)
                self.log(x)
                self.cfg_data[j] = x
            j = j + 1        

    def __save_newfile(self, pre):
        cfg_data = ""
        for i in self.cfg_data:
            cfg_data = cfg_data + i
        f_name = "cfg//"+ pre + "_alone.cfg"
        f = open(f_name, "w")
        f.write(cfg_data)
        f.close()
        self.cfg_data = []
        return f_name

if __name__ == "__main__":
    a = filewriter("alone_app.cfg")
    #a.savenewfile()
    
    #a.savenewfile((u'testdev@senlime.com', '2254',u'e3435805-dcb1-3343-b875-ab9e067d5be9', u'50dbb8b3207e9de966f824f4aeb7ed265045a9a72713977b3472b708f6c99498'), app = 0)
    a.savenewfilex()
    
    
