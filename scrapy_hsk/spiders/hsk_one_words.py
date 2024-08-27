import scrapy

from scrapy_hsk.items import WordItem


class HskOneWordsSpider(scrapy.Spider):
    """Scrapy spider for HSK 1 level words"""
    name = 'hsk_one_words'
    allowed_domains = ["myhsk.org"]
    start_urls = ["https://myhsk.org/hsk-1-slova-online/"]

    def parse(self, response):
        """Parse HSK 1 level words from the website"""
        for word in response.css('tbody tr'):
            data = {
                'word': word.css('tr td.column-1::text').get(),
                'transcription': word.css('tr td.column-2::text').get(),
                'rus_translation': word.css('tr td.column-3::text').get(),
                'level': 1
            }
            yield WordItem(data)
