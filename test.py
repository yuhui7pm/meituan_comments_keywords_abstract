'''
    这里是用来测试的文件
'''

# from selenium import webdriver
# import random
# proxy_list = [
#     {"http" : "124.205.155.148:9090"},
#     {"http" : "124.205.155.154:9090"},
#     {"http" : "222.189.191.205:9999"},
#     {"http" : "61.145.49.175:9999"},
#     {"http" : "218.21.96.128:58080"},
#     {"http": "123.8.114.2:9999"},
#     {"http": "36.250.156.55:9999"},
# ]
# proxy = '127.0.0.1:9743'
# randomProxyUrl = random.choice(proxy_list)['http']
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://' + proxy)
# chrome = webdriver.Chrome(options=chrome_options)
# chrome.get('http://httpbin.org/get')

# from selenium import webdriver
# PROXY = "124.205.155.148:9090"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
# chrome = webdriver.Chrome(options=chrome_options)
# chrome.get('http://1212.ip138.com/ic.asp')
# print('2: ', chrome.page_source)
# chrome.quit()

# from selenium import webdriver
# proxy = '218.22.7.62:53281'
# chromeOptions = webdriver.ChromeOptions()
# chromeOptions.add_argument('--proxy-server=http://'+proxy)
# driver = webdriver.Chrome(options=chromeOptions)
# driver.get("https://www.baidu.com")

from selenium import webdriver
# 获取cookie信息
browser = webdriver.Chrome()
browser.get("https://st.meituan.com/")
cookie = browser.get_cookies()
# 打印cookie信息
print(cookie)
# 退出浏览器
# browser.quit()