#-*-coding:utf8-*-
import re

class filewriter():
    def __init__(self, filename = "alone_app.cfg"):
        self.cfgfile = filename
        self.cfg_data = []
        self.__readfile()

    def __readfile(self):
        f = open(self.cfgfile)
        cfg_data = f.readlines()
        f.close()
        for i in cfg_data:
            self.cfg_data.append(i)
             

    def savenewfile(self, newcfgs = ["app3", "1", "2", "3"] ):
        chang_cfg_list = ["app_prov_customer_name", "app_prov_license_key", "app_prov_license_serial", "app_prov_application_id"]
        
        t = 0
        for i in chang_cfg_list:
            self._change_cfg(i, newcfgs[t])
            t = t + 1
        

        self.__save_newfile(newcfgs[0])
        
    def _change_cfg(self, cfg_lab, newcfg):
        u_re = cfg_lab + " =.*\n"
        link = re.compile(u_re)
        new_link = cfg_lab + " = " + newcfg + "\n"
        j = 0
        for i in self.cfg_data:
            if re.match(cfg_lab, i):
                x = re.sub(link, new_link, i)
                print x
                self.cfg_data[j] = x
            j = j + 1        

    def __save_newfile(self, pre):
        cfg_data = ""
        for i in self.cfg_data:
            cfg_data = cfg_data + i

        f = open("cfg\\"+ pre + "_alone.cfg", "w")
        f.write(cfg_data)
        f.close()

if __name__ == "__main__":
    a = filewriter()
    a.savenewfile()
