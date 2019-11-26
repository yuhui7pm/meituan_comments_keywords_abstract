#######################################
####  爬取"快代理"的"国内高匿代理IP"
#######################################
import requests
from bs4 import BeautifulSoup
from telnetlib import Telnet  # 这是用来验证IP是否可用
import pandas as pd           # 将数据保存到csv中
import pymongo

class MongoDB():
    def __init__(self, result=''):
        self.host = 'localhost'
        self.port = 27017
        self.databaseName = 'meituan'
        self.formName = 'proxy_ip'
        self.result = result

    # 连接数据库
    def collect_database(self):
        client = pymongo.MongoClient(host=self.host, port=self.port)  # 连接MongoDB
        db = client[self.databaseName]  # 选择数据库
        collection = db[self.formName]  # 指定要操作的集合,表
        return collection

    # 保存数据
    def save_to_Mongo(self):
        collection = self.collect_database()
        try:
            if collection.insert_many(self.result):
                print('存储到MongoDB成功', self.result)
        except Exception:
            print('存储到MongoDb失败', self.result)

    # 查询数据
    def selectMongoDB(self):
        collection = self.collect_database()
        # print('评论数据的总长度为：',collection.count_documents({}))
        for x in collection.find():
            print(x)

    # 删除数据
    def delete_database(self):
        collection = self.collect_database()
        collection.delete_many({'proxy_web_name': 'kuai_proxy'})  # 删除数据库内容

class KuaiProxy():
    def __init__(self):
        self.baseUrl = 'https://www.kuaidaili.com/free/inha/'

    #获取快代理的有效ip,数目为num条
    def getDataList(self, num=5):
        print('爬取中...')
        #将浏览器的request header和response header的字段复制过来
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            'Host': 'www.kuaidaili.com',
            'Referer': 'https://www.kuaidaili.com/free/inha'
        }
        totalList = []  #爬取到的所有的ip
        ableList = []   #爬取到的有效的ip
        unableList = [] #爬取到的无效的ip
        page = 1   #为保证能爬取到足够多的有效代理，这里设置最大爬取页数

        #至少要爬取到num个有效的免费ip地址
        while len(ableList) < num:
            self.url = self.baseUrl + str(page)
            req = requests.get(self.url, headers=headers)
            html_doc = BeautifulSoup(req.text, 'html.parser')
            lists = html_doc.select('.table.table-bordered.table-striped tbody tr')
            print('数据分析中,请稍等...')
            for tr in lists:
                self.tr = tr
                ip = self.getText(0) + ':' + self.getText(1)
                obj = {
                    'ip': ip,
                    'anonymous': self.getText(2),
                    'type': self.getText(3),
                    'address': self.getText(4),
                    'responseTime':self.getText(5),
                    'finalVerifyTime': self.getText(6),
                }
                totalList.append(obj)
                try:
                    Telnet(self.getText(0), self.getText(1),timeout=10)#timeout的只是在初始化socket连接时起作用，而一旦连接成功后如果出现等待那就不会起作用了
                    ableList.append(obj)
                    print('ableList:', ableList, len(ableList))
                except:
                    unableList.append(obj)
            page = page + 1
        self.totalList = totalList
        self.ableList = ableList
        self.unableList = unableList
        return ableList

    #删除开头或是结尾的字符，如对" Runoob "去除首尾空格
    def getText(self, index):
        return self.tr.select('td')[index].text.strip()

class SaveDataInFiles():
    def __init__(self, results=''):
        # 需要保存的数据
        self.results = results

    # 出口文件
    def saveResults(self):
        self.saveInCsv()
        self.saveInTxt()

    # 将结果ip保存到D:\python\meituan\output_file\proxyIp_kuai.txt中
    def saveInTxt(self):
        txt = open('D:\python\meituan\output_file\proxyIp_kuai.txt', 'w')
        txt.truncate()  # 保存内容前先清空内容
        for item in self.results:
            itemStr = str(item)
            txt.write(itemStr)
            txt.write('\n')
        txt.close()

    # 将结果保存到D:\python\meituan\output_file\proxyIp_kuai.csv中
    def saveInCsv(self):
        csvUrl = 'D:\python\meituan\output_file\proxyIp_kuai.csv'
        pd.DataFrame(self.results).to_csv(csvUrl, encoding="utf-8-sig")  # 避免保存的中文乱码

#调用方法,获取有效IP列表
KuaiProxy = KuaiProxy().getDataList()
# 保存数据到files中
SaveDataInFiles(KuaiProxy).saveResults()
# 保存数据到数据库
MongoDB(KuaiProxy).save_to_Mongo()
# 查看保存的数据
MongoDB().selectMongoDB()
