import scrapy

from scrapy_hsk.items import WordItem


class HskOneSentencesSpider(scrapy.Spider):
    """Scrapy spider for HSK 1 level sentences"""

    name = 'hsk_one_sentences'
    allowed_domains = ["myhsk.org"]
    start_urls = ["https://myhsk.org/hsk-4-slova-online/"]

    def parse(self, response):
        for word in response.css('tbody tr'):
            data = {
                'word': word.css('tr td.column-1::text').get(),
                'transcription': word.css('tr td.column-2::text').get(),
                'rus_translation': word.css('tr td.column-3::text').get(),
                'level': 6
            }
            yield WordItem(data)
