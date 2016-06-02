# -*- coding=utf8 -*-
import random
import itertools
class testdata():
    def __init__(self, num = 1000, kind="random"):
        self.testdata_kind = kind
        self.testdata_num = num

        self.init_test_par()
    
    def init_test_par(self):
        self.par_cs = ["c", "s"] # c为client send data, s 为server send data
        self.use_par_packet_length = [1, 16*1024]# 发送包的大小范围为[1,16k],当前由于UDP切片问题没做,这里初次设置为16k
        self.par_packets = []
        #生成随机长度列表
        for i in xrange(self.testdata_num):
            p_length = random.randint(self.use_par_packet_length[0], self.use_par_packet_length[1])
            self.par_packets.append(p_length)        

    def get_test_data(self):
        """
        1.对self.par_* 的参数做笛卡尔乘机 
        2.对步骤1的结果做random的testdata排列
        """
        #1.对self.par_* 的参数做笛卡尔乘机 
        self.testdatas=[]
        for x in itertools.product(self.par_cs, self.par_packets):
            self.testdatas.append(x)
        #2.对步骤1的结果做random的testdata取值
        f=open("testx.cvs","w")
        for i in self.testdatas:
            num = random.randint(1, len(self.testdatas))
            print self.testdatas[num-1]
            send, length = self.testdatas[num-1]
            print "%s,%d" % (send, length)
            f.write("%s,%d\n" % (send, length))
            
        f.close()

if __name__=="__main__":
    #f=open("testx.cvs","w")
    #f.write("1,2,3,4")
    #f.close()
    x=testdata()
    x.get_test_data()
