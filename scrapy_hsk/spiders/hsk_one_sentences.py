import scrapy

from scrapy_hsk.items import SentenceItem


class HskOneSentencesSpider(scrapy.Spider):
    """Scrapy spider for HSK 1 level sentences"""

    name = 'hsk_one_sentences'
    allowed_domains = ["https://hsk.academy.ru/"]
    start_urls = ['https://hsk.academy/ru/hsk-1-vocabulary-list']

    def parse(self, response):
        """Parse HSK 1 level sentences from the provided response."""
        content = response.css()
        print(content)
        #hsk-dynamic-content > div > ul > li:nth-child(1) > span
        #hsk-dynamic-content > div > ul > li:nth-child(2) > span
