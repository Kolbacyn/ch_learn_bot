Bot assisting in studying Chinese with Telegram

![Telegram](https://img.shields.io/badge/Telegram-blue?style=for-the-badge&logo=telegram)
[![Scrapy](https://img.shields.io/badge/scrapy-%14fa1c.svg?style=for-the-badge&logo=scrapy&logoColor=white)](https://scrapy.org/)

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
