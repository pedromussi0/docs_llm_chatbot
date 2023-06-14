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


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        # Handle POST request as before
        data = json.loads(request.body.decode("utf-8"))
        user_input = data.get("input_user")

        conversation = request.session.get("conversation", [])

        conversation.append(("user", user_input))

        response = chat_template(
            user_input, context=get_answer(user_input), conversation=conversation
        )

        conversation.append(("AI", response))

        request.session["conversation"] = conversation

        chat_data = {"conversation": conversation}

        return JsonResponse(chat_data)
    elif request.method == "GET":
        # Handle GET request to fetch the conversation
        conversation = request.session.get("conversation", [])

        chat_data = {"conversation": conversation}

        return JsonResponse(chat_data)
    else:
        # Handle other request methods
        return JsonResponse({"error": "Invalid request method."})
