Bot assisting in studying Chinese with Telegram

![Telegram](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=telegram)
[![Scrapy](https://img.shields.io/badge/scrapy-%14fa1c.svg?style=for-the-badge&logo=scrapy&logoColor=white)](https://scrapy.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=SQLAlchemy&logoColor=SQLAlchemy)](https://www.sqlalchemy.org/)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)

## Quick start

First, clone this repository:

```bash
git clone git@github.com:Kolbacyn/ch_learn_bot.git
```

Second, create and activate virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate
```
Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Create an empty `.env` file and add bot token to it:

```bash
BOT_TOKEN=1234567890:ABCDefghijklmnopqrstuvwxyz

```

Finally, run bot:

```bash
python main.py
```


## Filling database

To fill database with sentences, run:

```bash
python filling_db.py
```

Bot contains pre-processed .csv files with sentences. Command `python filling_db.py` will fill database with sentences from these files.
