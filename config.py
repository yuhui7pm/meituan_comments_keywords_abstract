import requests
import re  #用于正则表达式
import base64, zlib
import time
import random
import pandas as pd
import os
import urllib.parse
import json

#获得城市名，uuid和商铺数目
def getInfo():
    """获取uuid"""
    url = 'https://st.meituan.com/meishi/'  #汕头美食
    headers = {
        'Host': 'st.meituan.com',
        'Referer': 'https://st.meituan.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    }
    res = requests.get(url, headers=headers).text
    # findall(pattern, string, flags=0),返回string中所有与pattern相匹配的全部字串,r表示原生字符例：\n不表示换行。re.S表示作用域拓展到整个字符串，即包括换行符
    if res:
        uuid = re.findall(r'"uuid":"(.*?)"', res, re.S)[0]
        city = re.findall(r'"chineseFullName":"(.*?)"',res,re.S)[0]
        shopsNum = re.findall(r'"totalCounts":(\d+)',res,re.S)[0]
        with open('./output_file/uuid_city_shopsNum.log', 'w',encoding="utf-8") as f:
            print('chrome_uuid:'+uuid+'\n'+'city:'+city+'\n'+'shopsNum:'+str(shopsNum))
            f.write('chrome_uuid:'+uuid+'\n'+'city:'+city+'\n'+'shopsNum:'+str(shopsNum))
    ans = {
        'uuid':uuid,
        'city':city,
        'shopsNum':shopsNum
    }
    return ans
ans = getInfo()

DATA = {
    "cityName": '汕头',
    "cateId": '0',
    "areaId": "0",
    "sort": "",
    "dinnerCountAttrId": "",
    "page": "1",
    "userId": "",
    "uuid": ans['uuid'],
    "platform": "1",
    "partner": "126",
    "originUrl": "https://{}.meituan.com/meishi".format('st'),
    "riskLevel": "1",
    "optimusCode": "1"
}
SIGN_PARAM = "areaId={}&cateId={}&cityName={}&dinnerCountAttrId={}&optimusCode={}&originUrl={}/pn{}/&page={}&partner={}&platform={}&riskLevel={}&sort={}&userId={}&uuid={}".format(
    DATA["areaId"],
    DATA["cateId"],
    re.findall(r"b'(.+?)'",str(DATA["cityName"].encode(encoding='UTF-8',errors='strict')))[0],
    DATA["dinnerCountAttrId"],
    DATA["optimusCode"],
    DATA["originUrl"],
    DATA["page"],
    DATA["page"],
    DATA["partner"],
    DATA["platform"],
    DATA["riskLevel"],
    DATA["sort"],
    DATA["userId"],
    DATA["uuid"]
)

def encrypt(data):
    """压缩编码"""
    binary_data = zlib.compress(data.encode())#二进制压缩
    base64_data = base64.b64encode(binary_data)     #base64编码
    return base64_data.decode()                     #返回utf-8编码的字符串

def token():
    """生成token参数"""
    ts = int(time.time()*1000)  #获取当前的时间，单位ms
    #brVD和brR为设备的宽高，浏览器的宽高等参数，可以使用事先准备的数据自行模拟
    json_path = os.path.dirname(os.path.realpath(__file__))+'\\utils\\br.json'
    df = pd.read_json(json_path)
    brVD,brR_one,brR_two = df.iloc[random.randint(0,len(df)-1)]#iloc基于索引位来选取数据集
    TOKEN_PARAM ={
            "rId": 100900,
            "ver": "1.0.6",
            "ts": ts,  # 变量
            "cts": ts + random.randint(100, 120),  # 经测,cts - ts 的差值大致在 90-130 之间
            "brVD": eval(brVD),  # 变量
            "brR": [eval(brR_one), eval(brR_two), 24, 24],
            "bI": ["https://st.meituan.com/meishi/", ""],  # 从哪一页跳转到哪一页
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "aM": "",
            "sign": encrypt(SIGN_PARAM)
    }
    # 二进制压缩
    binary_data = zlib.compress(json.dumps(TOKEN_PARAM).encode())
    # print('binary_data:',json.dumps(TOKEN_PARAM).encode())
    # base64编码
    base64_data = base64.b64encode(binary_data)
    # print('这里是token的使用了ascii编码之前的:', base64_data)
    # print('这里是token的使用了ascii编码之后的:',urllib.parse.quote(base64_data.decode(),'utf-8'))
    return urllib.parse.quote(base64_data.decode(),'utf-8')

AJAXDATA = {
    'basicUrl':'https://st.meituan.com/meishi/api/poi/getPoiList?',
    'cityName': '%E6%B1%95%E5%A4%B4',
    'cateId': 0,
    'areaId': 0,
    'sort': '',
    'dinnerCountAttrId': '',
    'page': '1',
    'userId': '',
    'uuid': ans['uuid'],
    'platform': 1,
    'partner': 126,
    'originUrl': 'https%3A%2F%2Fst.meituan.com%2Fmeishi%2F',
    'riskLevel': 1,
    'optimusCode': 10,
    '_token': token()
}
urlParam = 'https://st.meituan.com/meishi/api/poi/getPoiList?cityName={}&cataId={}&areaId={}&sort={}&dinnerCountAttrId={}' \
           '&page={}&userId={}&uuid={}&platform={}&partner={}&originUrl={}&riskLevel={}&optimusCode={}&_token={}'.format(
    AJAXDATA['cityName'],
    AJAXDATA['cateId'],
    AJAXDATA['areaId'],
    AJAXDATA['sort'],
    AJAXDATA['dinnerCountAttrId'],
    AJAXDATA['page'],
    AJAXDATA['userId'],
    AJAXDATA['uuid'],
    AJAXDATA['platform'],
    AJAXDATA['partner'],
    AJAXDATA['originUrl'],
    AJAXDATA['riskLevel'],
    AJAXDATA['optimusCode'],
    AJAXDATA['_token'],
)

print('ajax:',urlParam)
