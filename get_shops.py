import requests
import re  #用于正则表达式

#获得城市名，uuid和商铺数目
def getInfo():
    """获取uuid"""
    url = 'https://st.meituan.com/meishi/'  #汕头美食
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }
    res = requests.get(url, headers=headers).text
    # findall(pattern, string, flags=0),返回string中所有与pattern相匹配的全部字串,r表示原生字符例：\n不表示换行。re.S表示作用域拓展到整个字符串，即包括换行符
    uuid = re.findall(r'"uuid":"(.*?)"', res, re.S)[0]
    city = re.findall(r'"chineseFullName":"(.*?)"',res,re.S)[0]
    shopsNum = re.findall(r'"totalCounts":(\d+)',res,re.S)[0]
    with open('./output_file/uuid_city_shopsNum.log', 'w',encoding="utf-8") as f:
        print('uuid:', uuid,'\n','city:',city,'\n','shopsNum',shopsNum)
        f.write('chrome_uuid:'+uuid+'\n'+'city:'+city+'\n'+'shopsNum:'+str(shopsNum))

#获取一个城市所有店铺列表的poiInfos字段如下：
def shopListsAjax():
    basicUrl = 'https://st.meituan.com/meishi/api/poi/getPoiList?'
    param = {
        'cityName': '汕头',
        'cateId' : 0,
        'areaId' :0,
        'sort':'',
        'dinnerCountAttrId':'',
        'page':'1',
        'userId':'',
        'uuid':'2255e41b-3773-4178-8eb7-612f440d2148',
        'platform':1,
        'partner':126,
        'originUrl':'https%3A%2F%2Fst.meituan.com%2Fmeishi%2F',
        'riskLevel': 1,
        'optimusCode':10,
        '_token':'eJx1T01vqkAU%2FS%2BzLZGZMgJj0oUiRZQWxIpC0wXgKF%2BiwsiIL%2B%2B%2Fv2niW3TR5Cbn456c3PsHNPYOjBCEBEIJdLQBI4AGcKACCbBWbIYaVjAiz5ioIpD%2B8IZQQxJImmAKRp8a1iWVDL%2B%2BDV%2FoT6QoWNJ18iU9KBb0GYv5ztgiAjLGzu1Ills2ONKcXeN6kJ6OsuBtlsvihF8CQDQcP0SDwPKB8QPZf%2F0mXhEVbX6oBaNzXhVruODFeJlRObebLp6XUZIZfbmAs5SGk5OfobYsFpEx0UxLOUz4qju7y16l2ZNH7u5tMkvYh%2FHmVlfT6x3KyGb8dJc7Tfdtd8mnl5CreniJV%2Bb2tSTTGsHQ8oswN%2Beca1bbR3R9d64l1klopEl0oKeL7pzv3iZsVvU6z4ytEb8H4%2FY2Pcdeue1vxu69GqM0NC47OzF9V%2Fc6x4qQHxd45uz3QWOhuooiFigbnqjX18CkzFJpqeXRPuirWcxfXsDffxUqlKY%3D'
    }



getInfo()