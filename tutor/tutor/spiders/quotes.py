import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quots"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                    'text': quote.css('span.text::text').extract_first(),
                    'author': quote.css('small.author::text').extract_first()
                }
                
                
                
                
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,self.parse)
