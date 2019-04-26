# -*- coding: utf-8 -*-
import pymongo
from shortcut.settings import mongo_host, mongo_port, mongo_db_name, mongo_db_collection
import json


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShortcutPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        # 链接 mongodb
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        mybd = client[dbname]
        self.post = mybd[sheetname]

        # 存到本地，开打 json
        # self.f = open('shortcut.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 转换成字典
        data = dict(item)
        # 储存到 mongodb
        self.post.insert(data)

        # str = json.dumps(data, ensure_ascii=False)
        # 写入 json 文件
        # self.f.write(str + "\n")
        return item
