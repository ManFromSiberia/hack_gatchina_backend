from parser.celery import app


@app.task
def check_news():
    pass
