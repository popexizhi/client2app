#-*-coding:utf8-*-
import MySQLdb
import numpy
class db_mod():
    def __init__(self, db_name = "history_testdate" , ip = "192.168.1.44", user = "test_root", pd = "password"):
        self.db = MySQLdb.connect(ip ,user, pd, db_name, port=3306, charset="utf8")
        self.cursor = self.db.cursor()        

    def get_pin(self, num = 1016):
        sql = 'SELECT * from filesL2;'
        return self.select(sql)

    def insert(self, data):
        #insert into filesL2 (`filename`, `filelength`, `sta_time`, `end_time`, `use_time`, `average_speed`) values(
        sql = "insert into filesL2 (`filename`, `filelength`, `sta_time`, `end_time`, `use_time`, `average_speed`) values(%s)" % data
        res = self.cursor.execute(sql)
        self.db.commit()
        return res
        #return data

    def _exsql(self, sql):
        res = self.cursor.execute(sql)
        self.db.commit()
        return res

    def select(self, sql):        
        res = self.cursor.execute(sql)
        # Fetch a single row using fetchone()/fetchall() method.
        data = self.cursor.fetchall()

        return data

    def _statistics(self, filename_length):
        """ 将filename_length内容更新到statistics表中，此操作为filename_length文件的历史数据统计内容使用
        """
        sql = "select count(*) from statistics where id = (select id from file_list where filename = %s and filelength = %s)" % (filename_length.split(",")[0], filename_length.split(",")[1])
        res = self.select(sql)
        #print res
        if (res[0][0] == 0):
            #insert filename_length to statistics
            fileid_sql = "select id from file_list where filename = %s and filelength = %s" % (filename_length.split(",")[0], filename_length.split(",")[1])
            fileid = self.select(fileid_sql)[0]
            assert len(fileid) == 1 #此表有且只有一个此id
            print "fileid is %d" % fileid[0]
            insert_sql = "insert into statistics(id) value(%d)" % fileid
            self._exsql(insert_sql)
        else:
            fileid_sql = "select id from file_list where filename = %s and filelength = %s" % (filename_length.split(",")[0], filename_length.split(",")[1])
            fileid = self.select(fileid_sql)[0]
            assert len(fileid) == 1
        #数据统计和更新
        self._count_sta(filename_length.split(",")[0], filename_length.split(",")[1], fileid[0])

    def _count_sta(self, filename, filelength, fileid):    
        """ 数据统计和更新 """
        #count
        datas_sql =  "select use_time,average_speed from filesL2 where filename=%s and filelength=%s" % (filename, filelength)
        datas = self.select(datas_sql)
        count = len(datas)
        print datas
        
        use_time_list = []
        average_list=[]
        for i, j in datas:
            use_time_list.append(float(i))
            average_list.append(float(j))
        print numpy.mean(use_time_list), numpy.std(use_time_list)
        print numpy.mean(average_list), numpy.std(average_list)
      
        #use_time avg std
        use_time_avg = numpy.mean(use_time_list)
        use_time_std = numpy.std(use_time_list)
        #average avg std
        average_time_avg = numpy.mean(average_list)
        average_time_std = numpy.std(average_list)

        updata_sql = "update statistics set count=%d, use_time_arv = '%f', use_time_std = '%f', average_speed_arv = '%f', average_speed_std = '%f' where id = %d" \
                        % (count, use_time_avg, use_time_std, average_time_avg, average_time_std, fileid)
        print updata_sql
        print self._exsql(updata_sql)
        
    def _close(self):
        # disconnect from server
        self.db.close()       

    def _std_use_time(self, filename, filelength, use_time):
        sql = "select use_time_arv, use_time_std from statistics where id = (select id from file_list where filename = %s and filelength = %s)" % (filename, filelength)
        print sql
        res = self.select(sql)
        if (0 == len(res)):
            return -1 #无历史数据
        assert len(res) == 1
        if ( float(res[0][1]) - 0.000000 == 0 ):
            return -2 #无方差
        res_std = (float(use_time) - float(res[0][1]) ) / float(res[0][1])
        return res_std
            


if __name__ == "__main__":
    x = db_mod()
#    data = """'getfile//test_send_message_44.jpg', 477190, '2016-05-03 18:02:14.798572', '2016-05-03 18:02:16.259235', '1.460663', 326694.11082501576"""
#    print x.insert(data)
#    filename_length = """'getfile//1_10_send_message_44.jpg', 477190"""
#    x._statistics(filename_length)
    print x._std_use_time("'getfile//1_10_send_message_44.jpg'","477190", 25)
