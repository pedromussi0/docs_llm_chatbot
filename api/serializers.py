from rest_framework import serializers
from app.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "content", "timestamp"]
