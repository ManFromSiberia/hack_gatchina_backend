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
    pass
