# -*-coding:utf8 -*-
import re, time
class pexLog():
    def __init__(self, pa):
        self.pa = pa
        self.con = ""
        self.readfilenum = 0


    def expect(self, message, timeout = 30):
        """return n在timeout时间内查询到对应内容个数，self.after为查找到的内容
           return 0在timeout时间内容没有查询到对应内容 self.after 为空
        """
        res = 0
        self.after = ""
        wait_time = 0
        while wait_time < timeout:
            search_res = self.get_unread_line(self.pa, message)
            if 0 == len(search_res):
                time.sleep(1)
                wait_time = wait_time + 1
            else:
                self.after = search_res
                res = len(search_res)
                break
        return res
    

    def get_unread_line(self, inputfile, searmessage):
        filepath = open(inputfile)
        con = filepath.readlines()
        filepath.close()
        lines = len(con)
        res = []
        if lines > self.readfilenum:
            self.con = con[self.readfilenum: lines]
            for i in self.con:
                if re.search(searmessage, i):
                    res = re.findall(searmessage, i)
                    break
        return res


if __name__ == "__main__":
    x = pexLog("testcase/pextest.log")
    x.expect("ok")
    x.expect("err", timeout=2)
