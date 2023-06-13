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


def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("input_user")

        conversation = request.session.get("conversation", [])

        conversation.append(("user", user_input))

        response = chat_template(
            user_input, context=get_answer(user_input), conversation=conversation
        )

        conversation.append(("AI", response))

        request.session["conversation"] = conversation

        chat_data = {
            "conversation": conversation  # Pass the entire conversation to the template
        }

        return render(request, "app/index.html", {"chat_data": chat_data})
    else:
        return render(request, "app/index.html")
