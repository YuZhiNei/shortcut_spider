# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShortcutItem(scrapy.Item):

    # APP名字
    appname = scrapy.Field()

    # 快捷键与说明都集合在 data
    data = scrapy.Field()
