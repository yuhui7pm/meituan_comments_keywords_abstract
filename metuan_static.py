import requests;

#主要用于获取html页面的数据，比如：
#店铺名 评论标签以及页码
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

shopUrl = 'https://www.meituan.com/meishi/41007600/';# 店铺的url
res = requests.get(shopUrl, headers=headers);# 利用requests对象的get方法,对指定的url发起请求,该方法会返回一个Response对象
print(res.text);# 通过Response对象的text方法获取网页的文本信息

#发现竟然是动态渲染的页面,无法直接获取其html结构