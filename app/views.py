from api.views import get_messages
from .utils.langchain_url_handler import (
    get_answer,
)
from .utils.langchain_chat_handler import chat_template
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatMessage
from api.serializers import ChatMessageSerializer


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
@csrf_exempt
def submit_message(request):
    if request.method == "POST":
        # Save the user's message
        data = json.loads(request.body.decode("utf-8"))
        user_input = data.get("input_user")
        user_message = ChatMessage.objects.create(sender="user", content=user_input)

        # Generate AI response using chat_template
        response = chat_template(
            user_input, context=get_answer(user_input), conversation=[user_message]
        )

        # Save the AI's response
        ai_message = ChatMessage.objects.create(sender="ai", content=response)

        # Return the AI response message as JSON
        response_data = {
            "sender": ai_message.sender,
            "content": ai_message.content,
            "timestamp": ai_message.timestamp,
        }
        return JsonResponse(response_data)

    elif request.method == "GET":
        # Get all the chat messages
        messages = get_messages()

        # Prepare the conversation data
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
