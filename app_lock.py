# -*- coding:utf8 -*-
class app_provision_res():
    def __init__(self, id_name="test"):
        self.name = id_name
        self.provision_res_l = 0
    def set_provision_pass(self):
        #
        self.provision_res_l = 1

    def get_provision_status(self):
        return self.provision_res_l
