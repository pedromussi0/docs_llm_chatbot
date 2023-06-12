from django.shortcuts import render
from .utils.langchain_url_handler import (
    get_split_docs,
    get_vectorstore,
    embed_documents,
    find_answer,
)
from .utils.langchain_chat_handler import get_llm_response
from django.http import JsonResponse
from app.models import ProcessedDocument


def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get(
            "user_input"
        )  # Assuming the form field name is 'user_input'
        response = find_answer(user_input)
        return render(request, "app/index.html", {"response": response})
    else:
        return render(request, "app/index.html")
