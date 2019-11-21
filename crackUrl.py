import base64
import zlib
import requests
import urllib
import pymongo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re

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

# 获取cookies和最大页码数
class GetBasicInfo():
    def __init__(self):
        self.url = "https://st.meituan.com/meishi/"
        self.headers = {
            'Host': 'st.meituan.com',
            'Referer': 'https://st.meituan.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }

    def get_uuid(self):
        """获取uuid"""
        url = 'https://st.meituan.com/meishi/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
        res = requests.get(url, headers=headers).text
        print(res)
        #findall(pattern, string, flags=0),返回string中所有与pattern相匹配的全部字串
        uuid = re.findall(r'"uuid":"(.*?)"', res, re.S)[0]
        with open('./output_file/uuid.log', 'w') as f:
            print('uuid:',uuid)
            f.write('chrome_uuid:'+uuid)

    # 访问美团
    # def get_basic_information(self):
    #     #初始化数据
    #     arr = []
    #     list = {}
    #     #建立连接
    #     chrome_options = webdriver.ChromeOptions()
    #     browser = webdriver.Chrome(options=chrome_options)
    #     browser.get(self.url)
    #     browser.implicitly_wait(10)  # 隐式等待
    #
    #     # 从美团首页跳转到详情页
    #     browser.find_element_by_css_selector('.category-nav-content-wrapper ul li:first-child .nav-text-wrapper').click()  # 点击按钮
    #     flag = WebDriverWait(browser,10).until(EC.presence_of_all_elements_located(By.CSS_SELECTOR('.pagination.clear li:nth-last-child(2)')))
    #     if flag:
    #         #获取cookie
    #         cookie = browser.get_cookies()
    #         for item in cookie:
    #             if item.get('name')=="uuid":
    #                 list['cookie_uuid'] = item.get('value')
    #                 print(item.get('value'))
    #         # 获取最大页码
    #         shopsMaxPage = browser.find_element_by_css_selector('.pagination.clear li:nth-last-child(2)').text
    #     browser.quit()
    #     list['shopsMaxPage'] = shopsMaxPage
    #     print('最大页码:',shopsMaxPage)
    #     arr.append(list)
    #     return arr

#获取cookie和最大页码数
data = GetBasicInfo().get_uuid()

#将数据保存到mongoDB中
# mongoDB('meituan','shopsInterfaceInfo',data)

# def decode_token(token):
#     # base64解码
#     token_decode = base64.b64decode(token.encode())
#     # 二进制解压
#     token_string = zlib.decompress(token_decode)
#     return token_string

# cityName: 汕头
# cateId: 0
# areaId: 0
# dinnerCountAttrId:
# page: 2
# originUrl: https://st.meituan.com/meishi/pn2/
# optimusCode: 10

# partical = 'https://st.meituan.com/meishi/api/poi/getPoiList?' \
#     'cityName=%E6%B1%95%E5%A4%B4&cateId=0&areaId=0&sort=&dinnerCountAttrId=&page=2&userId=&uuid=2255e41b-3773-4178-8eb7-6 \
#     12f440d2148&platform=1&partner=126&originUrl=https%3A%2F%2Fst.meituan.com%2Fmeishi%2Fpn2%2F&riskLevel=1&optimusCode=10'
#
# token = [
#     'eJxVjttugkAQht9lb0tkVxB2TXqhSBGlBbGi0PQCcJWTqLCC2PTduyTtRZNJ/sN8k8wXqMw9GCMICYQCaGgFxgAN4EABAmA134xUWRqOZIwRJAKI/3fDoSqAqPJmYPyhYkVQZfWzL1yeP5AkyQLG5FP4tTK3Q5lPz5gcAQljl3osijUbnGjKbmE5iM8nkfs6SUX+AuDo6b1HpRERECF9kfcF1/BX2V9+5c/zozo9ltzRRVtkG7hss8kqoWJqVk24yIMo0bp8Cecx9adnN0F1ni0DbarqhnSctuvmYq86hSZPDnnY9+k8Yu/aq13cdKezKCPbydNDbFTsmvaqnV39VsH+NVzru5eczEoEfcPN/FRftK1q1F1ANw/rlsuY+FocBUd6vmLr8nC2frUuN2mi7bTwzZvU99kldPJdd9f2b8UExb523ZuR7trYaSwjQG6YyXPrcPAqA5VFEDBP2raRcnvxdMoMheZqGhy8rpiH7fMz+P4Bn2qN9g==',
#     'eJyFT9tuqkAU/Zd5lcjADDeTPjiWCiKVIqK16YMgCiqXMwyj0vTfO008D+fpJDtZl72ysvcXoO4ejBQILQglwDMKRkAZwqEOJMBasdEMjFQdQU0zLAmk/3qGakggofEzGH1g3ZQMbHz+GqHQHwpCWDJN61N6UCyoisX8ZlwRATljTTuS5ZYNy6xg3a4apnUpC97mhdxUqizO+F8IyUAUlpEoFHh+4O6B7K/2xWeirS2OlWDZ7HrpU4WNT/YbyUi2CAo1m0K/wzXMcR417jEh4dG8Tk7Uwcg5x67r7Mm4mS9XCrHpIkHcDKLsfgr0iwgtKk4OGjEd52YPgtI89INB7E1W5yDTZpvzGu+1sHs7vcQ81dxZHm5377RZ+jwlfmOtKup1nTvz1cqKLg6KFd7Y3X2dx3KYjK11ULfTOYu2h5f7PeyJ5yW6VVPeOdGmH3t/4kNvJC6crOd8X4tL3qPX19KcbnehVgY2eu5ZMU/VxfXWqnSDbnzptU/g+wfkjJsw',
#     'eJx9T11vqkAQ/S/7KpEFdvkw6YNrqSBSKSJamz4IoqDycZdlVZr+924T78N9uZNJzpmZk5MzX4C6ezBSILQglADPKBgBZQiHOpAAa8UFG0hTdWghURJI/91hA0sgofEzGH3oWJUMZHz+LkIxfyiahiTTtD6lB0WCqkj0r8YVEpAz1rQjWW7ZsMwK1u2qYVqXsuBtXshNpcoixv9FQJiVkTATeH7g7oHs7+yLr4RTWxwrwbLZ9dKnChuf7DeSkWwRFGo2hX6HapijPGrcY0LCo3mdnKiDNOccu66zJ+NmvlwpxKaLRONmEGX3U6BfhGhRcXLAxHScmz0ISvPQDwaxN1mdgwzPNuc12uOwezu9xDzF7iwPt7t32ix9nhK/sVYV9brOnflqZUUXR4sV3tjdfZ3HcpiMrXVQt9M5i7aHl/s97InnJbpVU9450aYfe3/iQ28kLpys53xfiyTv0etraU63uxCXga0996yYp+riemtVutFufOm1T+D7B4J0me0=',
#     'eJwlzc1tAjEQBeBeOPi2eG0Mu4o0h4hTpIgbBRg8wCjrH43HkVIIHdBApLSU1BErOb3v8PTeyjP6lwCjOnvBf5B8HHxE+Pm8fz++VKCUkPe5JXkW4d5RuQjFVvc5IJhRZaYrpSMvcBMp9UnrKuuIJM2n9TlH3V1vpEuyWhV/RbA9WPosGLtTZfFyyRzBKKb69orvuHTXzAKqVfz7bI0CWLvdojOnYTNNm8GZaR5mPE3DztiLc2Owxs2rX3xvSKs='
# ]
# # cts则为ts+100*1000
#
# for i in range(0, len(token)):
#     token1 = decode_token(token[i])
#     print(token1)


# [{'domain': '.meituan.com', 'expiry': 1579514383, 'httpOnly': False, 'name': 'ci', 'path': '/', 'secure': False, 'value': '117'},
#  {'domain': '.meituan.com', 'expiry': 1605866382, 'httpOnly': False, 'name': '_hc.v', 'path': '/', 'secure': False, 'value': '0a3e41de-c14e-f54c-8241-776aa294b7d8.1574330382'},
#  {'domain': '.meituan.com', 'httpOnly': True, 'name': 'lng', 'path': '/', 'secure': False, 'value': '116.724425'},
#  {'domain': '.meituan.com', 'httpOnly': True, 'name': 'lat', 'path': '/', 'secure': False, 'value': '23.377651'},
#  {'domain': '.meituan.com', 'expiry': 1668938381, 'httpOnly': False, 'name': '_lxsdk', 'path': '/', 'secure': False, 'value': '16e8d6733a991-0e7d1e29ff084d-b363e65-121886-16e8d6733aa60'},
#  {'domain': 'www.meituan.com', 'expiry': 1574330682.427232, 'httpOnly': False, 'name': 'webloc_geo', 'path': '/', 'secure': False, 'value': '23.412368%2C116.63813%2Cwgs84'},
#  {'domain': '.meituan.com', 'expiry': 1668938381, 'httpOnly': False, 'name': '_lxsdk_cuid', 'path': '/', 'secure': False, 'value': '16e8d6733a991-0e7d1e29ff084d-b363e65-121886-16e8d6733aa60'},
#  {'domain': '.meituan.com', 'httpOnly': True, 'name': 'uuid', 'path': '/', 'secure': False, 'value': '0b9780ce-b8dd-40c8-8b26-286d080780c2'},
#  {'domain': '.meituan.com', 'expiry': 1574332181, 'httpOnly': False, 'name': '_lxsdk_s', 'path': '/', 'secure': False, 'value': '16e8d6733ad-6bb-51b-9e6%7C%7C1'},
#  {'domain': 'www.meituan.com', 'expiry': 1574416782.128, 'httpOnly': True, 'name': 'client-id', 'path': '/', 'secure': False, 'value': 'b34ea182-e5b2-4e46-8e30-a6ffdcebbdd7'}]
