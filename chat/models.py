from django.contrib.gis.db.models import PointField
from django.db import models


class Chat(models.Model):
    SOCIAL_NETWORKS = (
        (0, 'Telegram'),
        (1, 'Whats App'),
        (2, 'VK')
    )
    social_network = models.IntegerField(
        'Social Network',
        choices=SOCIAL_NETWORKS
    )
    city = models.CharField(
        'City',
        max_length=255,
        blank=True,
        null=True
    )
    city_district = models.CharField(
        'City district',
        max_length=255
    )
    postal_code = models.IntegerField(
        'Postal code',
        blank=True,
        null=True
    )
    street = models.CharField(
        'Street',
        max_length=255,
        blank=True,
        null=True
    )
    house_number = models.CharField(
        'House number',
        max_length=255,
        blank=True,
        null=True
    )
    residential_complex = models.CharField(
        'Residential complex',
        max_length=255,
        blank=True,
        null=True
    )
    chat_invite_link = models.CharField(
        'Chat invite link',
        max_length=255,
        blank=True,
        null=True
    )
    chat_id = models.CharField(
        'Chat id',
        max_length=255,
        blank=True,
        null=True
    )
    coordinates = PointField(
        'Chat coordinate',
        blank=True,
        null=True
    )
    is_private_house = models.BooleanField(
        'Private house',
        default=False
    )

    def __str__(self):
        if self.is_private_house:
            return f'Postal chat, {self.postal_code}'
        else:
            return f'{self.street}, {self.house_number}'

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
