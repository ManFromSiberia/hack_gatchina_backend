from django.contrib import admin
from django import forms
from mapwidgets import GooglePointFieldWidget

from chat.models import Chat


class ChatCoordinateForm(forms.ModelForm):
    class Meta:
        widgets = {
            'coordinates': GooglePointFieldWidget()
        }


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    fields = ('social_network', 'city', 'city_district', 'postal_code', 'street', 'house_number', 'residential_complex',
              'chat_id', 'chat_invite_link', 'coordinates', 'is_private_house')
    search_fields = ('street', 'city', 'house_number')
    form = ChatCoordinateForm
