# -*- coding:utf8 -*-
class app_provision_res():
    def __init__(self, id_name="test"):
        self.name = id_name
        self.provision_res_l = 0
        self.dev_provision_pass_l = 0
    def set_provision_pass(self):
        #
        self.provision_res_l = 1

    def get_provision_status(self):
        return self.provision_res_l

    def set_dev_provision_pass(self):
        self.dev_provision_pass_l = 1

    def dev_provision_pass(self):
        return self.dev_provision_pass_l
