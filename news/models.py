from django.db import models
from django.contrib.postgres.fields import ArrayField


class News(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    address = ArrayField(models.TextField(), blank=True)
    news_id = models.IntegerField()
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return str(self.news_id)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
