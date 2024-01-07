from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Word


class WordToDBPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        word = Word(
            word=item['word'],
            transcription=item['transcription'],
            rus_translation=item['rus_translation'],
            level=item['level']
        )
        self.session.add(word)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
