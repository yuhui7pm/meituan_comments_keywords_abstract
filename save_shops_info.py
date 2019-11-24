'''
    保存每个列表页所有商铺的基本信息
'''
import requests
import json
from get_shops import get_shops_url
from save_data import MongoDB
from save_data import SaveDataInFiles

output = [] #初始化数组，用于保存最终的结果
index = 1
# 定义类获取评论数据
def get_shops_info(ajax_url):
    url = ajax_url  # getshops传递过来的ajax_url
    headers = {
        'Host': 'st.meituan.com',
        'Referer': 'https://st.meituan.com/meishi/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    try:
        response = requests.get(url, headers=headers)
        # print('response:',response)
        # print('response_text:',response.text)
        # print('type(eval(response.text)):',type(eval(response.text)))
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

# 从返回的json字符串中获取想要的字段
def save_shops_info(ajax_url,index):
    items = get_shops_info(ajax_url).get('data').get('poiInfos')
    output.extend(items)
    print('正在追加内容到output数组中')

if __name__ == '__main__':
    # for ajaxUrl in get_shops_url:
    #     save_shops_info(ajaxUrl,index)
    #保存数据到数据库中
    collection = MongoDB('shops_info','','').collect_database()    #连接数据库
    # MongoDB('shops_info', collection, '').delete_database()  # 先清空数据库内容
    # MongoDB('shops_info', collection, output).save_to_Mongo()
    # 保存数据到csv中
    # SaveDataInFiles('D:\python\meituan\output_file\shops_info.csv', '', output).saveInCsv()
    #将数据保存到json文件夹中
    # with open('D:\python\meituan\output_file\shops_info.json', 'w') as f:
    #     json.dump(output, f)
    # 查询数据库数据
    MongoDB('shops_info',collection,'').selectMongoDB()


