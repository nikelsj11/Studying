# -*- coding: utf-8 -*-
from collections import defaultdict
import re
from scrapy import Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from base_crawlers.items import HabrahabrMonthlyItem


class HabrahabrMonthlyCrawler(CrawlSpider):
    name = 'habrahabr_monthly_crawler'

    allowed_domains = ["habrahabr.ru"]
    start_urls = ["http://habrahabr.ru/top/monthly/page1/"]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'top/monthly/page\d+/',)), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        body_selector = Selector(text=response.body, type="html")
        links = body_selector.xpath('//a[@class="button habracut"]/@href').extract()
        for link in links:
            yield Request(url=link, callback=self.parse_item)

    @staticmethod
    def parse_item(response):
        article_id = re.search(r'/(\d+)/', response.url).group(1)

        l = ItemLoader(item=HabrahabrMonthlyItem(), selector=Selector(text=response.body, type="html"))
        l.add_xpath('title', '//span[@class="post_title"]//text()')
        l.add_xpath(
            'author',
            '//a[re:test(@class, "(author-info__nickname)|(post-type__value_author)")]//text()')
        l.add_xpath('rating', '//span[@class="voting-wjt__counter-score js-score"]//text()')
        l.add_xpath('views', '//div[@class="views-count_post"]//text()')
        l.add_xpath('comments', '//span[@id="comments_count"]//text()')
        l.add_xpath('stars', '//span[@class="favorite-wjt__counter js-favs_count"]//text()')
        l.add_xpath('tags', '//div[@class="hubs"]//a//text()')
        l.add_xpath('article_text', '//div[@class="content html_format"]')
        l.add_value('article_id', article_id)

        return l.load_item()
