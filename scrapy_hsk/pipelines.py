from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from scrapy_hsk.models import Base, Word


class WordToDBPipeline:
    """Pipeline adding words to the database"""
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db', echo=False)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        existing_word = self.session.query(Word).filter_by(word=item['word']).first()
        if existing_word:
            raise DropItem(
                f'Word "{item["word"]}" already exists in the database.'
                )

        # Если слово не найдено, добавляем его в базу
        word = Word(
            word=item['word'],
            transcription=item['transcription'],
            rus_translation=item['rus_translation'],
            level=item['level']
        )
        self.session.add(word)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()  # В случае ошибки откатываем транзакцию
            raise DropItem(
                f'Failed to add word "{item["word"]}" due to integrity error.'
                )

        return item

    def close_spider(self, spider):
        self.session.close()
