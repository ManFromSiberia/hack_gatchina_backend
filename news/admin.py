from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'address', 'chats', 'news_id', 'is_new')
    list_display = ('title', 'is_new')
    list_editable = ('is_new',)
    autocomplete_fields = ('chats',)
