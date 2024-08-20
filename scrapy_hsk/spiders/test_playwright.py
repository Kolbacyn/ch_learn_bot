import scrapy
from scrapy_playwright.page import PageMethod

from scrapy_hsk.items import QuoteItem


class TestPlaywrightSpider(scrapy.Spider):
    name = "test_playwright"
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def start_requests(self):
        url = "https://quotes.toscrape.com/js/"
        yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
