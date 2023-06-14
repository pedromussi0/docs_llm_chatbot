import langchain
from langchain.document_loaders import SeleniumURLLoader
from .link_scraper import *
from app.models import ProcessedDocument
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
import faiss
from langchain.schema import Document
from typing import List
import openai

scraped_links = scrape_links(url=settings.NEXT_DOCS_URL)


def load_documents(scraped_links: list) -> List[Document]:
    documents = []
    error_urls = []

    for url in scraped_links:
        try:
            loader = SeleniumURLLoader(urls=[url])
            new_documents = loader.load()
            documents.extend(new_documents)
        except ValueError:
            # Append the URL to the error list if loading fails
            error_urls.append(url)

    return documents


# ------------------- embeddings -------------------------------

processed_documents = ProcessedDocument.objects.all()


def get_split_docs():
    documents = [
        Document(page_content=doc.content, metadata={"source": doc.url})
        for doc in processed_documents
    ]
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200
    )
    docs = text_splitter.split_documents(documents)

    return docs


def embed_documents(docs):
    embeddings = OpenAIEmbeddings()
    embedded_documents = []

    for doc in docs:
        embedded_doc = embeddings.embed_documents(doc.page_content)
        embedded_documents.append(embedded_doc)

    return embedded_documents


def get_vectorstore():
    embeddings = OpenAIEmbeddings()

    return FAISS.load_local(
        "app/vectorstore/nextembeds", index_name="faiss_index", embeddings=embeddings
    )


# --------------------- querying --------------------------------


def get_answer(user_input):
    db = get_vectorstore()

    response = db.similarity_search(query=user_input)
    filtered_response = [
        {"content": doc.page_content, "metadata": doc.metadata} for doc in response
    ]

    return filtered_response
