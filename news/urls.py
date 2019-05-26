from django.urls import path

from news.views import NewsUpdateView

urlpatterns = [
    path('updates/', NewsUpdateView.as_view()),
]
