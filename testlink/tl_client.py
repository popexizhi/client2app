#-*-encoding:utf8 -*-
from testlink import TestlinkAPIClient, TestLinkHelper, testlinkerrors
import sys,time
import err

LOGLEVEL="DEBUG"
class tl_client():
    def __init__(self, tl_url="192.168.1.84", key = "641a49a91c63fe1a803ec1c5dc62a4e6"):
        self.server_url = "http://%s/testlink/lib/api/xmlrpc.php" % tl_url
        self.key = key
        self.tl_helper = TestLinkHelper(self.server_url, self.key)
        self.tl = self.tl_helper.connect(TestlinkAPIClient)

    def log(self, message, level=LOGLEVEL):
        if "DEBUG" == level or "info" == level:
            print "*" * 20
            print "[tl_client] %s" % str(message)

    def getTestCasesForTestSuite(self, testsuitid):
        self.log(testsuitid)
        try:
            tc_list = self.tl.getTestCasesForTestSuite(testsuitid,'true','full')
        except testlinkerrors.TLConnectionError as e:
            self.log(str(e), "info")
            raise err.TFError(str(e))
        
        except testlinkerrors.TLResponseError as e:
            self.log(str(e), "info")
            raise err.TFError(str(e))

        self.log(tc_list)
        return self.gettclist(tc_list)

    def gettclist(self, tc_list):
        tc_id_list = None
        for i in tc_list:
            self.log(i)
            self.log("id is %s" % i["id"])
            if tc_id_list:
                tc_id_list = "%s %s"% (str(tc_id_list),str(i["id"]))
            else:
                tc_id_list = str(i["id"])
        
        self.log(tc_id_list)
        return tc_id_list

if __name__ == "__main__":
    x = tl_client()
    x.getTestCasesForTestSuite("3")
