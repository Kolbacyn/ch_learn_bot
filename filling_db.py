import csv

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Sentence

engine = create_engine('sqlite:///sqlite_sentences.db', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


def process_csv_file(file):
    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            sentence = Sentence(
                sentence=row[0],
                transcription=row[1],
                translation=row[2],
                level=1
            )
            session.add(sentence)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
        return


process_csv_file('utilities/sentences/level_1.csv')
