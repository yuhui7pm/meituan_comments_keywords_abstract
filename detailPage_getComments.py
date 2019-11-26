'''
    根据数据库中汕头市外卖商铺信息，爬取所有商铺的评论信息
'''
# 爬取美团外卖评论 https://www.meituan.com/meishi/41007600/
import requests  # 模拟浏览器向服务器发出请求
import math
import urllib.parse  # 定义了url的标准接口，实现url的各种抽取
from selenium import webdriver
from save_data import MongoDB
from save_data import SaveDataInFiles
from config import ans
from requests.adapters import HTTPAdapter


#######################################################################################################################
# 定义类获取商铺评论标签和所有评论
class GetShopComments():
    def __init__(self, shopBasicInfo, uuid, shop_num=''):
        self.comments_ajax_url = "https://www.meituan.com/meishi/api/poi/getMerchantComment?"
        self.ajax_headers = {
            'Host': 'www.meituan.com',
            'Referer': 'https://www.meituan.com/meishi/41007600/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        # 前面GetShopInformation的类中传递过来的最大页数
        self.maxPage = math.ceil(shopBasicInfo['allCommentNum'] / 10)
        self.shopName = shopBasicInfo['title']
        self.poiId = shopBasicInfo['poiId']
        self.uuid = uuid['uuid']
        # self.uuid = uuid
        self.shop_num = shop_num


    # 获取每个店铺页面上的所有数据(json格式)，标签+评论
    def get_comments_in_page(self, items):
        parms = {
            'uuid': self.uuid,
            'platform': '1',
            'partner': '126',
            'originUrl': 'https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F' + str(self.poiId) + '%2F',
            'riskLevel': '1',
            'optimusCode': '10',
            'id': self.poiId,
            'userId': '',
            'offset': items,
            'pageSize': '10',
            'sortType': '1',
        }
        url = self.comments_ajax_url + urllib.parse.urlencode(parms)
        # 连接超时，重新连接
        request = requests.Session()
        request.mount('http://', HTTPAdapter(max_retries=3))
        request.mount('https://', HTTPAdapter(max_retries=3))
        try:
            response = request.get(url, headers=self.ajax_headers,timeout=10)
            if response.status_code == 200:
                return response.json()
        # except requests.ConnectionError as e:
        except requests.exceptions.Timeout as e:
            print('Error', e.args)

    # 解析json数据，并获取评论数据
    def parse_comments_in_page(self, originJson, page):
        if originJson:
            items = originJson.get('data').get('comments')
            if items:
                for item in items:
                    comments = {
                        'shopName': self.shopName,
                        'page': page,
                        'username': item.get('userName'),
                        'user-icon': item.get('userUrl'),
                        'stars': item.get('star'),
                        'user-comment': item.get('comment'),
                        'user-comment-time': item.get('commentTime'),
                        'user-comment-zan': item.get('zanCnt')}
                    yield comments

    # 解析json数据，并获取标签评论数据
    def parse_comments_tags(self):
        if self.maxPage > 0:
            original_data = self.get_comments_in_page(1)
            if original_data:
                tags = original_data.get('data').get('tags')
                if tags:
                    for item in tags:
                        item['poiId'] = self.poiId
                        item['shopName'] = self.shopName
                    return tags
    # 评论数据的入口和出口
    def get_comments(self):
        commentsData = []  # 用于存储最终的结果，然后将结果保存到数据库中
        if self.maxPage > 0:
            for page in range(1, self.maxPage + 1):
                print('我现在已经爬取到第' + str(shop_num) + '家店铺的第' + str(page) + '页啦~')
                original_data = self.get_comments_in_page(page)
                results = self.parse_comments_in_page(original_data, page)
                for result in results:
                    commentsData.append(result)
            return commentsData

    # 评论标签数据


#######################################################################################################################

if __name__ == '__main__':
    shop_num = 315  # 用于统计爬到哪一家店铺
    # 开启新数据库用于保存评论数据
    tags_collection = MongoDB('shops_tags', '', '').collect_database()  # 连接数据库
    comments_collection = MongoDB('shops_comments', '', '').collect_database()  # 连接数据库
    # 查看数据库内容
    # MongoDB('shops_tags',tags_collection).selectMongoDB()
    # 清空数据库
    # MongoDB('shops_tags', tags_collection).delete_database()
    # MongoDB('shops_comments', comments_collection).delete_database()
    # 获取前面数据库中保存的商家数据
    collection = MongoDB('shops_info', '', '').collect_database()  # 连接数据库
    shops = collection.find({}, {"poiId": 1, "title": 1, "allCommentNum": 1})  # 只输出id和title字段，第一个参数为查询条件，空代表查询所有
    shops = list(shops)  # 将游标转换成数组
    for items in shops[315:]:
        shop_num = shop_num + 1  # 用于统计爬到哪一家店铺
        commentsRes = GetShopComments(items, ans, shop_num).get_comments()  # 获取店铺的所有评论
        tagsRes = GetShopComments(items, ans).parse_comments_tags()  # 获取评论标签
        MongoDB('shops_tags', tags_collection, tagsRes).save_to_Mongo()  # 保存评论标签数据
        MongoDB('shops_comments', comments_collection, commentsRes).save_to_Mongo()  # 保存评论数据
        SaveDataInFiles('D:\python\meituan\output_file\shop_comments.csv', '', commentsRes).saveInCsv()  # 保存评论数据到csv文件中
        SaveDataInFiles('D:\python\meituan\output_file\shop_tags.csv', '', tagsRes).saveInCsv()  # 保存评论数据到csv文件中
