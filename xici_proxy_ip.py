#######################################
####  爬取"西刺免费代理"的"国内高匿代理IP"
#######################################
import requests
import csv
from bs4 import BeautifulSoup
from telnetlib import Telnet  # 这是用来验证IP是否可用

class XiciProxy():
    def __init__(self):
        self.baseUrl = 'https://www.xicidaili.com/nn/'

    #获取西刺代理的有效ip,数目为4条
    def getDataList(self, num=2):
        print('爬取中...')
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
    def saveInTxt(self,d):
        s = str(d)
        txt = open('D:\python\meituan\output_file\proxyIp.txt', 'w')
        txt.writelines(s)
        txt.close()

    #将结果保存到D:\python\meituan\output_file\proxyIp.csv中
    # def saveInCsv(self,ableList):
    #     csvFile = open('D:\python\meituan\output_file\proxyIp.csv', 'wb')
    #     for value in ableList:
    #         w = csv.DictWriter(csvFile, value.keys())
    #         w.writerow(value)
    #     csvFile.close()

#调用方法,获取有效IP列表
XiciProxy().getDataList()

#     # def writeXls(self):
#     #     wb = xlwt.Workbook(encoding='ascii')
#     #     ws = wb.add_sheet('ip列表')
#     #     ws.write(0, 0, 'IP地址')
#     #     ws.write(0, 1, '服务器地址')
#     #     ws.write(0, 2, '是否匿名')
#     #     ws.write(0, 3, '类型')
#     #     ws.write(0, 4, '验证时间')
#     #     self.getDataList(60)  # 60为可用数据的长度
#     #     print('爬取总数据{}条'.format(len(self.totalList)))
#     #     print('{}条可用'.format(len(self.ableList)))
#     #     print('{}条不可用'.format(len(self.unableList)))
#     #     for i, data in enumerate(self.ableList):
#     #         ws.write(i+1, 0, data['ip'])
#     #         ws.write(i+1, 1, data['address'])
#     #         ws.write(i+1, 2, data['anonymous'])
#     #         ws.write(i+1, 3, data['type'])
#     #         ws.write(i+1, 4, data['date'])
#     #     wb.save('西刺代理ip.xls')
#     #     print('录入西刺代理ip.xls-成功')
#     #
#     # def readXls(self, index):
#     #     book = open_workbook('西刺代理ip.xls')
#     #     sheet = book.sheet_by_index(0)
#     #     row_con = sheet.row_values(index)  # 行的操作
#     #     return row_con
#
# XiciProxy().getDataList();
# # if __name__ == '__main__':
# #     xiciProxy = XiciProxy()
# #     xiciProxy.writeXls()