from parser.celery import app
from parser.parser import Parser
from news.models import News
from django.core.exceptions import ObjectDoesNotExist
import time



@app.task
def check_news():
    last_news = Parser().get_last_news()
    try:
        News.objects.get(news_id=last_news['news_id'])
    except ObjectDoesNotExist:
        News.objects.create(
            title=last_news['title'],
            text=last_news['text'],
            address=last_news['addresses'],
            news_id=last_news['news_id'],
            is_new=True,
        )

@app.task
def demo():
    five_news = Parser().demo()
    for last_news in five_news:
        try:
            News.objects.get(news_id=last_news['news_id'])
        except ObjectDoesNotExist:
            News.objects.create(
                title=last_news['title'],
                text=last_news['text'],
                address=last_news['addresses'],
                news_id=last_news['news_id'],
                is_new=True,
            )
        time.sleep(30)