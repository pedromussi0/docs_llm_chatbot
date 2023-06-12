from django.core.management.base import BaseCommand
from app.models import ProcessedDocument
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.text_splitter import CharacterTextSplitter
from django.core.cache import cache
import faiss
import time


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
        embedding_size = 1536
        index = faiss.IndexFlatL2(embedding_size)
        vector_store = FAISS(embeddings.embed_query, index, InMemoryDocstore({}), {})

        delay_between_calls = 50 / len(docs)  # Calculate the required delay
        vector_stores_left = len(docs)

        # Add the documents to the vector_store with a delay
        for document in docs:
            # Introduce a delay
            time.sleep(delay_between_calls)
            vector_store.add_documents([document])
            vector_stores_left -= 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Vector store created successfully! Vector stores left: {vector_stores_left}"
                )
            )

        # Save the vector store instance to the cache
        cache.set("vector_store", vector_store)
