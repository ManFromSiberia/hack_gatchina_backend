from django.urls import path

from chat.views import ChatsFromCoordinatesView, CreateNewChatView, ChatLinkView

urlpatterns = [
    path('chats_from_coordinates/', ChatsFromCoordinatesView.as_view()),
    path('create/', CreateNewChatView.as_view()),
    path('link/<chat_id>/', ChatLinkView.as_view())
]
