from django.db import models

from chat.models import Chat


class Complaint(models.Model):
    text = models.TextField(
        'Complaint text',
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.DO_NOTHING,
        related_name='complaints',
        verbose_name='Chat',
    )

    def __str__(self):
        return f'Жалоба в чате {self.chat.__str__()}'

    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
