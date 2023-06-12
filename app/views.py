from django.shortcuts import render
from .utils.langchain_url_handler import (
    get_split_docs,
    get_vectorstore,
    embed_documents,
)
from .utils.langchain_chat_handler import get_llm_response
from django.http import JsonResponse
from app.models import ProcessedDocument


def chat_view(request):
    processed_documents = ProcessedDocument.objects.all()
    if request.method == "POST":
        user_input = request.POST.get(
            "user_input"
        )  # Assuming the form field name is 'user_input'
        response = get_llm_response(user_input)
        return render(request, "app/index.html", {"response": response})
    else:
        return render(request, "app/index.html")
