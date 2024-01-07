import scrapy

from scrapy_hsk.items import WordItem


class HskOneWordsSpider(scrapy.Spider):
    name = "hsk_one_words"
    allowed_domains = ["myhsk.org"]
    start_urls = ["https://myhsk.org/hsk-1-slova-online/"]

    def parse(self, response):
        for word in response.css('tbody tr'):
            data = {
                'word': word.css('tr td.column-1::text').get(),
                'transcription': word.css('tr td.column-2::text').get(),
                'rus_translation': word.css('tr td.column-3::text').get(),
                'level': 1
            }
            yield WordItem(data)
