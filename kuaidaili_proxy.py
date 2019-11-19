#######################################
####  爬取"快代理"的"国内高匿代理IP"
#######################################
import requests
import csv  #不使用这个
from bs4 import BeautifulSoup
from telnetlib import Telnet  # 这是用来验证IP是否可用
import pandas as pd           # 将数据保存到csv中

class XiciProxy():
    def __init__(self):
        self.baseUrl = 'https://www.kuaidaili.com/free/inha/'

    #获取西刺代理的有效ip,数目为num条
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
        page = 50   #为保证能爬取到足够多的有效代理，这里设置最大爬取页数

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
                print('ableList:',ableList,len(ableList))
                try:
                    Telnet(self.getText(0), self.getText(1),timeout=10)#timeout的只是在初始化socket连接时起作用，而一旦连接成功后如果出现等待那就不会起作用了
                    ableList.append(obj)
                except:
                    unableList.append(obj)
            page = page + 1
        self.totalList = totalList
        self.ableList = ableList
        self.unableList = unableList

        #结果保存到txt中
        self.saveInTxt(ableList)
        #将结果保存到csv中
        self.saveInCsv(ableList)

    #删除开头或是结尾的字符，如对" Runoob "去除首尾空格
    def getText(self, index):
        return self.tr.select('td')[index].text.strip()

    #将结果ip保存到D:\python\meituan\output_file\proxyIp.txt中
    def saveInTxt(self,data):
        txt = open('D:\python\meituan\output_file\proxyIp.txt', 'w')
        txt.truncate()  #保存内容前先清空内容
        for item in data:
            itemStr = str(item)
            txt.write(itemStr)
            txt.write('\n')
        txt.close()

    #将结果保存到D:\python\meituan\output_file\proxyIp.csv中
    def saveInCsv(self,ableList):
        csvUrl = 'D:\python\meituan\output_file\proxyIp.csv'
        pd.DataFrame(ableList).to_csv(csvUrl,encoding="utf_8_sig")  #避免保存的中文乱码
        # csvFile = open('D:\python\meituan\output_file\proxyIp.csv', 'w')
        # csvFile.truncate() #清空内容
        # scvHeader = ['ip','anonymous','type','address','responseTime','finalVerifyTime']
        # w = csv.DictWriter(csvFile, scvHeader)
        # w.writeheader()
        # w.writerows(ableList)
        # csvFile.close()

#调用方法,获取有效IP列表
XiciProxy().getDataList()