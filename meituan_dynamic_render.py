# 解决动态渲染的问题
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
browser = webdriver.Chrome()
browser.get('https://www.meituan.com/meishi/41007600/')
#商铺名字
shopName = browser.find_element_by_class_name('details').find_element_by_class_name('name')
shopNameText = shopName.text.replace('食品安全档案','')
shopNameText= shopNameText.replace('/n','')
#网友点评的标签
commentTags = browser.find_element_by_css_selector('.tags.clear li')
#获取评论页码
commentsPage = browser.find_element_by_css_selector('.pagination.clear li:nth-last-child(2)')
print(shopNameText,commentTags.text,commentsPage.text)
browser.close()
