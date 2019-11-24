'''
    #获得城市名，uuid和商铺数目以及页数
'''

import requests
import re  #用于正则表达式
import math

#获得城市名，uuid和商铺数目以及页数
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
        'shopsNum':int(shopsNum),
        'pages':math.ceil(int(shopsNum)/15),
    }
    return ans
ans = getInfo()
