'''
    定义类用于保存数据到数据库，txt或者csv
'''
import pandas as pd           # 将数据保存到csv中
import pymongo

class MongoDB():
    def __init__(self,formName,collection='',result=''):
        self.host = 'localhost'
        self.port = 27017
        self.databaseName = 'meituan'
        self.formName = formName
        self.result = result
        self.collection = collection

    # 连接数据库
    def collect_database(self):
        client = pymongo.MongoClient(host=self.host, port=self.port)  # 连接MongoDB
        db = client[self.databaseName]  # 选择数据库
        collection = db[self.formName]  # 指定要操作的集合,表
        print('数据库已经连接')
        return collection

    # 保存数据
    def save_to_Mongo(self):
        # collection = self.collect_database()
        try:
            if self.collection.insert_many(self.result):
                # print('存储到MongoDB成功', self.result)
                print('存储到MongoDB成功')
        except Exception:
            print('存储到MongoDb失败', self.result)

    # 查询数据
    def selectMongoDB(self):
        # collection = self.collect_database()
        # print('评论数据的总长度为：',collection.count_documents({}))
        print('正在查询数据库')
        for x in self.collection.find():
            print(x)

    # 删除数据
    def delete_database(self):
        self.collection.delete_many({})  # 删除数据库内容
        print('已清空数据库')

class SaveDataInFiles():
    def __init__(self,csv_url='',txt_url='',results=''):
        # 需要保存的数据
        self.results = results
        self.csv_url = csv_url
        self.txt_url = txt_url

    # 出口文件
    def saveResults(self):
        self.saveInCsv()
        self.saveInTxt()

    # 将结果ip保存到D:\python\meituan\output_file\proxyIp_kuai.txt中
    def saveInTxt(self):
        txt = open(self.txt_url, 'w')
        txt.truncate()  # 保存内容前先清空内容
        for item in self.results:
            itemStr = str(item)
            txt.write(itemStr)
            txt.write('\n')
        txt.close()

    # 将结果保存到D:\python\meituan\output_file\proxyIp_kuai.csv中
    def saveInCsv(self):
        # print('csv:',self.results,self.csv_url)
        csvUrl = self.csv_url
        pd.DataFrame(self.results).to_csv(csvUrl, encoding="utf-8-sig")  # 避免保存的中文乱码
        print('保存到csv文件中成功了')