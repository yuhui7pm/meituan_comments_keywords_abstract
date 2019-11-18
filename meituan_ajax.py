import requests;               #模拟浏览器向服务器发出请求
import urllib.parse;           #定义了url的标准接口，实现url的各种抽取
from bs4 import BeautifulSoup; #html和xml的解析库，用于从网页中提取数据

base_url ="https://www.meituan.com/meishi/api/poi/getMerchantComment?";
headers = {
    'Host': 'www.meituan.com',
    'Referer': 'https://www.meituan.com/meishi/41007600/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
}
# https://www.meituan.com/meishi/api/poi/getMerchantComment?uuid=4344eb25-c171-4c19-9d82-278ba5f01224&platform=1&partner=126
# &originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F41007600%2F&riskLevel=1&optimusCode=10&id=41007600&userId=&offset=0&pageSize=10&sortType=1
# 获取请求的结果
def get_page(items):
    parms = {
        'uuid':'4344eb25-c171-4c19-9d82-278ba5f01224',
        'platform':'1',
        'partner':'126',
        'originUrl':'https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F41007600%2F',
        'riskLevel':'1',
        'optimusCode':'10',
        'id':'41007600',
        'userId':'',
        'offset':items,
        'pageSize':'10',
        'sortType':'1',
    }
    url = base_url + urllib.parse.urlencode(parms)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error',e.args)

#从返回的json字符串中获取想要的字段
def parse_page(json):
    if json:
        items = json.get('data').get('comments')
        for item in items:
            comments = {}
            comments['username'] = item.get('userName');
            comments['user-icon'] = item.get('userUrl');
            comments['stars'] = item.get('star');
            comments['user-comment'] = item.get('comment');
            comments['user-comment-time'] = item.get('commentTime');
            comments['user-comment-zan'] = item.get('zanCnt');
            yield comments;

# 遍历page，输出提取到的结果
if __name__ == '__main__':
    for page in range(1,897):
        json = get_page(page);
        results = parse_page(json)
        for result in results:
            print(result)