# -*- coding: utf-8 -*-

# Scrapy settings for base_crawlers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'base_crawlers'

SPIDER_MODULES = ['base_crawlers.spiders']
NEWSPIDER_MODULE = 'base_crawlers.spiders'

ITEM_PIPELINES = ['base_crawlers.pipelines.HabrahabrMonthlyItemPipline']

DOWNLOAD_DELAY = 0.25

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

DEFAULT_REQUEST_HEADERS = {
    'Referer': 'http://habrahabr.ru/top/monthly/'
}
