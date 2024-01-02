import scrapy


class HskOneWordsSpider(scrapy.Spider):
    name = "hsk_one_words"
    allowed_domains = ["myhsk.org"]
    start_urls = ["https://myhsk.org/hsk-1-slova-online/"]

    def parse(self, response):
        for word in response.css('tbody tr'):
            yield {
                'hanzi': word.css('tr td.column-1::text').get(),
                'pinyin': word.css('tr td.column-2::text').get(),
                'russian': word.css('tr td.column-3::text').get()
            }
