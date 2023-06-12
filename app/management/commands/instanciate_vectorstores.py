from django.core.management.base import BaseCommand
from app.models import ProcessedDocument
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter


class Command(BaseCommand):
    help = "Load documents and embeddings from the database and initialize vector store"

    def handle(self, *args, **options):
        # Retrieve all ProcessedDocument objects from the database
        processed_documents = ProcessedDocument.objects.all()

        # Convert ProcessedDocument objects to Langchain Documents
        documents = [
            Document(page_content=doc.content, metadata={"source": doc.url})
            for doc in processed_documents
        ]

        # Split the documents into chunks using CharacterTextSplitter
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200
        )
        docs = text_splitter.split_documents(documents)

        # Initialize Embeddings and the FAISS vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(documents=docs, embedding=embeddings)

        vectorstore.save_local("app/vectorstore", index_name="faiss_index")
