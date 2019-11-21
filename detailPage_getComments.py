# 爬取美团外卖评论 https://www.meituan.com/meishi/41007600/
import requests;  # 模拟浏览器向服务器发出请求
import urllib.parse;  # 定义了url的标准接口，实现url的各种抽取
# from bs4 import BeautifulSoup;  # html和xml的解析库，用于从网页中提取数据
# import pymongo  # 从mongoDB中读取数据
# import pandas as pd
# 解决动态渲染的问题
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
import pymongo
import pandas as pd

#######################################################################################################################
#共用的数据

#######################################################################################################################
#操作mongoDB
class mongoDB():
    def __init__(self,databaseName,formName,result=''):
        self.host = 'localhost'
        self.port = 27017
        self.databaseName = databaseName
        self.formName = formName
        self.result = result

    #连接mongoDB
    def mongoDB_connect(self):
        client = pymongo.MongoClient(host=self.host, port=self.port)  # 连接MongoDB
        db = client[self.databaseName]  # 选择数据库
        collection = db[self.formName]  # 指定要操作的集合,表
        return collection

    #保存数据
    def save_to_Mongo(self):
        collection = self.mongoDB_connect()
        # collection.delete_many({})  # 删除数据库内容
        try:
            if collection.insert_many(self.result):
                print('存储到MongoDB成功', self.result)
        except Exception:
            print('存储到MongoDb失败', self.result)

    #查询数据
    def selectMongoDB(self):
        collection = self.mongoDB_connect()
        print('评论数据的总长度为：',collection.count_documents({}))
        for x in collection.find():
            print(x)

    # 删除数据
    def delete_database(self):
        collection = self.mongoDB_connect()
        collection.delete_many({})  # 删除数据库内容
#######################################################################################################################
# 获取店铺的基本信息：名字，评论标签，页码
class GetShopInformation():
    # 定义一些初始化的数据
    def __init__(self):
        self.shopUrl = 'https://www.meituan.com/meishi/41007600/'

    # 获取名字，评论标签，页码
    def get_basic_information(self):
        # 访问美团
        chrome_options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(self.shopUrl)
        browser.implicitly_wait(10)  # 隐式等待

        # 获取商铺名字
        shopName = browser.find_element_by_class_name('details').find_element_by_class_name('name')
        shopName = shopName.text.replace('食品安全档案', '')
        shopName = shopName.replace('\n', '', 3)
        # 获取已经分类好的点评标签
        commentTags = browser.find_element_by_css_selector('.com-cont .tags.clear').text
        commentTags = commentTags.replace('\n', ' ', 30)
        # 获取最多的评论页码
        commentMaxPage = browser.find_element_by_css_selector('.pagination.clear li:nth-last-child(2)').text

        # 关闭浏览器
        browser.quit()

        # 赋值，并返回结果
        return {
            'shopName': shopName,
            'commentTags': commentTags,
            'commentMaxPage': commentMaxPage,
        }
#######################################################################################################################
# 定义类获取评论数据
class GetShopComments():
    def __init__(self, shopBasicInfo):
        self.comments_ajax_url = "https://www.meituan.com/meishi/api/poi/getMerchantComment?"
        self.ajax_headers = {
            'Host': 'www.meituan.com',
            'Referer': 'https://www.meituan.com/meishi/41007600/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        # 前面GetShopInformation的类中传递过来的最大页数
        self.maxPage = int(shopBasicInfo['commentMaxPage'])
        self.shopName = shopBasicInfo['shopName']

    def get_page(self, items):
        parms = {
            'uuid': '4344eb25-c171-4c19-9d82-278ba5f01224',
            'platform': '1',
            'partner': '126',
            'originUrl': 'https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F41007600%2F',
            'riskLevel': '1',
            'optimusCode': '10',
            'id': '41007600',
            'userId': '',
            'offset': items,
            'pageSize': '10',
            'sortType': '1',
        }
        url = self.comments_ajax_url + urllib.parse.urlencode(parms)
        try:
            response = requests.get(url, headers=self.ajax_headers)
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError as e:
            print('Error', e.args)

    # 从返回的json字符串中获取想要的字段
    def parse_page(self,originJson,page):
        if originJson:
            items = originJson.get('data').get('comments')
            for item in items:
                comments = {
                    'shopName': self.shopName,
                    'page':page,
                    'username': item.get('userName'),
                    'user-icon': item.get('userUrl'),
                    'stars': item.get('star'),
                    'user-comment': item.get('comment'),
                    'user-comment-time': item.get('commentTime'),
                    'user-comment-zan': item.get('zanCnt')}
                yield comments

    def get_comments(self):
        commentsData = [] #用于存储最终的结果，然后将结果保存到数据库中
        for page in range(1, self.maxPage):
            print('我现在已经爬取到第'+str(page)+'页啦~')
            original_data = self.get_page(page)
            results = self.parse_page(original_data,page)
            for result in results:
                commentsData.append(result)
        return commentsData

# 将数据保存到csv中
class SaveDataInFiles():
    def __init__(self, results=''):
        # 需要保存的数据
        self.results = results

    # 出口文件
    def saveResults(self):
        self.saveInCsv()
        # self.saveInTxt()

    # 将结果ip保存到D:\python\meituan\output_file\comments.txt中
    def saveInTxt(self):
        txt = open('D:\python\meituan\output_file\comments.txt', 'w')
        txt.truncate()  # 保存内容前先清空内容
        for item in self.results:
            itemStr = str(item)
            txt.write(itemStr)
            txt.write('\n')
        txt.close()

    # 将结果保存到D:\python\meituan\output_file\comments.csv中
    def saveInCsv(self):
        csvUrl = 'D:\python\meituan\output_file\comments.csv'
        pd.DataFrame(self.results).to_csv(csvUrl, encoding="utf-8-sig")  # 避免保存的中文乱码

#######################################################################################################################
##########################################################################
######################          主函数         ###########################
##########################################################################
if __name__ == '__main__':
    # 获取店铺的基本信息：名字，评论标签，最大页码
    basicInfo = GetShopInformation().get_basic_information()
    # 获取店铺的所有评论
    commentsRes = GetShopComments(basicInfo).get_comments()

    # 清空数据库数据
    # mongoDB('meituan', 'comments').delete_database()
    # mongoDB('meituan', 'commentsTag').delete_database()

    # 将评论数据保存到mongoDB数据库中
    # mongoDB('meituan','comments',commentsRes).save_to_Mongo()

    # 将店铺基本数据保存到mongoDB中
    # tmp = []
    # tmp.append(basicInfo)
    # mongoDB('meituan','commentsTag',tmp).save_to_Mongo()

    # 查询mongoDB的数据
    # mongoDB('meituan','comments').selectMongoDB()
    # mongoDB('meituan','commentsTag').selectMongoDB()

    # 保存数据到files中
    SaveDataInFiles(commentsRes).saveResults()