import scrapy

from scrapy_hsk.items import SentenceItem


class HskOneSentencesSpider(scrapy.Spider):
    """Scrapy spider for HSK 1 level sentences"""

    name = 'hsk_one_sentences'
    allowed_domains = ['https://hsk.academy.ru/']
    start_urls = ['https://hsk.academy/ru/hsk-1-vocabulary-list']

    async def parse(self, response):
        # Используем Playwright для загрузки страницы
        page = response.meta['playwright_page']
        
        # Ждем, пока нужный элемент загрузится (например, элемент с классом .dynamic-content)
        await page.wait_for_selector('div#hsk-dynamic-content')

        # Получаем HTML содержимое после загрузки
        content = await page.content()

        # Парсим загруженный контент с помощью Scrapy Selector
        sel = scrapy.Selector(text=content)

        # Находим нужные элементы <li>
        list_items = sel.css('div#hsk-dynamic-content ul li span.theme_hanzi_2XzkQ::attr(data-tooltip)').getall()

        for item in list_items:
            yield {'item': item.strip()}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={'playwright': True})
