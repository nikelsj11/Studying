# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HabrahabrMonthlyItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()
    views = scrapy.Field()
    comments = scrapy.Field()
    stars = scrapy.Field()
    tags = scrapy.Field()
    article_id = scrapy.Field()
    article_text = scrapy.Field()
