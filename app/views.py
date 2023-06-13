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
        user_input = request.POST.get(
            "user_input"
        )  # Assuming the form field name is 'user_input'
        response = chat_template(user_input, context=get_answer(user_input))
        # response = find_answer(user_input)
        return render(request, "app/index.html", {"response": response})
    else:
        return render(request, "app/index.html")
