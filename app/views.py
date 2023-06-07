from django.shortcuts import render

from .models import ChatMessage
from .utils.langchain_chat_handler import generate_chat
from .utils.langchain_url_handler import *


def chat(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        history = [
            {"role": msg.sender, "text": msg.content}
            for msg in ChatMessage.objects.all()
        ]
        ai_response = generate_chat(
            history, user_input
        )  # Use llm_data from your_llm_script directly
        ai_message = ChatMessage(sender="ai", content=ai_response)
        ai_message.save()

        user_message = ChatMessage(sender="user", content=user_input)
        user_message.save()

    else:
        user_input = ""  # Set default user_input when the page is initially loaded

    messages = ChatMessage.objects.all()

    context = {"messages": messages}

    return render(request, "app/index.html", context)
