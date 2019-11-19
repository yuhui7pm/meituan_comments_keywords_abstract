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
#######################################################################################################################
#共用的数据

#######################################################################################################################
#数据到mongoDB
class SaveComments():
    def __init__(self,result):
        self.host = 'localhost'
        self.port = 27017
        self.databaseName = 'meituan'
        self.formName = 'comments'
        self.result = result

    def save_to_Mongo(self):
        client = pymongo.MongoClient(host=self.host, port=self.port)  # 连接MongoDB
        db = client[self.databaseName]  # 选择数据库
        collection = db[self.formName]  # 指定要操作的集合,表
        collection.delete_many({})  # 删除数据库内容
        try:
            if collection.insert_many(self.result):
                print('存储到MongoDB成功', self.result)
        except Exception:
            print('存储到MongoDb失败', self.result)
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
    def parse_page(self,originJson):
        if originJson:
            items = originJson.get('data').get('comments')
            for item in items:
                comments = {}
                comments['shopName'] = self.shopName
                comments['username'] = item.get('userName')
                comments['user-icon'] = item.get('userUrl')
                comments['stars'] = item.get('star')
                comments['user-comment'] = item.get('comment')
                comments['user-comment-time'] = item.get('commentTime')
                comments['user-comment-zan'] = item.get('zanCnt')
                return comments

    def get_comments(self):
        commentsData = [] #用于存储最终的结果，然后将结果保存到数据库中
        for page in range(1, self.maxPage):
            print('page:',page)
            original_data = self.get_page(page)
            result = self.parse_page(original_data)
            commentsData.append(result)
        return commentsData
#######################################################################################################################
##########################################################################
######################          主函数         ###########################
##########################################################################
if __name__ == '__main__':
    # 获取店铺的基本信息：名字，评论标签，最大页码
    basicInfo = GetShopInformation().get_basic_information()
    # 获取店铺的所有评论
    commentsRes = GetShopComments(basicInfo).get_comments()
    # 将数据保存到mongoDB数据库中
    SaveComments(commentsRes).save_to_Mongo()
