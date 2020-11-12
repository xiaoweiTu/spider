# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    createTime = scrapy.Field()
    url = scrapy.Field()
    urlId = scrapy.Field()
    imageUrl = scrapy.Field()
    imagePath = scrapy.Field()
    zan = scrapy.Field()
    comments = scrapy.Field()
    reads = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    pass
