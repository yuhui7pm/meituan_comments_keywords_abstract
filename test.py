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

# from selenium import webdriver
# # # 获取cookie信息
# # browser = webdriver.Chrome()
# # browser.get("https://st.meituan.com/")
# # cookie = browser.get_cookies()
# # # 打印cookie信息
# # print(cookie)
# # # 退出浏览器
# # # browser.quit()

# import base64
# import zlib
# def decode_token(token):
#     # base64解码
#     token_decode = base64.b64decode(token.encode())
#     # 二进制解压
#     token_string = zlib.decompress(token_decode)
#     return token_string
#
# token = [
#         'eJx1T9tuqkAU/Zd5LZEZZ8rFpA+KFFFaECsKTR8AR7mJCiMjNuffzzTxPJyHJjtZl72ysvc3aOwdGCEIdQgl0NEGjAAawIECJMBasXlWCSYKInCIRSD938MYSyBpgikYfeKhJqlE/foxfKE/EcZE0jT9S3pQIuiQiPnJ2CICMsbO7UiWWzY40pxd43qQno6y4G2Wy+KEXwJANBw/RIPA8oHxA9k//SZeERVtfqgFo3NeFWu44MV4mVE5t5sunpdRkhl9uYCzlIaTk5+htiwWkTFRTQsfJnzVnd1lr9DsydPv7m0yS9iH8eZWV9PrHcr0zfjpLneq5tvukk8vIVe08BKvzO1rqU9rBEPLL8LcnHOuWm0f0fXduZZE00MjTaIDPV0053z3NmGzqtd5ZmyN+D0Yt7fpOfbKbX8zdu/VGKWhcdnZiem7mtc5VoT8uCAzZ78PGgvVVRSxAG94olxfA5MyS6Glmkf7oK9mMX95AX/+AuZIlIo=',
#         'eJx9T12PojAU/S99lUihRajJPliHEURGBhEdJ/MgiILKx5ZSlc3+9+0k7sO+bHKT83FPTu79BZh7AGMNQgKhAkTGwBhoQzgcAQXwVm4MEyM8MqBJdF0B6T+eBRFRQMLiFzD+RMRUTGx+fRuh1J8aQlixLPKlPCmWVMdyvjOujICc86Ydq2rLh2VW8G5fDdO6VCVv80JtKl2VZ/w/BGRZGckyiZcn7p/I/2pffiWb2uJUSZbNb9c+1fjkbL/TjGbLoNCzGfQ7XMMc51HjnhIanqzb9MwcjJxL7LrOgU6axWqtUZstEySsIMoe52B0laFlJejRoJbj3O1BUFrHfjCIven6EmTGfHvZ4IMRdu/n11ikhjvPw93+gzUrX6TUb8i6Yl7XuXNfr0h0dVCsicbuHps8VsNkQjZB3c4WPNodXx+PsKeel4xIzUTnRNt+4v2Mj72ZuHC6WYhDLS/5iN7eSmu224dGGdjopefFItWXt3ursy26i5XX/gC//wCK9Zny',
#         "eJwlzc1tAjEQBeBeOPi2eG0Mu4o0h4hTpIgbBRg8wCjrH43HkVIIHdBApLSU1BErOb3v8PTeyjP6lwCjOnvBf5B8HHxE+Pm8fz++VKCUkPe5JXkW4d5RuQjFVvc5IJhRZaYrpSMvcBMp9UnrKuuIJM2n9TlH3V1vpEuyWhV/RbA9WPosGLtTZfFyyRzBKKb69orvuHTXzAKqVfz7bI0CWLvdojOnYTNNm8GZaR5mPE3DztiLc2Owxs2rX3xvSKs="
# ]
#
# for i in range(0, len(token)):
#     token1 = decode_token(token[i])
#     print(token1)

# import re;
# print(re.findall(r"b'(.+?)'",str(b'\xe6\xb1\x95\xe5\xa4\xb4'))[0])

# import execjs
# # eval 和 complie 是要构建一个JS的环境
# iN = execjs.compile('''function IN() {
#     var hR = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
#     var hK = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
#     return [hR, hK]
# };''')
#
# iM = execjs.compile('''function IM() {
#     var iZ = [screen.width, screen.height];
#     var iW = [screen.availWidth, screen.availHeight];
#     var iX = screen.colorDepth;
#     var iY = screen.pixelDepth;
#     return [iZ, iW, iX, iY]
# };''')
#
# print(iN.call('IN'))  # execjs.compile用于执行更复杂的js代码