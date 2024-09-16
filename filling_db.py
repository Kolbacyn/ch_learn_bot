import csv

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from scrapy_hsk.models import Base, Sentence
from utilities.constants import Database, Numeric

engine = create_engine(Database.SQLITE, echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


def process_csv_file(file) -> None:
    """Process csv file"""
    with open(file, encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            sentence = Sentence(
                sentence=row[Numeric.ZERO],
                transcription=row[Numeric.ONE],
                translation=row[Numeric.TWO],
                level=Numeric.TWO
            )
            session.add(sentence)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
        return


process_csv_file('utilities/sentences/level_2.csv')
