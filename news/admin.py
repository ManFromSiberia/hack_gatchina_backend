from django.contrib import admin

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'address', 'news_id', 'is_new')
    list_display = ('news_id', 'is_new')
    list_editable = ('is_new',)
