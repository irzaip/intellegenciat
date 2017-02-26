# -*- coding: utf-8 -*-
import scrapy


class ScrapSpider(scrapy.Spider):
    name = "scrap"
    allowed_domains = ["basic"]
    start_urls = ['http://quotes.toscrape.com/']
    def start_request(self):
	    scrapy.Request(url=start_urls,callback=self.parse)

    def parse(self, response):
    	print response.bodys
        pass
