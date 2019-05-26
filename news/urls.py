from django.urls import path

from news.views import NewsUpdateView, NewsPostCompleteView

urlpatterns = [
    path('updates/', NewsUpdateView.as_view()),
    path('<id>/complete/', NewsPostCompleteView.as_view())
]
