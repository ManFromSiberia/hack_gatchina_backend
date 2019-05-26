from django.urls import path
from .views import CreateComplaintView

urlpatterns = [
    path('create/', CreateComplaintView.as_view())
]