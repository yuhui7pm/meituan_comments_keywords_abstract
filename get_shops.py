import base64, zlib
import time
import random
import pandas as pd
import os
from config import SIGN_PARAM

def encrypt(data):
    """压缩编码"""
    binary_data = zlib.compress(data.encode())#二进制压缩
    base64_data = base64.b64encode(binary_data)     #base64编码
    print('base64_data',base64_data)
    return base64_data.decode()                     #返回utf-8编码的字符串

def token():
    """生成token参数"""
    ts = int(time.time()*1000)  #获取当前的时间，单位ms
    #brVD和brR为设备的宽高，浏览器的宽高等参数，可以使用事先准备的数据自行模拟
    json_path = os.path.dirname(os.path.realpath(__file__))+'\\utils\\br.json'
    df = pd.read_json(json_path)
    brVD,brR_one,brR_two = df.iloc[random.randint(0,len(df)-1)]#iloc基于索引位来选取数据集
    TOKEN_PARAM = {
        "rId": 100900,
        "ver": "1.0.6",
        "ts": ts,  # 变量
        "cts": ts + random.randint(100,120),# 经测,cts - ts 的差值大致在 90-130 之间
        "brVD": eval(brVD),  # 变量
        "brR": [eval(brR_one), eval(brR_two), 24, 24],
        "bI": ["https://st.meituan.com/meishi/",""],  #从哪一页跳转到哪一页
        "mT": [],
        "kT": [],
        "aT": [],
        "tT": [],
        "aM": "",
        "sign": encrypt(SIGN_PARAM)
    }
    encrypt(TOKEN_PARAM)