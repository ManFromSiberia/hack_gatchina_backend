from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.models import Chat
from complaint.models import Complaint


class CreateComplaintView(APIView):
    def post(self, request, *args, **kwargs):
        complaint_text = request.data.get('text')
        chat_id = request.data.get('chat_id')
        chat = Chat.objects.get(chat_id=chat_id)
        Complaint.objects.create(text=complaint_text, chat=chat)
        return Response('Ok', status=status.HTTP_200_OK)
