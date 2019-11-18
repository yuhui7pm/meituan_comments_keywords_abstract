# 解决动态渲染的问题
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pymongo;

#selenium设置代理
proxy = '202.20.16.82:10152'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://'+proxy)
browser = webdriver.Chrome(options=chrome_options)
#访问美团
# browser.get('https://www.meituan.com/meishi/41007600/')
# browser.implicitly_wait(10)#隐式等待
#商铺名字
shopName = browser.find_element_by_class_name('details').find_element_by_class_name('name')
shopName = shopName.text.replace('食品安全档案','')
shopName = shopName.replace('\n','',3)
print('shopName:',shopName)
#网友点评的标签
commentTags = browser.find_element_by_css_selector('.com-cont .tags.clear').text
commentTags = commentTags.replace('\n',' ',30)
print('commentTags:',commentTags)

#获取评论页码
commentMaxPage = browser.find_element_by_css_selector('.pagination.clear li:nth-last-child(2)').text
print('commentMaxPage:',commentMaxPage)
browser.close()

#存储数据到MongoDB
meituanStaticData = {
    'shopName': shopName,
    'commentTags': commentTags,
    'commentMaxPage': commentMaxPage
}
client = pymongo.MongoClient(host='localhost',port=27017)   #连接MongoDB
db = client['meituan']                    #选择数据库
collection = db['meituanStaticData']      #指定要操作的集合,表
collection.delete_many({})                #删除数据库内容
def save_to_Mongo(result):
    try:
        if collection.insert_one(result):
            print('存储到MongoDB成功', result)
    except Exception:
        print('存储到MongoDb失败', result)

save_to_Mongo(meituanStaticData)
for x in collection.find():
  print(x)

#清除缓存
browser.quit();
