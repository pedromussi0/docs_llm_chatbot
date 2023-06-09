from django.shortcuts import render
from django.views import View
from .models import ChatMessage, ProcessedDocument  # Import your model
from .utils.langchain_chat_handler import generate_chat
from .utils.langchain_url_handler import find_answer, embed_documents


class QASearchView(View):
    def get(self, request):
        return render(request, "qa_search.html")

    def post(self, request):
        # Get the documents and their embeddings from the database
        documents = list(ProcessedDocument.objects.values())

        # Extract the contents and embeddings
        contents = [doc["content"] for doc in documents]
        embedded_documents = [doc["embedded_document"] for doc in documents]

        context = request.POST.get("context")
        question = request.POST.get("question")

        # Embed the context and question
        embedded_context = embed_documents(
            context
        )  # Assuming "embed_documents" handles a single string input
        embedded_question = embed_documents(
            question
        )  # Assuming "embed_documents" handles a single string input

        # Perform question-answering
        answer, answer_doc_id = find_answer(
            embedded_question, embedded_context, contents
        )

        # Get the URL of the best matching document
        best_document_url = documents[answer_doc_id]["url"]

        return render(
            request, "index.html", {"answer": answer, "url": best_document_url}
        )
