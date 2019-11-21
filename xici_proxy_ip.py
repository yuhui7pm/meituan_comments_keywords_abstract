#######################################
####  爬取"西刺免费代理"的"国内高匿代理IP"
#######################################

import requests
import csv  # 不使用这个
from bs4 import BeautifulSoup
from telnetlib import Telnet  # 这是用来验证IP是否可用
import pandas as pd  # 将数据保存到csv中
# import datetime               # 获取当前时间
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
        collection.delete_many({'proxy_web_name': 'xici_proxy'})  # 删除数据库内容

class XiciProxy():
    def __init__(self):
        self.baseUrl = 'https://www.kuaidaili.com/free/inha/'
        # self.createTime = datetime.datetime.now().strftime('%Y-%m-%d')
        # self.mongoDB =mongoDB(self) #调用数据库的类

    # 获取西刺代理的有效ip,数目为num条
    def getDataList(self, num=10):
        print('爬取中...')
        # 将浏览器的response header和request header的复制过来
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            'Host': 'www.xicidaili.com',
            'Referer': 'https://www.xicidaili.com/nn/'
        }
        totalList = []
        ableList = []
        unableList = []
        page = 1  # 只爬取第一页的数据
        # 至少要爬取到num=20个有效的免费ip地址
        while len(ableList) < num:
            self.url = self.baseUrl + str(page)
            req = requests.get(self.url, headers=headers)
            html_doc = BeautifulSoup(req.text, 'html.parser')
            # 除去第一行，因为第一行为标题栏(国家，IP地址，端口，服务器地址，是否匿名......)，不是我们想要的数据
            lists = html_doc.select('#ip_list tr')[1:]
            print('数据分析中,请稍等...')
            print('lists:',lists)
            for li in lists[1:]:
                self.li = li
                ip = self.getText(1) + ':' + self.getText(2)
                obj = {
                    'proxy_web_name': 'xici_proxy',
                    'ip': ip,
                    'address': self.getText(3),
                    'anonymous': self.getText(4),
                    'type': self.getText(5),
                    'alive': self.getText(8),
                    'date': self.getText(9),
                }
                totalList.append(obj)
                print('ableList:', ableList, len(ableList))
                try:
                    Telnet(self.getText(1), self.getText(2), timeout=0.1)
                    print(len(ableList), num, Telnet(self.getText(1), self.getText(2), timeout=1))
                    ableList.append(obj)
                except:
                    unableList.append(obj)
            page = page + 1
        self.totalList = totalList
        self.ableList = ableList
        self.unableList = unableList

        return ableList

    # 删除开头或是结尾的字符，如对" Runoob "去除首尾空格
    def getText(self, index):
        return self.li.select('td')[index].text.strip()

class SaveDataInFiles():
    def __init__(self, results=''):
        # 需要保存的数据
        self.results = results

    # 出口文件
    def saveResults(self):
        self.saveInCsv()
        self.saveInTxt()

    # 将结果ip保存到D:\python\meituan\output_file\roxyIp_xici.txt中
    def saveInTxt(self):
        txt = open('D:\python\meituan\output_file\proxyIp_xici.txt', 'w')
        txt.truncate()  # 保存内容前先清空内容
        for item in self.results:
            itemStr = str(item)
            txt.write(itemStr)
            txt.write('\n')
        txt.close()

    # 将结果保存到D:\python\meituan\output_file\roxyIp_xici.csv中
    def saveInCsv(self):
        csvUrl = 'D:\python\meituan\output_file\proxyIp_xici.csv'
        pd.DataFrame(self.results).to_csv(csvUrl, encoding="utf-8-sig")  # 避免保存的中文乱码


# 调用方法,返回有效IP列表
xici_proxy = XiciProxy().getDataList()
# 保存数据到files中
SaveDataInFiles(xici_proxy).saveResults()
# 保存数据到数据库
MongoDB(xici_proxy).save_to_Mongo()
# 查看保存的数据
MongoDB().selectMongoDB()
