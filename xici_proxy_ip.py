#######################################
####  爬取"西刺免费代理"的"国内高匿代理IP"
#######################################
####  爬取的太频繁，被封ip了
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
    def getDataList(self, num=2):
        print('爬取中...')
        #将浏览器的response header和request header的复制过来
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            'Host': 'www.xicidaili.com',
            'Referer': 'https://www.xicidaili.com/nn/'
        }
        totalList = []
        ableList = []
        unableList = []
        page = 50   #只爬取第一页的数据
        #至少要爬取到num=20个有效的免费ip地址
        while len(ableList) < num:
            self.url = self.baseUrl + str(page)
            req = requests.get(self.url, headers=headers)
            html_doc = BeautifulSoup(req.text, 'html.parser')
            # 除去第一行，因为第一行为标题栏(国家，IP地址，端口，服务器地址，是否匿名......)，不是我们想要的数据
            lists = html_doc.select('#ip_list tr')[1:]
            print('数据分析中,请稍等...')
            for li in lists[1:]:
                self.li = li
                ip = self.getText(1) + ':' + self.getText(2)
                obj = {
                    'ip': ip,
                    'address': self.getText(3),
                    'anonymous': self.getText(4),
                    'type': self.getText(5),
                    'alive':self.getText(8),
                    'date': self.getText(9),
                }
                totalList.append(obj)
                print('ableList:',ableList,len(ableList))
                try:
                    Telnet(self.getText(1), self.getText(2),timeout=0.1)
                    print(len(ableList),num,Telnet(self.getText(1), self.getText(2),timeout=1))
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
        # self.saveInCsv(ableList)
    #删除开头或是结尾的字符，如对" Runoob "去除首尾空格
    def getText(self, index):
        return self.li.select('td')[index].text.strip()

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
        pd.DataFrame(ableList).to_csv(csvUrl,encoding="utf-8-sig")  #避免保存的中文乱码
        # csvFile = open('D:\python\meituan\output_file\proxyIp.csv', 'w')
        # csvFile.truncate() #清空内容
        # scvHeader = ['ip','anonymous','type','address','responseTime','finalVerifyTime']
        # w = csv.DictWriter(csvFile, scvHeader)
        # w.writeheader()
        # w.writerows(ableList)
        # csvFile.close()

#调用方法,获取有效IP列表
XiciProxy().getDataList()