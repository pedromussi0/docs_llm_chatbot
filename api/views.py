from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import ChatMessage
from api.serializers import ChatMessageSerializer


# Create your views here.


class ChatMessageView(ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


def get_messages():
    return ChatMessage.objects.order_by("timestamp")
