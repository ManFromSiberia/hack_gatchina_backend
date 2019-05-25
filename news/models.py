from django.db import models


class News(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    address = models.CharField(max_length=256, blank=True)
    is_new = models.BooleanField(default=False)
