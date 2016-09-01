# -*-coding:utf8 -*-
class ProvisionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    try:
        raise ProvisionError("test path")
    except ProvisionError as e:
        print ("err is %s" % e.value)
