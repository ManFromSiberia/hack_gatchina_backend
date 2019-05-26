from django.db import models
from django.contrib.postgres.fields import ArrayField

from chat.models import Chat


class News(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    address = ArrayField(models.TextField(), blank=True)
    chats = models.ManyToManyField(
        Chat,
        related_name='news',
        verbose_name='Notification Chats',
        blank=True,
        null=True
    )
    news_id = models.IntegerField(blank=True, null=True)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return str(self.news_id)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
