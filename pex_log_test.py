#-*-coding:utf8 -*-
from pex_log import pexLog
import unittest
import os, time
import threading


class TestpexLog(unittest.TestCase):
    def test_expect(self):
        x = pexLog("testcase/pextest.log")
        res = x.expect("ok")
        self.assertEqual(res, 1)
        self.assertEqual(x.after, ["ok"])


    def test_expect_wait(self):
        pa = "testcase/pextesti.log"
        os.system("echo ''>%s" % pa)
        t = 20
        x = pexLog(pa)
        t1 = threading.Thread(target=self._os_write, args=(pa,"ok",1))
        t1.start()
        res = x.expect("ok", t)
        self.assertEqual(res, 1)
        self.assertEqual(x.after, ["ok"])

    def _os_write(self, pa, message, wa_t):
        time.sleep(wa_t)
        cmd = "echo '%s'>>%s" % (message, pa)
        print cmd
        os.system(cmd)

if __name__=="__main__":
    unittest.main()
