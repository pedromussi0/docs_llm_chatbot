from django.shortcuts import render
from .utils.langchain_url_handler import (
    get_split_docs,
    get_vectorstore,
    embed_documents,
    get_answer,
)
from .utils.langchain_chat_handler import chat_template
from django.http import JsonResponse
from app.models import ProcessedDocument
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from .serializers import ChatMessageSerializer


# ------------------------------------------------------------------------------


class ChatMessageView(APIView):
    def get(self, request):
        messages = ChatMessage.objects.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------------------------------------
@csrf_exempt
def submit_message(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user_input = data.get("input_user")

        user_message = ChatMessage.objects.create(sender="user", content=user_input)

        # Generate AI response using chat_template
        response = chat_template(
            user_input, context=get_answer(user_input), conversation=[user_message]
        )

        ai_message = ChatMessage.objects.create(sender="ai", content=response)

        # Return the AI response message as JSON
        response_data = {
            "sender": ai_message.sender,
            "content": ai_message.content,
            "timestamp": ai_message.timestamp,
        }
        return JsonResponse(response_data)

    elif request.method == "GET":
        messages = ChatMessage.objects.all()
        conversation = [
            {
                "sender": message.sender,
                "content": message.content,
                "timestamp": message.timestamp,
            }
            for message in messages
        ]
        chat_data = {"conversation": conversation}
        return JsonResponse(chat_data)

    else:
        return JsonResponse({"error": "Invalid request method."})
