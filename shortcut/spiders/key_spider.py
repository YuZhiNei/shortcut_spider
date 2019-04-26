# -*- coding: utf-8 -*-
import scrapy
from shortcut.items import ShortcutItem
import urllib.parse
import urllib.request
import simplejson


class KeySpiderSpider(scrapy.Spider):
    name = 'key_spider'
    allowed_domains = ['www.10000key.com']
    start_urls = ['http://www.10000key.com/']

    def parse(self, response):

        key_url = "https://www.10000key.com//KJ/api/file/getSearchFileName?userid= 10234"
        # data = {
        #     "userid": 10234,
        # }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        # data_url = key_url + urllib.parse.urlencode(data)
        # 获取页面
        res = urllib.request.urlopen(urllib.request.Request(url=key_url, headers=headers))
        # 读取 json 数据中的 data
        data_list = simplejson.loads(res.read().decode("utf-8"))['data']
        # {"flag": "Success", "msg": 200, "data": [{"img": ".", "filename": "MacOS", "fileid": "28"}]}
        # 遍历出 app 名字和对应 id
        for i in data_list:
            item = ShortcutItem()
            # app 名字
            item['appname'] = i['filename']
            # app 对应id
            fileid = i['fileid']

            yield scrapy.Request(url=key_url, callback=self.new_data, meta={'item': item, 'fileid': fileid}, dont_filter=True)

    def new_data(self, response):

        item = response.meta['item']
        fileid = response.meta['fileid']
        app_url = "https://www.10000key.com//KJ/api/FileDetail/searchFileDetailList?"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }
        data = {
            "fileid": fileid,
            "userid": 10234
        }
        data_url = app_url + urllib.parse.urlencode(data)
        res = urllib.request.urlopen(urllib.request.Request(url=data_url,headers=headers))
        app_info = simplejson.loads(res.read().decode("utf-8"))['data']
        if app_info:
            # 设计 json 格式 data:[{title:info,title1:info1}]
            ls = []
            for x in app_info:
                dic = dict()
                dic["detaltitle"] = x['detailtitle']
                dic["explain"] = x['explain']
                ls.append(dic)
            item['data'] = ls
            yield item
        else:
            pass

        pass
